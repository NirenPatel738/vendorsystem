from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model
Vendor = get_user_model()


class CreateVendorSerialzier(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendor
        fields = ("id", "name", "password", "phone", "vendor_code", "address", )
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'name': {'required': True},
            'phone': {'required': True},
            'address': {'required': True},
        }

    def create(self, validated_data):
        user = Vendor.objects.create_user(**validated_data)
        return user


class VendorLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("id", "name", "phone", "vendor_code", "address", "date_joined")


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("id", "name", "phone", "vendor_code", "address", "on_time_delivery_rate", "quality_rating_avg", "average_response_time", "fulfillment_rate", "date_joined")

    def validate(self, attrs):
        phone = attrs.get('phone')
        if phone:
            if Vendor.objects.filter(phone=phone).exists():
                if Vendor.objects.filter(phone=phone).count() > 1:
                    msg = {'error': 'Phone number is already associated with another user. Try a new one.', 'status':False}
                    raise serializers.ValidationError(msg)

        return attrs

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            if Vendor.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'), phone=phone, password=password)

            else:
                msg = {'error': 'Phone number is not registered.','register': False}
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.HyperlinkedModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, trim_whitespace=False)

    class Meta:
        model=Vendor
        fields = ('old_password','new_password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance
