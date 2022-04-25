from rest_framework.authentication import get_authorization_header, BaseAuthentication
from .models import User
from rest_framework import exceptions
from django.conf import settings
from datetime import datetime, timedelta
import jwt


class AuthenticationJWT(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("No authentication token is provided")

        token = auth_token[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            expiration = payload.get('expiration', None)
            datetime_expiration = datetime.strptime(expiration, '%Y-%m-%dT%H:%M:%S')

            if datetime.utcnow() > datetime_expiration:
                raise jwt.ExpiredSignatureError

            email = payload.get('email', None)
            user = User.objects.get(email=email)
            return (user, token)

        except jwt.ExpiredSignatureError as error:
            raise exceptions.AuthenticationFailed("The given token is expired")
        except jwt.DecodeError as error:
            raise exceptions.AuthenticationFailed("The given token is invalid")
        except User.DoesNotExist as error:
            raise exceptions.AuthenticationFailed("The given user email is not valid")
