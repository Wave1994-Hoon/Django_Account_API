import jwt
import json

from .models      import Account, AccountInfo, TokenBlackList
from my_settings  import SECRET_KEY

from django.http            import JsonResponse,HttpResponse
from django.core.exceptions import ValidationError

class Login_Check:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY["secret"], SECRET_KEY["algorithm"])
                user          = Account.objects.get(id = token_payload["account"]).id
                request.user  = user

                return self.original_function(self, request, *args, **kwargs)

            return JsonResponse({"messaege":"NEED_LOGIN"}, status=401)

        except jwt.DecodeError:
            return JsonResponse({"message":"INVALID_USER"}, status=401)

def validate_password(password):
    validate_condition = [
        lambda s: any(x.isupper() for x in s),
        lambda s: any(x.islower() for x in s),
        lambda s: any(x.isdigit() for x in s),
        lambda s: len(s) == len(s.replace(" ","")),
        lambda s: len(s) >= 10
    ]
    
    for validator in validate_condition:
        if not validator(password):
            return True