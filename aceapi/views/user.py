from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from aceapi.models import AppUser, TutorStudent
from aceapi.models.score import Score

class AppUserView(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET request for a single app_user

        Returns:
            Response: JSON serialized user instance
        """
        try:
            app_user=AppUser.objects.get(pk=pk)
            if app_user.user.is_staff:
                serializer = TutorSerializer(app_user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
  
                # scores = Score.objects.filter(student = app_user)
                ##! Getting error that score object is not subscriptable
                # english = int(max(scores, key=lambda x:x['english'])['english'])
                # math = int(max(scores, key=lambda x:x['math'])['math'])
                # reading = int(max(scores, key=lambda x:x['reading'])['reading'])
                # science = int(max(scores, key=lambda x:x['science'])['science'])
                # overall = (english + math + reading + science) / 4

                # app_user.superscore = {
                #     "english": english,
                #     "math": math,
                #     "reading": reading,
                #     "science": science,
                #     "overall": overall
                # }

                serializer = StudentSerializer(app_user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except AppUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk):
        """update app_user"""
        try:
            user = AppUser.objects.get(pk=pk)
            auth_user = User.objects.get(pk = user.user_id)
            user.bio = request.data['bio']
            auth_user.email = request.data['email']
            auth_user.first_name = request.data['firstName']
            auth_user.last_name = request.data['lastName']
            if user.user.is_staff:
                user.billing_rate = request.data['billingRate']
            else:
                user.day_id = request.data['dayId']
                user.start_time = request.data['startTime']
                user.end_time = request.data['endTime']
                user.parent_name = request.data['parentName']
                user.parent_email = request.data['parentEmail']
            auth_user.save()
            user.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except AppUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False)
    def current(self,request):
        """get current user"""
        user = AppUser.objects.get(user = request.auth.user)
        if user.user.is_staff:
            serializer = TutorSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = StudentSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


    @action(methods=['get'], detail=False)
    def students(self,request):
        """get list of student users"""
        students = AppUser.objects.filter(user__is_staff = False)
        for student in students:
            try:
                pair = TutorStudent.objects.get(student_id = student)
                student.unassigned = False
                student.tutor_id = pair.tutor_id
            except TutorStudent.DoesNotExist:
                student.unassigned = True
                student.tutor_id = "0"

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(methods=['get'], detail=False)
    def tutors(self,request):
        """get list of tutor users"""
        tutors = AppUser.objects.filter(user__is_staff = True)
        serializer = TutorSerializer(tutors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(methods=['put'], detail=True)
    def activate(self,request, pk):
        """activate user"""
        try:
            user = User.objects.get(pk=pk)
            if user.is_active:
                user.is_active = 0
                user.save()
                return Response({'message: user has been deactivated'},
                                status=status.HTTP_204_NO_CONTENT)

            else:
                user.is_active = 1
                user.save()
                return Response({'message: user is now active'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    # @action(methods=['put'], detail=True)
    # def deactivate(self,request, pk):
    #     """activate user"""
    #     try:
    #         user = User.objects.get(pk=pk)
    #         user.is_active = 0
    #         user.save()
    #         return Response({'message: user has been deactivated'},
    #                         status=status.HTTP_204_NO_CONTENT)
    #     except User.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_superuser', 'username', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active')

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AppUser
        fields = ('id', 'user', 'bio', 'day',
                  'start_time', 'end_time', 'parent_name', 'parent_email',
                  'focus_areas', 'superscore', 'unassigned', 'tutor_id')
        depth = 1

class TutorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AppUser
        fields = ('id', 'user', 'bio', 'billing_rate')
        depth = 1
