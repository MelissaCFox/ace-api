from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from aceapi.models import Score, AppUser, Test
from aceapi.views.user import StudentSerializer


class ScoreView(ViewSet):

    def list(self, request):
        """Handle GET requests to scores resource

        Returns:
            Response: JSON serialized list of score instances
        """
        scores=Score.objects.all()

        serializer=ScoreSerializer(scores, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single score

        Returns:
            Response: JSON serialized score instance
        """
        try:
            score=Score.objects.get(pk=pk)
            serializer = ScoreSerializer(score)
            return Response(serializer.data)
        except Score.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self,request):
        """handle POST request to create a new score instance"""
        try:
            student = AppUser.objects.get(pk = request.data['studentId'])
            test = Test.objects.get(pk=request.data['testId'])
            score = Score.objects.create(
                student = student,
                test = test,
                date = request.data['date'],
                english = request.data['english'],
                math = request.data['math'],
                reading = request.data['reading'],
                science = request.data['science']
            )
            serializer = ScoreSerializer(score)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        """handle PUT request for an existing score"""
        try:
            score = Score.objects.get(pk=pk)
            score.english = request.data['english'],
            score.math = request.data['math'],
            score.reading = request.data['reading'],
            score.science = request.data['science']
            score.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Score.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk):
        """handle DELETE request for a score resource"""
        try:
            score = Score.objects.get(pk=pk)
            score.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Score.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class ScoreSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = Score
        fields = ('__all__')
        depth = 1
