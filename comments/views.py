from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .models import Comment
from .serializers import CommentSerializer
from posts.models import Post
from photora_api.permissions import IsOwnerOrReadOnly


class CommentsPagination(PageNumberPagination):
    """
    Custom pagination for comments
    """
    # Sets the page size to 20 comments
    page_size = 20


class CommentList(APIView, CommentsPagination):
    """
    Comment List API View for retrieving and creating comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):
        # Retrieve all the comments connected to specified post
        comments = Comment.objects.filter(post=post_id)
        # Paginate result
        paginated = self.paginate_queryset(comments, request, view=self)
        # Serialize result
        serializer = CommentSerializer(
            paginated, many=True, context={'request': request}
            )
        # Send paginated response
        return self.get_paginated_response(serializer.data)

    def post(self, request, post_id):
        # Find specified post or show error page if not found
        post = get_object_or_404(Post, id=post_id)
        # Serialize data
        serializer = CommentSerializer(
            data=request.data, context={'request': request}
        )
        # Save comment if data is valid and return created comment
        if serializer.is_valid():
            serializer.save(owner=request.user, post=post)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        # If data is invalid, send 400 response
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CommentDetail(APIView):
    """
    Comment Detail API View for retieving, updating or deleting comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, post_id, id):
        # Find specified comment or show error page if not found
        comment = get_object_or_404(Comment, post=post_id, id=id)
        # Serialize comment
        serializer = CommentSerializer(comment, context={'request': request})
        # Send response
        return Response(serializer.data)

    def put(self, request, post_id, id):
        # Find specified comment or show error page if not found
        comment = get_object_or_404(Comment, post=post_id, id=id)
        # Check if the user can edit the comment
        self.check_object_permissions(request, comment)
        # Serialize data
        serializer = CommentSerializer(
            comment, data=request.data, context={'request': request})
        # Update comment if data is valid and return updated comment
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # If data is invalid, send 400 response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, id):
        # Find specified comment or show error page if not found
        comment = get_object_or_404(Comment, post=post_id, id=id)
        # Check if the user can delete the comment
        self.check_object_permissions(request, comment)
        # Delete comment
        comment.delete()
        # Return 204 response
        return Response(status=status.HTTP_204_NO_CONTENT)
