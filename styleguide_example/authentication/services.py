from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template import loader


def send_password_reset_email(*, user):
    token = token_generator.make_token(user)

    context = {'reset_url': f"{settings.FRONTEND_URL}/reset-password-confirm/?token={token}&uid={user.id}"}
    
    body = loader.render_to_string('forgotten_password_email.html', context)

    send_mail(
        subject=f"DemoSite: Reset password",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def user_reset_password(*, user, token, password):
    if not token_generator.check_token(user, token):
        raise ValidationError({"token": ["Invalid value"]})

    user.set_password(password)

    user.save()
