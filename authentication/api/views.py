from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RegistrationSerializer
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
                http://localhost:8000/api/activate/{uid}/{token}
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
