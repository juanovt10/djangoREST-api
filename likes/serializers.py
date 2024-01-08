from django.db import IntegrityError
from rest_framework import serializers
from .models import Likes

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Likes
        fields = ['id', 'owner', 'created_at', 'post',]

    
    def create(self, validated_data):
        try: 
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
