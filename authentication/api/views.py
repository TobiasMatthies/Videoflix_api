from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, CustomTokenObtainPairSerializer
from core.settings import DEFAULT_FROM_EMAIL
import django_rq


def send_activation_email(user_id, token):
    """
    Sends the activation email to the user in a background task.
    """
    try:
        user = User.objects.get(pk=user_id)
        uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))

        send_mail(
            "Welcome to Videoflix",
            f"""Thank you for registering. Please confirm your email address.
                Activate your account by clicking the link below:
                http://127.0.0.1:5500/pages/auth/activate.html?uid={uid}&token={token}
            """,
            DEFAULT_FROM_EMAIL,
            [user.email]
        )
    except User.DoesNotExist:
        print(f"Attempted to send activation email for non-existent user ID: {user_id}")


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = default_token_generator.make_token(user)

        django_rq.enqueue(send_activation_email, user.id, token)

        return Response({
            "user": serializer.data,
            "token": token
        }, status=201)


class ActivateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid, token):
        try:
            user_id = urlsafe_base64_decode(uid).decode('utf-8')
            user = User.objects.get(pk=user_id)

            if user.is_active:
                return Response({"message": "Account already activated."}, status=400)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Account successfully activated."}, status=200)
            else:
                return Response({"error": "Invalid or expired activation link."}, status=400)

        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"error": "Invalid activation link."}, status=400)


class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data.get("access")

        response = Response({"message": "success"}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.data = {"detail": "Login successful", "user": serializer.validated_data["user"]}
        return response


class LogoutAPIView(APIView):
    #Todo: add permission class to check if refresh token is sent
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."}, status=200)
