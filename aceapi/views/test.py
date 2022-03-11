from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from aceapi.models import AppUser, Test, Like


class TestView(ViewSet):

    def list(self, request):
        """Handle GET requests to tests resource

        Returns:
            Response: JSON serialized list of test instances
        """
        tests=Test.objects.all()
        tutor = AppUser.objects.get(user_id = request.auth.user.id)
        for test in tests:
            try:
                Like.objects.get(tutor = tutor, test = test)
                test.liked = True
            except Like.DoesNotExist:
                test.liked = False

        serializer=TestSerializer(tests, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single test

        Returns:
            Response: JSON serialized test instance
        """
        try:
            test=Test.objects.get(pk=pk)
            tutor = AppUser.objects.get(user_id = request.auth.user.id)
            try:
                Like.objects.get(tutor = tutor, test = test)
                test.liked = True
            except Like.DoesNotExist:
                test.liked = False
            serializer = TestSerializer(test)
            return Response(serializer.data)
        except Test.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self,request):
        """handle POST request to create a new test instance"""
        try:
            test = Test.objects.create(
                name = request.data['name'],
                year = request.data['year'],
                num_sci = request.data['numSci']
            )
            serializer = TestSerializer(test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except AppUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk):
        """handle DELETE request for a test resource"""
        try:
            test = Test.objects.get(pk=pk)
            test.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Test.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['put'], detail=True)
    def like(self,request, pk):
        """like or unlike a test"""
        try:
            like = Like.objects.get(test=pk, tutor__user_id=request.auth.user.id)
            like.delete()
            return Response({'message: removed like from test'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            tutor = AppUser.objects.get(user_id = request.auth.user.id)
            test = Test.objects.get(pk=pk)
            like = Like.objects.create(
                tutor = tutor,
                test = test
            )
            return Response({'message: user liked the test'}, status=status.HTTP_204_NO_CONTENT)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'name', 'year', 'num_sci', 'liked')
        depth = 1
