from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from . serializers import RegistrationSerializer
from core.settings import DEFAULT_FROM_EMAIL

# Create your views here.
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)


        send_mail(
            "Welcome to Videoflix",
            "Thank you for registering. Please confirm your email address.",
            DEFAULT_FROM_EMAIL,
            [user.email]
        )
        return Response({"user": serializer.data, "token": str(refresh)}, status=201)
