from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()  # This uses your custom User model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'phone_number', 'street_address',
                  'city', 'state', 'postal_code', 'country', 'date_of_birth')
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'full_name', 'phone_number',
                  'street_address', 'city', 'state', 'postal_code', 'country', 'date_of_birth')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 since it's not needed in the creation process
        user = User.objects.create_user(**validated_data)  # Use your custom create_user method
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Get the default data (token, etc.)
        data['email'] = self.user.email  # Add the user's email to the response
        data['full_name'] = self.user.full_name  # Add the user's full name to the response
        return data  # Return only the data dictionary, not a tuple
