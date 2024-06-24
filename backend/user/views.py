from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from .serializers import UserLoginSerializer
from .serializers import CustomTokenSerializer
#from .serializers import UserSerializerRecoverPass

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from django_rest_passwordreset.serializers import PasswordTokenSerializer
from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.conf import settings
from rest_framework import status, exceptions
from django.core.exceptions import ValidationError

from rest_framework.views import APIView

from rest_framework import parsers, renderers

from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from django.utils import timezone
from datetime import timedelta

from trazas.utils import savelog

class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        # log purpuse
        contextLogs = {
            'user_email': request.data.get("email", "AnonymousUser"),
            'message': 'Usuario accediendo a parcelas',
            'status': 'success',
            'extra_data': {
                'status_code': status_code,
            }
        }
        #savelog(contextLogs,request)
        # end log purpuse

        return Response(response, status=status_code)
"""
class UserRecoverPassView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserSerializerRecoverPass

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

"""

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    tipo = 'reset' #serializador.data['type']
    site_url_reset = settings.SITE_URL + 'reset_password'
    site_shortcut_name = 'Data4SmartFarming'
    language = reset_password_token.user.language
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(site_url_reset, reset_password_token.key),
        'site_name': site_shortcut_name,
        'site_domain': site_url_reset,
    }

    # render email text
    title = ''
    if tipo == 'reset':
        if language == 'es':
            title = "=?utf-8?Q?=F0=9F=94=91Resetear_contrase=C3=B1a_de_D4SmartFarming?="
            email_html_message = render_to_string('user_reset_password.html', context)
            email_plaintext_message = render_to_string('user_reset_password.txt', context)
        else:
            title = "=?utf-8?Q?=F0=9F=94=91Reset_D4SmartFarming_password?="
            email_html_message = render_to_string('user_reset_password_en.html', context)
            email_plaintext_message = render_to_string('user_reset_password.txt', context)
    else:
        if language == 'es':
            title = "=?utf-8?Q?=F0=9F=8E=89Bienvenido_a_D4SmartFarming?="
            email_html_message = render_to_string('user_reset_password_welcome.html', context)
            email_plaintext_message = render_to_string('user_reset_password.txt', context)
        else:
            title = "=?utf-8?Q?=F0=9F=8E=89Welcome_to_D4SmartFarming?="
            email_html_message = render_to_string('user_reset_password_welcome_en.html', context)
            email_plaintext_message = render_to_string('user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        title,
        # message:
        email_plaintext_message,
        # from:
        "D4SmartFarming <soporte@d4smartfarming.com>",
        # to:
        [reset_password_token.user.email],
        # BCC
        ['backups@smartbits.es']
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()

class CustomPasswordTokenVerificationView(APIView):
    """
    An Api View which provides a method to verifiy that a given pw-reset token is valid before actually confirming the
    reset.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'invalid'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        # check if user has password to change
        if not reset_password_token.user.has_usable_password():
            return Response({'status': 'irrelevant'})

        return Response({'status': 'OK'})

class CustomResetPasswordConfirm(APIView):
    """
    An Api View which provides a method to reset a password based on a unique token
    """
    throttle_classes = ()
    permission_classes = ()
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        # change users password (if we got to this code it means that the user is_active)
        if reset_password_token.user.eligible_for_reset():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
            try:
                # validate the password against existing validators
                validate_password(
                    password,
                    user=reset_password_token.user,
                    password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                )
            except ValidationError as e:
                # raise a validation error for the serializer
                raise exceptions.ValidationError({
                    'password': e.messages
                })

            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

        # Delete all password reset tokens for this user
        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({'status': 'OK'})