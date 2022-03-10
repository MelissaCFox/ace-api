from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from aceapi.models import SubjectArea

class SubjectAreaView(ViewSet):

    def list(self, request):
        """Handle GET requests to subject_areas resource

        Returns:
            Response: JSON serialized list of subject_area instances
        """
        subject_areas=SubjectArea.objects.all()

        serializer=SubjectAreaSerializer(subject_areas, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single subject_area

        Returns:
            Response: JSON serialized subject_area instance
        """
        try:
            subject_area=SubjectArea.objects.get(pk=pk)
            serializer = SubjectAreaSerializer(subject_area)
            return Response(serializer.data)
        except SubjectArea.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class SubjectAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectArea
        fields = ('id', 'subject', 'name')
        depth = 1
