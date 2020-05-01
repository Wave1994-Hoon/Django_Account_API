import json
import bcrypt
import jwt

from .models       import Account, AccountInfo, TokenBlackList
from my_settings   import SECRET_KEY
from .utils        import Login_Check, validate_password

from django.views            import View
from django.http             import HttpResponse, JsonResponse
from django.db               import IntegrityError
from django.core.validators  import validate_email
from django.core.exceptions  import ValidationError
from django.db               import IntegrityError, transaction
from datetime                import datetime, timedelta

class SignUp(View):
    def post(self, request):
        ''' 회원 가입 '''
        try:
            with transaction.atomic():

                data = json.loads(request.body)
                validate_email(data['email'])

                if validate_password(data["password"]):
                    return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)

                if Account.objects.filter(email=data['email']).exists():
                    return JsonResponse({'message' : 'EXISTS_EMAIL'}, status=400)

                user = Account.objects.create(
                    email  = data['email'],
                    name   = data['name'],
                    gender = data['gender'],
                )

                AccountInfo.objects.create(
                    account_id   = user.id,
                    password     = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8'),
                    phone_number = data['phone_number'],
                    nickname     = data['nickname']
                )

                return HttpResponse(status=200)

        except ValidationError:
            return JsonResponse({'message' : 'VALIDATION_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)


class SignIn(View):
    def post(self, request):
        ''' 로그인 '''
        try:
            data = json.loads(request.body)
            validate_email(data["email"])

            if Account.objects.filter(email=data["email"]).exists():
                account   = Account.objects.get(email=data["email"])
                user_info = AccountInfo.objects.get(account_id=account.id)

                if bcrypt.checkpw(data["password"].encode(), user_info.password.encode("UTF-8")):
                    token = jwt.encode({"account" : account.id, 'exp':datetime.utcnow() + timedelta(days=3)}, SECRET_KEY["secret"], SECRET_KEY["algorithm"]).decode("UTF-8")

                    return JsonResponse({"Authorization" : token}, status=200)

                return HttpResponse(status=401)

            return JsonResponse({"message" : "NOT_EXISTS_MAIL"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)


class AccountView(View):
    @Login_Check
    def get(self, request):
        try:
            # profile = Account.objects.filter(id=request.user).values('name', 'gender')
            profile = Account.objects.get(id=request.user)
            
            profile_data = {
                'name' : profile.name,
                'email' : profile.email,
                'gender' : profile.gender,
                'nickname' : AccountInfo.objects.get(account_id=profile.id).nickname,
                'phone_number' : AccountInfo.objects.get(account_id=profile.id).phone_number,
            }

            return JsonResponse({"account_profile": profile_data}, status=200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"}, status=400)
        except Account.DoesNotExist:
            return JsonResponse({'message': 'ACCOUNT_DOES_NOT_EXISTS'}, status=401)


class AccountList(View):
    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 5))

        account_list = Account.objects.order_by('created_at').values('email', 'name', 'gender')[offset:offset+limit]

        return JsonResponse({'data' : list(account_list)}, status = 200)


class AccountSearch(View):
    def post(self, request):
        try:
            keywords     = {}
            account_info = []

            if request.GET.get('name'):
                keywords['name'] = request.GET.get('name')

            if request.GET.get('email'):
                keywords['email'] = request.GET.get('email')
            
            users = Account.objects.filter(**keywords)

            account_info = [{
                'name'         : user.name,
                'gender'       : user.gender,
                'phone_number' : AccountInfo.objects.get(id=user.id).phone_number,
                'nickname'     : AccountInfo.objects.get(id=user.id).nickname,               
            } for user in users]
            
            return JsonResponse({'data' : account_info}, status=200)
        
        except KeyError:
             return JsonResponse({'message' : 'INVALID_KEY'}, status=400)
