from datetime import date
from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from aceapi.models import AppUser, Test, Like
from aceapi.views.user import TutorSerializer


class LikeView(ViewSet):

    def list(self, request):
        """Handle GET requests to likes resource

        Returns:
            Response: JSON serialized list of like instances
        """
        likes=Like.objects.filter(tutor__user_id = request.user.id)

        serializer=LikeSerializer(likes, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single like

        Returns:
            Response: JSON serialized like instance
        """
        try:
            like=Like.objects.get(pk=pk)
            serializer = LikeSerializer(like)
            return Response(serializer.data)
        except Like.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self,request):
        """handle POST request to create a new like instance"""
        try:
            tutor = AppUser.objects.get(user_id = request.auth.user.id)
            test = Test.objects.get(pk=request.data['testId'])
            like = Like.objects.create(
                tutor = tutor,
                test = test
            )
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk):
        """handle DELETE request for a like resource"""
        try:
            like = Like.objects.get(pk=pk)
            like.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class LikeSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer()
    class Meta:
        model = Like
        fields = ('__all__')
        depth = 1
