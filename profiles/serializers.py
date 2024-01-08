from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # Create the serializer 
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    # This method provides the check to see if the
    # owner of the profile is logged in
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # As it was used in django forms, we define the model and the fields
    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner',
        ]


