from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import RegistrationSerializer, CustomTokenObtainPairSerializer
import django_rq
from . utils import send_activation_email, send_password_reset_email


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
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response({"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."}, status=200)
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response

        return Response({"detail": "No refresh token provided."}, status=400)


class TokenRefreshAPIView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response({"error": "Refresh token not found in cookies"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access_token = serializer.validated_data["access"]
        response = Response()

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return Response({"detail": "Token refreshed", "acces": access_token}, status=status.HTTP_200_OK)


class PasswordResetAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)

        if user:
            django_rq.enqueue(send_password_reset_email, user.id, token)
        return Response({"detail": "Password reset functionality not implemented yet."}, status=status.HTTP_200_OK)
