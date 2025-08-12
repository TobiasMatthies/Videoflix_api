from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from core.settings import DEFAULT_FROM_EMAIL

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


def send_password_reset_email(user_id, token):
    try:
        user = User.objects.get(pk=user_id)
        uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))

        send_mail(
            "Password Reset Videoflix",
            f"""To change your password, please click the link below. If you did not
            request your password to be changed, ignore this email.
            http://127.0.0.1:5500/pages/auth/confirm_password.html?uid={uid}&token={token}
            """,
            DEFAULT_FROM_EMAIL,
            [user.email]
        )
    except User.DoesNotExist:
        print(f"Attempted to send activation email for non-existent user ID: {user_id}")
