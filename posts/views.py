from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer
from profiles.serializers import ProfileListSerializer
from photora_api.permissions import IsOwnerOrReadOnly
from functools import reduce
import operator
from django.db.models import Q


class PostList(APIView):
    serializer_class = PostSerializer
 
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
            )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class PostDetail(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id):
        post = get_object_or_404(Post, id=id)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLike(APIView):
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = ProfileListSerializer(
            post.likes, many=True, context={'request': request}
            )
        return Response(serializer.data)

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            post.likes.add(request.user)
            return Response(status=status.HTTP_201_CREATED)


class PostSearch(APIView):
    serializer_class = PostSerializer

    def get(self, request):
        keyword_list = request.query_params.get('keywords')
        if keyword_list:
            keywords = keyword_list.split()
            search_query = reduce(
                operator.and_,
                (
                    Q(
                        Q(title__icontains=keyword)
                        | Q(description__icontains=keyword)
                    )
                    for keyword in keywords
                ),
            )

            search_result = Post.objects.filter(search_query)
            serializer = PostSerializer(
                search_result, many=True, context={'request': request}
            )
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

