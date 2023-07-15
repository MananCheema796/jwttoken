from rest_framework import serializers
from .models import CustomUser
from .models import Student
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password' ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'city']


class LoginSerializer(serializers.Serializer):

    email = serializers.CharField(
        label="email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
            email=email, password=password)
            if not user:
                msg = 'Access denied: wrong email or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model= CustomUser
        fields = ['id', 'first_name', 'email']



class ChangePassSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=30)
    new_password1 = serializers.CharField(max_length=30)
    new_password2 = serializers.CharField(max_length=30)

    def validate(self, attrs):
        print("attrs", attrs)
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError("new passwords dosn't match")

        user= self.context.get('user')

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError('old password is  incorrect')
        
        user.set_password(attrs["new_password1"])
        user.save()
        
        return attrs

