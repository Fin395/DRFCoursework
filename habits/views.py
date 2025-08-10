from rest_framework.viewsets import ModelViewSet
from rest_framework import generics


from habits.models import Habit
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializer, HabitReducedSerializer
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        if serializer.validated_data['is_pleasant'] is True:
            serializer.validated_data['interval'] = None
        serializer.save()

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def get_permissions(self):
        self.permission_classes = []
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in self.permission_classes]


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitReducedSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
