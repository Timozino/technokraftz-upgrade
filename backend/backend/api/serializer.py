
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from userAuth.models import CustomUser, Profile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = '__all__'
        
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
        
# class RegistrationSerializer(serializers.ModelSerializer):
#     password=serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2=serializers.CharField(write_only=True, required=True)
    
#     class Meta:
#         model=CustomUser
#         fields=["username","fullName","email", "password", "password2"]
        
#     def checkValidation(self, attr):
#         if attr["password"] != attr["password2"]:
#             raise serializers.ValidationError({"password":"Password did not match"})
        
#         return attr
    
#     def validate_username(self, value):
#         if CustomUser.objects.filter(username=value).exists():
#             raise serializers.ValidationError({"username":"A user with this username already exists!"})
#         return value

#     def validate_email(self, value):
#         if CustomUser.objects.filter(email=value).exists():
#             raise serializers.ValidationError({"email":"A user with this email already exists!"})
#         return value
    
#     def createUser(self, validated_data):
#         user = CustomUser.objects.create(
#             username = validated_data["username"],
#             fullName = validated_data["fullName"],
#             email = validated_data["email"],
            
#         ),
#         if user.username == "" or user.username== None:
#             emailUsername, _ = user.email.split("@")
#             user.username = emailUsername
            
#             user.set_password(validated_data["password"])
#             user.save()
#         else:
#             user.set_password(validated_data["password"])
#             user.save()
            
#         return user
            
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "fullName", "email", "password", "password2"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists!"})

        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists!"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 from validated_data
        user = CustomUser.objects.create_user(**validated_data)
        return user
            