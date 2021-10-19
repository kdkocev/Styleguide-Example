from django.urls import path

from .apis import (
    UserLoginApi,
    UserLogoutApi,
    UserMeApi,
    UserPasswordResetApi,
    UserPasswordResetConfirmApi,
)

urlpatterns = [
    path(
        'login/',
        UserLoginApi.as_view(),
        name='login'
    ),
    path(
        'logout/',
        UserLogoutApi.as_view(),
        name='logout'
    ),
    path(
        'me/',
        UserMeApi.as_view(),
        name='me'
    ),
    path(
        'password-reset/',
        UserPasswordResetApi.as_view(),
        name="password-reset"
    ),
    path(
        'password-reset-confirm/',
        UserPasswordResetConfirmApi.as_view(),
        name="password-reset-confirm"
    ),
]
