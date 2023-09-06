from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializer import CreateUserSerializer
from .models import User
# Create your views here.

class UserView(CreateAPIView):
    serializer_class = CreateUserSerializer

class UsernameCountView(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        data = {
            'username': username,
            'count':count,
        }
        return Response(data)

class MobileCountView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(username=mobile).count()
        data = {
            'username': mobile,
            'count':count,
        }
        return Response(data)

