from .env_reader import env

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.mailtrap.io"
EMAIL_PORT = 2525
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default='')
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default='')
EMAIL_USE_TLS = True

# Uncomment to send actual emails
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
