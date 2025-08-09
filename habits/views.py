from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    # pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        if serializer.validated_data['is_pleasant'] is True:
            serializer.validated_data['interval'] = None
        serializer.save()
