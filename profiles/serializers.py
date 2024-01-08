from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # Create the serializer 
    owner = serializers.ReadOnlyField(source='owner.username')

    # As it was used in django forms, we define the model and the fields
    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image',
        ]


