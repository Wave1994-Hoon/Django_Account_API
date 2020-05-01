from django.db    import models

class Account(models.Model):
    email      = models.EmailField(max_length=100, unique=True)
    name       = models.CharField(max_length=20)
    gender     = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts'


class AccountInfo(models.Model):
    account      = models.ForeignKey(Account, on_delete=models.CASCADE)
    password     = models.CharField(max_length=400)
    phone_number = models.IntegerField(max_length=20)
    nickname     = models.CharField(max_length=30)
    is_deleted   = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_info'


class TokenBlackList(models.Model):
    access_token = models.CharField(max_length=500)

    class Meta:
        db_table = 'token_black_list'

