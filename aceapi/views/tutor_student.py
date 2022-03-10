from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from aceapi.models import AppUser, TutorStudent
from aceapi.views.user import TutorSerializer, StudentSerializer


class TutorStudentView(ViewSet):

    def list(self, request):
        """Handle GET requests to tutor_students resource

        Returns:
            Response: JSON serialized list of tutor_student instances
        """
        pairs=TutorStudent.objects.all()

        serializer=TutorStudentSerializer(pairs, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single tutor_student

        Returns:
            Response: JSON serialized tutor_student instance
        """
        try:
            pair=TutorStudent.objects.get(pk=pk)
            serializer = TutorStudentSerializer(pair)
            return Response(serializer.data)
        except TutorStudent.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self,request):
        """handle POST request to create a new like instance"""
        try:
            tutor = AppUser.objects.get(pk = request.data['tutorId'])
            student = AppUser.objects.get(pk = request.data['studentId'])
            pair = TutorStudent.objects.create(
                tutor = tutor,
                student = student
            )
            serializer = TutorStudentSerializer(pair)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def update(self,request,pk):
        """handle PUT request for a tutor_student resource"""
        try:
            pair = TutorStudent.objects.get(pk=pk)
            tutor = AppUser.objects.get(pk = request.data['tutorId'])
            student = AppUser.objects.get(pk = request.data['studentId'])
            pair.tutor = tutor
            pair.student = student
            pair.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except TutorStudent.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  

    def destroy(self, request, pk):
        """handle DELETE request for a tutor_student resource"""
        try:
            pair = TutorStudent.objects.get(pk=pk)
            pair.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except TutorStudent.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class TutorStudentSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer()
    student = StudentSerializer()
    class Meta:
        model = TutorStudent
        fields = ('__all__')
        depth = 1
