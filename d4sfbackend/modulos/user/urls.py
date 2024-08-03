from django.urls import re_path as url, include
from .views import UserRegistrationView, UserLoginView, CustomPasswordTokenVerificationView, CustomResetPasswordConfirm


urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^signin', UserLoginView.as_view()),
    url(r'^password_reset/verify-token', CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
    url(r'^password_reset/confirm', CustomResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    url(r'^password_reset', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
]