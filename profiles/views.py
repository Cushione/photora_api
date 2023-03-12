from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer, ProfileListSerializer
from photora_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    """
    Profile List API View for retrieving profiles.
    """

    def get(self, request):
        # Get all profiles
        profiles = Profile.objects.all()
        # Serialize result
        serializer = ProfileSerializer(
            profiles, many=True, context={"request": request}
        )
        # Send response
        return Response(serializer.data)


class ProfileDetail(APIView):
    """
    Profile Detail API View for retieving and updating profiles.
    """

    serializer_class = ProfileSerializer

    def get(self, request, id):
        # Find specified profile or show error page if not found
        profile = get_object_or_404(Profile, id=id)
        # Serialize comment
        serializer = ProfileSerializer(profile, context={"request": request})
        # Send response
        return Response(serializer.data)


class ProfileFollow(APIView):
    """
    Profile Follow API View for retieving all the followers and following
    profiles
    """

    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Find specified profile or show error page if not found
        profile = get_object_or_404(Profile, id=id)
        # Serialize profiles that follow the profile
        serializer = ProfileListSerializer(
            profile.followers, many=True, context={"request": request}
        )
        # Send respone
        return Response(serializer.data)

    def post(self, request, id):
        # Find specified profile or show error page if not found
        profile = get_object_or_404(Profile, id=id)
        # If the request user is the owner of the profile send 400 response
        if profile.owner == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # If the user follows the profile, remove user from the followers
        if profile.followers.filter(id=request.user.id).exists():
            profile.followers.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the user does not follow the profile yet, add user to followers
        else:
            profile.followers.add(request.user)
            return Response(status=status.HTTP_201_CREATED)


class UserProfile(APIView):
    """
    User Profile API View for retieving and updating the profile of the
    request user
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        # Find specified profile or show error page if not found
        profile = get_object_or_404(Profile, owner=request.user)
        # Serialize profile
        serializer = ProfileSerializer(profile, context={"request": request})
        # Send respone
        return Response(serializer.data)

    def put(self, request):
        # Find specified profile or show error page if not found
        profile = get_object_or_404(Profile, owner=request.user)
        # (Redundant) Check if the user can edit the post
        self.check_object_permissions(request, profile)
        # Serialize data
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        # Update profile if data is valid and return updated profile
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # If data is invalid, send 400 response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
