from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from aceapi.models import Day

class DayView(ViewSet):

    def list(self, request):
        """Handle GET requests to days resource

        Returns:
            Response: JSON serialized list of day instances
        """
        days=Day.objects.all()

        serializer=DaySerializer(days, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single day

        Returns:
            Response: JSON serialized day instance
        """
        try:
            food_type=Day.objects.get(pk=pk)
            serializer = DaySerializer(food_type)
            return Response(serializer.data)
        except Day.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class DaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Day
        fields = ('id', 'day')
        depth = 1
