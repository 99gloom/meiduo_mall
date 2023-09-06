from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token

from .views import UserView, UsernameCountView, MobileCountView

urlpatterns = [
    re_path(r'users/$', UserView.as_view()),
    re_path(r'usernames/(?P<username>\w{5,20})/count/', UsernameCountView.as_view()),
    re_path(r'mobiles/(?P<mobile>1[3-9]\d{9})/count', MobileCountView.as_view()),

    # JWT登录
    re_path(r'^authorizations/$', obtain_jwt_token)
]