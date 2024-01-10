from django.db.models import Count
from rest_framework import generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer

# from django.http import Http404
# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Profile
# from .serializers import ProfileSerializer
# from drf_api.permissions import IsOwnerOrReadOnly


# class ProfileList(APIView):
#     """
#     This view lists the app's exisiting profiles
#     """
#     def get(self, request):
#         # Get all profiles
#         profiles = Profile.objects.all()
#         # Assign serializer 
#         serializer = ProfileSerializer(
#             profiles, many=True, context={'request': request}
#         )
#         # return the data response from the serializer
#         return Response(serializer.data)


# class ProfileDetail(APIView):
#     """
#     This view is specific for each profile view
#     """

#     # This will display a from to perform the put method
#     serializer_class = ProfileSerializer
#     permission_classes = [IsOwnerOrReadOnly]

#     def get_object(self, pk):
#         """
#         This method handles the error if a url is with 
#         an invalid id
#         """
#         try:
#             # checks if the profile id exisits and returns it
#             profile = Profile.objects.get(pk=pk)
#             self.check_object_permissions(self.request, profile)
#             return profile
#         except Profile.DoesNotExist:
#             # If it does not exisit it returns an standard 
#             # django 404 handler
#             raise Http404

#     def get(self, request, pk):
#         """
#         This method gets the profile object with the serializer 
#         """
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile, context={'request': request}
#         )
#         return Response(serializer.data)

#     def put(self, request, pk):
#         """
#         This method lets update the editable fields of the Profile
#         model 
#         """
#         # Get the profile
#         profile = self.get_object(pk)
#         # Initiate the serializer with the requested data
#         serializer = ProfileSerializer(
#             profile, data=request.data, context={'request': request}
#         )
#         # Check if the serializer is valid, save it and return the data
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         # return any potential erros that could arise
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)