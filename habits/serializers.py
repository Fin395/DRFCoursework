from rest_framework import serializers
from rest_framework.serializers import ValidationError
from datetime import timedelta
from django.forms.models import model_to_dict

from habits.models import Habit
from users.models import User


class HabitSerializer(serializers.ModelSerializer):
    related_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.none(), allow_null=True, required=False)

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ('user',)

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
        instance = getattr(self, 'instance', None)

        if instance:
            current_data = model_to_dict(instance)
            current_data.update(data)
            current_data.pop('user')

        else:
            current_data = data

        if current_data.get('is_pleasant'):
            if current_data.get('award') or current_data.get('related_habit'):
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
        else:
            if current_data.get('related_habit') and current_data.get('award'):
                raise ValidationError('У полезной привычки не могут быть одновременно связанная привычка и вознаграждение.')

            elif not current_data.get('related_habit') and not current_data.get('award'):
                raise ValidationError('У полезной привычки должна быть связанная привычка или вознаграждение.')

            elif not current_data.get('time') or not current_data.get('place') or not current_data.get('time_to_complete'):
                raise ValidationError('Для полезной привычки необходимо указать время, место, время на выполнение.')

            elif current_data.get('time_to_complete') > timedelta(seconds=120):
                raise ValidationError('Время выполнения должно быть не больше 120 секунд.')

            elif current_data.get('related_habit'):
                related_habit_id = current_data.get('related_habit').id
                habit = Habit.objects.get(pk=related_habit_id)

                if habit.is_pleasant is False:
                    raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки.')

        return current_data


class HabitReducedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'action', 'time', 'time_to_complete', 'interval']
