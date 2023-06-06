import base64
import pyotp
from rest_framework import serializers
from rest_framework.response import Response

# from personal.settings import EMAIL_HOST_USER
from user import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_joined', 'is_staff', 'is_active', 'is_superuser']


def generate_otp(user):
    secret = base64.b32encode(user.encode())
    OTP = pyotp.TOTP(secret, interval=1000)
    return {'secret': secret, 'OTP': OTP.now()}


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        key = generate_otp(attrs['email'])
        key1 = key['OTP']
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = UserSerializer(self.user).data
        send_mail(
                    'OTP Verification',
                    f"your otp is {key1}",
                    'EMAIL_HOST_USER',
                    ['priyank.sharma@consolebit.com'],
                    fail_silently=False,
        )
        attrs['secret'] = key['secret']
        return {'secret_key': attrs['secret']}


class VerifySerializer(serializers.ModelSerializer):
    secret_key = serializers.CharField(max_length=255)
    otp = serializers.IntegerField()

    class Meta:
        model = models.User
        fields = ['secret_key', 'otp']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                     style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = models.User
        fields = ['id', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = models.User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
                                          last_name=validated_data['last_name'])

        user.set_password(validated_data['password'])
        user.is_active = True
        user.is_staff = True
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                     style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = models.User
        fields = ('email', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "password field didn't match"})
        return attrs


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        data = super().validate(attrs)
        key = generate_otp(attrs['email'])
        key1 = key['OTP']
        send_mail(
                    'OTP Verification',
                    f"your otp is {key1}",
                    'EMAIL_HOST_USER',
                    ['priyank.sharma@consolebit.com'],
                    fail_silently=False,
        )
        attrs['secret'] = key['secret']
        return {'secret_key': attrs['secret']}
        
    
    class Meta:
        model = models.User
        fields = ('email',)

class VerfiyOTPforgotpassword(serializers.ModelSerializer):
    secret_key = serializers.CharField(max_length=255)
    otp = serializers.IntegerField()    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                     style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = models.User
        fields = ('secret_key','otp', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "password field didn't match"})
        return attrs