from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        # If added new columns through the User model, add them in the fields
        # list as seen below
        fields = ('username', 'password', 'email',
                  'first_name', 'last_name', 'is_staff')

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=validated_data['is_staff']
            # If added new columns through the User model, add them in this
            # create method call in the format as seen above
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data.pop('refresh', None) # remove refresh from the payload
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['is_staff'] = self.user.is_staff
        return data