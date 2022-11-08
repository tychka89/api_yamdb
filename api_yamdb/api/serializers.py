from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')
        required_fields = ('email', 'username')


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validation_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Никнейм "me" запрещен')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
