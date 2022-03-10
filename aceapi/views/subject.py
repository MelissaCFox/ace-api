from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from aceapi.models import Subject

class SubjectView(ViewSet):

    def list(self, request):
        """Handle GET requests to subjects resource

        Returns:
            Response: JSON serialized list of subject instances
        """
        subjects=Subject.objects.all()

        serializer=SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single subject

        Returns:
            Response: JSON serialized subject instance
        """
        try:
            subject=Subject.objects.get(pk=pk)
            serializer = SubjectSerializer(subject)
            return Response(serializer.data)
        except Subject.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('id', 'subject')
        depth = 1
