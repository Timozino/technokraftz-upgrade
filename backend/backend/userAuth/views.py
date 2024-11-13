from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from . models import CustomUser, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from api.serializer import RegistrationSerializer, CustomUserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
import random
from rest_framework_simplejwt.tokens import RefreshToken

def generate_random_otp(length=8):
    otp = ''.join([str(random.randint(0,9)) for _ in range(length)])
    return otp

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token["username"] = user.username
        token["fullname"] = user.fullName
        token["email"] = user.email
        
        return token
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
class RegisterView(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    permission_classes=[AllowAny]
    serializer_class=RegistrationSerializer
    
    
# class PasswordResetVerifyView(generics.RetrieveAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = CustomUserSerializer
    
#     def get_object(self):
#         email=self.kwargs['email']
        
#         #user=CustomUser.objects.get(email=email)
#         user=CustomUser.objects.filter(email=email).first()
        
#         if user:
           
            
#             uuidb64 = user.pk
#             refresh = RefreshToken.for_user(user)
#             refresh_token = str(refresh.access_token)
#             user.refresh_token = refresh_token
#             user.otp = generate_random_otp()
            
#             user.save()
            
#             link = f"http://localhost:5173/create-new-password/?otp{user.otp}&uuidb64={uuidb64}&=refresh_token{refresh_token}"
#             print("link===", link)
            
#         else:
#             return "You were not initially registered"
        
#         return user

class PasswordResetVerifyView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer
    
    def get_object(self):
        email = self.kwargs['email']
        
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise NotFound("User not found or not initially registered")
        
        # If user is found, proceed with token generation and OTP
        uuidb64 = user.pk
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh.access_token)
        user.refresh_token = refresh_token
        user.otp = generate_random_otp()
        user.save()
        
        link = f"http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"
        print("link ===", link)
        
        context = {
            "link":link,
            "username":user.username
        }
        subject = "Password Reset Email"
        text_body = render_to_string("email/password_reset.txt", context)
        html_body = render_to_string("email/password_reset.html", context)
        msg = send_mail(
            subject,
            "mod.timson@gmail.com",
            [user.email],
            text_body
            
        )
        #msg.attach_alternative(html_body, "text/html")
       # msg.send
        
        
        return user


class PasswordChangeView(generics.CreateAPIView):
    permission_classes =[AllowAny]
    serializer_class = CustomUserSerializer
    
    def create(self, request, *args, **kwargs):
        #payload = request.data
        
        otp=request.data['otp']
        uuidb64=request.data['uuidb64']
        password=request.data['password']
        
        user = CustomUser.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            user.pop(otp)
            user.save()
            
            return Response({"message":"Password successfully changed"}, status=status.HTTP_201_CREATED)
        else:return Response({"message":"No user with this credentials in our Database"}, status=status.HTTP_404_NOT_FOUND)
        