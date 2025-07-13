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