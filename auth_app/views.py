from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer


# Create your views here.
class RegisterAPI(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"status": True, "message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer
    
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={"status": True, "token": token.key , "message": "Logged in successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
         
            
    


        