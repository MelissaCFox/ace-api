from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from aceapi.models import StudentSubjectArea, AppUser, SubjectArea
from aceapi.views.user import StudentSerializer


class StudentSubjectAreaView(ViewSet):

    def list(self, request):
        """Handle GET requests to student_subject_areas resource

        Returns:
            Response: JSON serialized list of student_subject_area instances
        """
        student_sas=StudentSubjectArea.objects.all()

        serializer=StudentSubjectAreaSerializer(student_sas, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single student_subject_area

        Returns:
            Response: JSON serialized student_subject_area instance
        """
        try:
            student_sa=StudentSubjectArea.objects.get(pk=pk)
            serializer = StudentSubjectAreaSerializer(student_sa)
            return Response(serializer.data)
        except StudentSubjectArea.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self,request):
        """handle POST request to create a new student_subject_area instance"""
        try:
            student = AppUser.objects.get(pk = request.data['studentId'])
            subject_area = SubjectArea.objects.get(pk=request.data['subjectAreaId'])
            student_sa = StudentSubjectArea.objects.create(
                student = student,
                subject_area = subject_area
            )
            serializer = StudentSubjectAreaSerializer(student_sa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk):
        """handle DELETE request for a student_subject_area resource"""
        try:
            student_sa = StudentSubjectArea.objects.get(pk=pk)
            student_sa.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except StudentSubjectArea.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class StudentSubjectAreaSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = StudentSubjectArea
        fields = ('__all__')
        depth = 1
