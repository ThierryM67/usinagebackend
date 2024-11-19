from django.contrib.auth.models import User
from .models import News, ClientFAQ, ManFAQ, Contact, Admin
from rest_framework import serializers

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove password2 as it's not needed for user creation
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, data):
        # Ensure both password fields match if they are provided
        password = data.get('password')
        password2 = data.get('password2')
        if password and password2 and password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def update(self, instance, validated_data):
        # Remove password fields from validated data, as they need special handling
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If a password is provided, hash and set it
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Admin.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user associated with this email.")
        return value
    

class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Decode the uid to get the user
        try:
            uid = attrs.get('uid')
            user = Admin.objects.get(pk=uid)
        except Admin.DoesNotExist:
            raise serializers.ValidationError(_("Invalid user"))

        # Validate token
        token = attrs.get('token')
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(_("Invalid token"))

        # Validate the password
        new_password = attrs.get('new_password')
        validate_password(new_password, user)

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
    

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id', 'username', 'email', 'first_name', 'last_name')
    

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class ClientFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientFAQ
        fields = '__all__'


class ManFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManFAQ
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'