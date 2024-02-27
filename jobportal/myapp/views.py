from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics,viewsets
from rest_framework.views import APIView
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



# Create your views here.

###serializer for admin registration
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        
    def create(self, validated_data):
        # Hash the password before saving the user object
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
class PersonalinformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal_Information
        fields = '__all__'
    


@api_view(['GET'])
def home(rquest):
    return Response('welcome to job portal')

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def get(self, request, *args, **kwargs):
    #     queryset=User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)
    

class Add_personal(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        userr=request.user
        data= {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'gender': request.data.get('gender'),
            'date_of_birth': request.data.get('date_of_birth'),
            'location': request.data.get('location'),
            'phone_number': request.data.get('phone_number'),
            'user': userr.id  # Assuming user is a foreign key field in YourModel
        }
        serializer= PersonalinformationSerializer(data=data)
        print('serializer   ',serializer)
        if serializer.is_valid():
            print('validdd')
            serializer.save()
            return Response(serializer.data)
            print('yesss')
        return Response('personal informaion added successfully of ')
    
    def put(self, request, id, format=None):
        a=Personal_Information.objects.get(id=id)
        userr=request.user
        data= {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'gender': request.data.get('gender'),
            'date_of_birth': request.data.get('date_of_birth'),
            'location': request.data.get('location'),
            'phone_number': request.data.get('phone_number'),
            'user': userr.id  # Assuming user is a foreign key field in YourModel
        }
        serializer=PersonalinformationSerializer(a,data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
        
    
    def get(self,request):
        queryset=Personal_Information.objects.get(user=request.user)
        serializer = PersonalinformationSerializer(queryset)
        return Response(serializer.data)