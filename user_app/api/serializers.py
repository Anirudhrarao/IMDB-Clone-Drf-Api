from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(style={'input_type':'text'},write_only=True)
    # email = serializers.CharField(style={'input_type':'email'},write_only=True)
    # password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'Error':'password not matched'})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'Error':'Email already used try with different email'})
        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account