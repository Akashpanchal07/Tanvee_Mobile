from rest_framework import serializers
from django.contrib.auth import authenticate
from common.models import User, Profile, Address


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mobile', 'password', 'email', 'username')
        extra_kwargs = {'password': {'write_only': True},
                        'email' : {'write_only': True},
                        'username' : {'write_only' : True},}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# used for giving in the login and update user profile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("id", "password", "last_login", "created_at", "updated_at",
                    "is_new_user", "is_superuser", "is_staff", "is_admin")


    def validate(self, attrs):
        mobile = attrs.get('mobile')
        if mobile:
            if User.objects.filter(mobile=mobile).exists():
                if User.objects.filter(mobile=mobile).count() > 1:
                    msg = {'detail': 'mobile number is already associated with another user. Try a new one.', 'status':False}
                    raise serializers.ValidationError(msg)

        return attrs


    def update(self, instance, validated_data):
        instance.mobile = validated_data['mobile']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.alternate_email =  validated_data['alternate_email']
        instance.username = validated_data['username']
        instance.profile_pic = validated_data['profile_pic']

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
            if User.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'), phone=phone, password=password)

            else:
                msg = {'detail': 'Phone number is not registered.','register': False}
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class AddressSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    def get_country(self, obj):
        return obj.get_country_display()

    class Meta:
        model = Address
        fields = ("addresses", "street", "city",
                  "state", "postcode", "country")

    def __init__(self, *args, **kwargs):
        account_view = kwargs.pop("account", False)

        super(AddressSerializer, self).__init__(*args, **kwargs)

        if account_view:
            self.fields["addresses"].required = True
            self.fields["street"].required = True
            self.fields["city"].required = True
            self.fields["state"].required = True
            self.fields["postcode"].required = True
            self.fields["country"].required = True


class CreateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            "role",
        )

    def __init__(self, *args, **kwargs):
        super(CreateProfileSerializer, self).__init__(*args, **kwargs)
        self.fields["role"].required = True


class ProfileSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    address = AddressSerializer()

    def get_user_details(self, obj):
        return UserSerializer(obj.user).data

    class Meta:
        model = Profile
        exclude = ('otp', 'count')
        # fields = ("id", 'user_details', 'role', 'address')