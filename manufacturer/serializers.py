from rest_framework import serializers
from .models import Manufacturer, Offer, Rating

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _


#manufacturer serializer that doesn't hash passwords

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
'''
#This manufacturer serializer hashes client passwords
class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
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
        if not Manufacturer.objects.filter(email=value).exists():
            print(Manufacturer.objects.all().values('email'))
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
            user = Manufacturer.objects.get(pk=uid)
        except Manufacturer.DoesNotExist:
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


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'