from rest_framework import serializers
from rest_framework.serializers import ValidationError
from datetime import timedelta

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    related_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.none())

    class Meta:
        model = Habit
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            self.fields['related_habit'].queryset = Habit.objects.filter(
                is_public=True
            ) | Habit.objects.filter(
                user=request.user
            )

    def validate(self, data):
        if data.get('is_pleasant'):
            if data.get('award') or data.get('related_habit'):
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

        else:
            if data.get('related_habit') and data.get('award'):
                raise ValidationError('У полезной привычки не могут быть одновременно связанная привычка и вознаграждение.')

            elif not data.get('related_habit') or data.get('award'):
                raise ValidationError('У полезной привычки должна быть связанная привычка или вознаграждение.')


            elif not data.get('time') or not data.get('place') or not data.get('time_to_complete'):
                raise ValidationError('Для полезной привычки необходимо указать время, место, время на выполнение.')

            elif data.get('time_to_complete') > timedelta(seconds=120):
                raise ValidationError('Время выполнения должно быть не больше 120 секунд.')

            elif data.get('related_habit'):
                id = data.get('related_habit').id
                habit = Habit.objects.get(pk=id)

                if habit.is_pleasant is False:
                    raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки.')

        return data
