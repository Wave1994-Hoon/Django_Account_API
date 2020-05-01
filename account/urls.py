from django.urls import path
from .views      import SignUp, SignIn, AccountView, AccountList, AccountSearch

urlpatterns = [
    path('/signup', SignUp.as_view()),
    path('/signin', SignIn.as_view()),
    path('/view', AccountView.as_view()),
    path('/list', AccountList.as_view()),
    path('/search', AccountSearch.as_view()),
]