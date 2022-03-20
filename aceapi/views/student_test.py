from django.forms import ValidationError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from aceapi.models import AppUser, StudentTest, Test
from aceapi.views.user import StudentSerializer


class StudentTestView(ViewSet):

    def list(self, request):
        """Handle GET requests to student_tests resource

        Returns:
            Response: JSON serialized list of student_test instances
        """
        student = self.request.query_params.get('studentId', None)
        if student is not None:
            student_tests = StudentTest.objects.filter(Q(student_id = student))
        else:
            student_tests=StudentTest.objects.all()

        serializer=StudentTestSerializer(student_tests, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single student_test

        Returns:
            Response: JSON serialized student_test instance
        """
        try:
            student_test=StudentTest.objects.get(pk=pk)
            serializer = StudentTestSerializer(student_test)
            return Response(serializer.data)
        except StudentTest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self,request):
        """handle POST request to create a new like instance"""
        try:
            test = Test.objects.get(pk = request.data['testId'])
            student = AppUser.objects.get(pk = request.data['studentId'])
            student_test = StudentTest.objects.create(
                student = student,
                test = test,
                english = request.data['english'],
                math = request.data['math'],
                reading = request.data['reading'],
                science = request.data['science']
            )
            serializer = StudentTestSerializer(student_test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def update(self,request,pk):
        """handle PUT request for a student_test resource"""
        try:
            student_test = StudentTest.objects.get(pk=pk)

            student_test.english = request.data['english']
            student_test.math = request.data['math']
            student_test.reading = request.data['reading']
            student_test.science = request.data['science']
            
            no_english = request.data['english'] == "0,0,0,0,0"
            no_math = request.data['math'] == "0,0,0"
            no_reading = request.data['reading'] =="0,0,0,0"
            no_science = request.data['science'] == "0,0,0,0,0,0" or request.data['science'] == "0,0,0,0,0,0,0"

            if  no_english and no_math and no_reading and no_science:
                student_test.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                student_test.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
        except StudentTest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk):
        """handle DELETE request for a student_test resource"""
        try:
            student_test = StudentTest.objects.get(pk=pk)
            student_test.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except StudentTest.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class StudentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTest
        fields = ('id', 'english', 'math', 'reading', 'science', 'student', 'test',
                'completion')
        depth = 1
