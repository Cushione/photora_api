from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer, ProfileListSerializer
from photora_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer

    def get(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        serializer = ProfileSerializer(
            profile, context={'request': request})
        return Response(serializer.data)


class ProfileFollow(APIView):
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        serializer = ProfileListSerializer(
            profile.followers, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        if profile.owner == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if profile.followers.filter(id=request.user.id).exists():
            profile.followers.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            profile.followers.add(request.user)
            return Response(status=status.HTTP_201_CREATED)


class UserProfile(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        profile = get_object_or_404(Profile, owner=request.user)
        serializer = ProfileSerializer(
            profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        profile = get_object_or_404(Profile, owner=request.user)
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(
            profile, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
