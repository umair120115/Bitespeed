from rest_framework import serializers
from .models import CustomUser, Contact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', "username", "email", "password",'name']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class ContactSerializers(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ( 'id', 'phone', 'email', 'linkedId', 'linkPrecedence', 'createdAt', 'deletedAt', 'updatedAt' )

class InputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.IntegerField(required=False)

class OutputSerializer(serializers.Serializer):
    primaryContactId = serializers.UUIDField()
    emails = serializers.ListField()
    phoneNumbers = serializers.ListField()
    secondaryContactIds= serializers.ListField()
