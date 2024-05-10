from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

#Web3
# from eth_account.messages import encode_defunct
# from web3 import Account, Web3

User = get_user_model()

class Web3Authentication(BaseAuthentication):
    def authenticate(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header:
            return None
        
        # the header should be in the format "{public_key} {token}"
        public_key, token = auth_header.split(' ')[0], auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, public_key, algorithms="HS256")
        except jwt.InvalidTokenError:
            error_dict = {
                'errorMessage': 'Invalid or expired token',
            }
            raise exceptions.AuthenticationFailed(error_dict)
        
        user = self.get_user(payload)

        if not user:
            error_dict = {
                'errorMessage': 'Invalid wallet address',
            }
            raise exceptions.AuthenticationFailed(error_dict)

        return user

    def get_user(self, payload):
        wallet_address = payload.get('id') #retrieve wallet address from payload
        return User.objects.filter(wallet_address=wallet_address).first()
