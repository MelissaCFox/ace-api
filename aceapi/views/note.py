from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from aceapi.models import Note, AppUser
from aceapi.views.user import StudentSerializer

class NoteView(ViewSet):

    def list(self, request):
        """Handle GET requests to notes resource

        Returns:
            Response: JSON serialized list of note instances
        """
        notes=Note.objects.all()

        serializer=NoteSerializer(notes, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single note

        Returns:
            Response: JSON serialized note instance
        """
        try:
            note=Note.objects.get(pk=pk)
            serializer = NoteSerializer(note)
            return Response(serializer.data)
        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self,request):
        """handle POST request to create a new note instance"""
        try:
            student = AppUser.objects.get(pk=request.data['studentId'])
            author = AppUser.objects.get(user_id=request.auth.user.id)

            note = Note.objects.create(
                student = student,
                author = author,
                note = request.data['note'],
                date = date.today(),
                pinned = request.data['pinned']
            )
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except AppUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, pk):
        """handle PUT request to an existing note"""
        try:
            note = Note.objects.get(pk=pk)
            note.note = request.data['note']
            note.pinned = request.data['pinned']
            note.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk):
        """handle DELETE request for a note resource"""
        try:
            note = Note.objects.get(pk=pk)
            note.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['put'], detail=True)
    def pin(self,request, pk):
        """pin and unpin notes"""
        try:
            note = Note.objects.get(pk=pk)
            if note.pinned == 1:
                note.pinned = 0
                note.save()
                return Response({'message: note is no longer pinned'},
                                status=status.HTTP_204_NO_CONTENT)
            elif note.pinned == 0:
                note.pinned = 1
                note.save()
                return Response({'message: note is now pinned'}, status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    # @action(methods=['put'], detail=True)
    # def unpin(self,request, pk):
    #     """unpin note"""
    #     try:
    #         note = Note.objects.get(pk=pk)
    #         note.pinned = 0
    #         note.save()
    #         return Response({'message: note is no longer pinned'},
    #                         status=status.HTTP_204_NO_CONTENT)
    #     except Note.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)



class AuthorSerializer(serializers.ModelSerializer):
    model = AppUser
    fields = ('__all__')

class NoteSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    # author = AuthorSerializer()
    class Meta:
        model = Note
        fields = ('__all__')
        depth = 1
