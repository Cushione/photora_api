from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from .serializers import CommentSerializer
from posts.models import Post
from photora_api.permissions import IsOwnerOrReadOnly


class CommentList(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
 
    def get(self, request, post_id):
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(
            comments, many=True, context={'request': request}
            )
        return Response(serializer.data)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user, post=post)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CommentDetail(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, post_id, id):
        comment = get_object_or_404(Comment, post=post_id, id=id)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, post_id, id):
        comment = get_object_or_404(Comment, post=post_id, id=id)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(
            comment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, id):
        comment = get_object_or_404(Comment, post=post_id, id=id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
