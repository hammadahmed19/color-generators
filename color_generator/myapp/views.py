import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Colours
from .serializers import ColoursSerializer
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import generics 
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def create_colour_scheme(request):
    user_name = request.data.get('user_name')
 
    if not user_name:
        return Response({"error": "User name is required"}, status=status.HTTP_400_BAD_REQUEST)

    
    colours = request.data.get('colours')
    
   
    colour_data = {'user_name': user_name, 'colours': colours}

     
    serializer = ColoursSerializer(data=colour_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_colour_schemes_and_name(request):
    data = Colours.objects.all()
    serializer = ColoursSerializer(data, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_colour_scheme(request, pk):
    try:
        colour_scheme = Colours.objects.get(pk=pk)
    except Colours.DoesNotExist:
        return Response({"error": "Colour scheme not found"}, status=status.HTTP_404_NOT_FOUND)

  
    serializer = ColoursSerializer(colour_scheme, data=request.data, partial=True)   

    if serializer.is_valid():
        serializer.save()   
        return Response(serializer.data, status=status.HTTP_200_OK)  
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


@api_view(['DELETE'])
def delete_colour_scheme(request, pk):
    try:
        colour_scheme = Colours.objects.get(pk=pk)
        colour_scheme.delete()  # Delete the instance
        return Response({"message": "Colour scheme deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Colours.DoesNotExist:
        return Response({"error": "Colour scheme not found"}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        identifier = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')

        user = None

        if identifier:  
            try:
                if '@' in identifier:  
                    user = User.objects.get(email=identifier)
                else:  # Otherwise, treat it as a username
                    user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                user = None

            # Now, authenticate using the retrieved user (if found)
            if user is not None:
                user = authenticate(username=user.username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': user_serializer.data
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
        
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Get refresh token from request
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)

            # Blacklist the refresh token
            token.blacklist()

            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    