from rest_framework import serializers
from .models import Client, Request, Rating, News, Request2

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _


#This client serializer doesnt hash passwords
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
         
'''
#This client serializer hashes client passwords
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)#removes plain text p/word
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)#sets hashed password
        instance.save()
        return instance
'''

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Client.objects.filter(email=value).exists():
            print(Client.objects.all().values('email'))
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
            user = Client.objects.get(pk=uid)
        except Client.DoesNotExist:
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
    

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class RequestSerializer2(serializers.ModelSerializer):
    
    image1 = serializers.ImageField(required=False, allow_null=True)
    image2 = serializers.ImageField(required=False, allow_null=True)
    image3 = serializers.ImageField(required=False, allow_null=True)
    image4 = serializers.ImageField(required=False, allow_null=True)
    image5 = serializers.ImageField(required=False, allow_null=True)

    file1 = serializers.FileField(required=False, allow_null=True)
    file2 = serializers.FileField(required=False, allow_null=True)
    file3 = serializers.FileField(required=False, allow_null=True) 
    
    class Meta:
        model = Request2
        fields = '__all__'

    # def to_internal_value(self, data):
    #     # Only include file fields if they are present in data
    #     data = {key: value for key, value in data.items() if value is not None}
    #     return super().to_internal_value(data)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


'''
class CartItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    quantity = serializers.IntegerField()

class OrderRequestSerializer(serializers.Serializer):
    cart = CartItemSerializer(many=True)
'''