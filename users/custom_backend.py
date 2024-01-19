from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

#Web3
from eth_account.messages import encode_defunct
from web3 import Account, Web3

User = get_user_model()

class PasswordBackend(ModelBackend):
    def authenticate(self, request, password=None, wallet=None, **kwargs):
        if set(request.data.keys()) == {"wallet","password"}:
            try:
                user = User.objects.get(wallet=wallet, password=password)
            except User.DoesNotExist:
                return None

            return user
        else:
            return None

# def verify_signature(address, signature, message):
#     message_hash = encode_defunct(text=message)
#     try:
#         # Recover the public key from the signature
#         public_key = Account.recover_message(message_hash, signature=signature)
#         # Convert the public key to an Ethereum address
#         recovered_address = Web3.toChecksumAddress(Account.from_key(public_key).address)
#         # Compare the recovered address with the provided address
#         if address == recovered_address:
#             return True
#     except:
#         pass
#     return False