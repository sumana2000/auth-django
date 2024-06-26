from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

        # setting write_only=True ensures class object wont password is not returned as a response even though username and email is returned
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    # to hash the password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance