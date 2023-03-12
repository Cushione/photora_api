from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer
from profiles.serializers import ProfileListSerializer
from photora_api.permissions import IsOwnerOrReadOnly
from functools import reduce
import operator
from django.db.models import Q


class PostList(APIView, PageNumberPagination):
    """
    Post List API View for retrieving and creating posts.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        # If the user is authenticated, filter out own posts and posts from
        # profiles that the user follows. Otherwise retrieve all posts
        if request.user.is_authenticated:
            exclude = [
                profile.owner
                for profile in request.user.followed_profiles.all()
            ]
            posts = Post.objects.exclude(
                Q(owner=request.user) | Q(owner__in=exclude)
            )
        else:
            posts = Post.objects.all()
        # Paginate result
        paginated = self.paginate_queryset(posts, request, view=self)
        # Serialize result
        serializer = PostSerializer(
            paginated, many=True, context={"request": request}
        )
        # Send paginated response
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        # Serialize data
        serializer = PostSerializer(
            data=request.data, context={"request": request}
        )
        # Save post if data is valid and return created post
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If data is invalid, send 400 response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    """
    Post Detail API View for retieving, updating or deleting posts.
    """

    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, id):
        # Find specified post or show error page if not found
        post = get_object_or_404(Post, id=id)
        # Serialize post
        serializer = PostSerializer(post, context={"request": request})
        # Send response
        return Response(serializer.data)

    def put(self, request, id):
        # Find specified post or show error page if not found
        post = get_object_or_404(Post, id=id)
        # Check if the user can edit the post
        self.check_object_permissions(request, post)
        # Serialize data
        serializer = PostSerializer(
            post, data=request.data, context={"request": request}, partial=True
        )
        # Update post if data is valid and return updated post
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # If data is invalid, send 400 response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        # Find specified post or show error page if not found
        post = get_object_or_404(Post, id=id)
        # Check if the user can delte the post
        self.check_object_permissions(request, post)
        # Delete post
        post.delete()
        # Return 204 response
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLike(APIView):
    """
    Post Like API View for retieving all the likes from posts and liking
    posts.
    """

    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        # Find specified post or show error page if not found
        post = get_object_or_404(Post, id=id)
        # Serialize profiles that liked the post
        serializer = ProfileListSerializer(
            post.likes, many=True, context={"request": request}
        )
        # Send respone
        return Response(serializer.data)

    def post(self, request, id):
        # Find specified post or show error page if not found
        post = get_object_or_404(Post, id=id)
        # If the user liked the post, remove user from the likes
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the user does not like the post yet, add user to likes
        else:
            post.likes.add(request.user)
            return Response(status=status.HTTP_201_CREATED)


class PostSearch(APIView, PageNumberPagination):
    """
    Post Search API View for retieving posts by keywords
    """

    serializer_class = PostSerializer

    def get(self, request):
        # Get keywords from query parameters
        keyword_list = request.query_params.get("keywords")
        if keyword_list:
            # Split keywords string
            keywords = keyword_list.split()
            # Generate search query
            # Every keywords has to be in either the title, description or
            # in the owner's profile name
            search_query = reduce(
                operator.and_,
                (
                    Q(
                        Q(title__icontains=keyword)
                        | Q(description__icontains=keyword)
                        | Q(owner__profile__name__icontains=keyword)
                    )
                    for keyword in keywords
                ),
            )
            # Retrieve posts with the search query
            search_result = Post.objects.filter(search_query)
            # Paginate result
            paginated = self.paginate_queryset(
                search_result, request, view=self
            )
            # Serialize result
            serializer = PostSerializer(
                paginated, many=True, context={"request": request}
            )
            # Send paginated response
            return self.get_paginated_response(serializer.data)
        # Return 400 response if no keywords were provided
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfilePosts(APIView):
    """
    Profile Posts API View for retieving all posts from a specified user profile
    """

    serializer_class = PostSerializer

    def get(self, request, id):
        # Retrieve all the posts from specified user profile
        posts = Post.objects.filter(owner__profile__id=id)
        # Serialize data
        serializer = PostSerializer(
            posts, many=True, context={"request": request}
        )
        # Send response
        return Response(serializer.data)


class FollowPostList(APIView, PageNumberPagination):
    """
    Follow Post List API View for retieving all posts from followed profiles
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all the profile the request user follows
        followed = [
            profile.owner for profile in request.user.followed_profiles.all()
        ]
        # Find all the posts of the profiles
        posts = Post.objects.filter(owner__in=followed)
        # Paginate result
        paginated = self.paginate_queryset(posts, request, view=self)
        # Serialize result
        serializer = PostSerializer(
            paginated, many=True, context={"request": request}
        )
        # Send paginated response
        return self.get_paginated_response(serializer.data)


class LikedPostList(APIView, PageNumberPagination):
    """
    Liked Post List API View for retieving all the liked posts
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all the posts the request user liked
        liked = request.user.liked_posts.all()
        # Paginate result
        paginated = self.paginate_queryset(liked, request, view=self)
        # Serialize result
        serializer = PostSerializer(
            paginated, many=True, context={"request": request}
        )
        # Send paginated response
        return self.get_paginated_response(serializer.data)
