from rest_framework import serializers
from rest_framework.serializers import ValidationError
from datetime import timedelta

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        # validators = [VideoReferenceValidator(field="video_reference")]

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

# class CourseSerializer(serializers.ModelSerializer):
#     lessons_count = serializers.SerializerMethodField()
#     lessons_data = LessonSerializer(source="lessons", many=True, read_only=True)
#     is_subscribed = serializers.SerializerMethodField()
#
#     def get_lessons_count(self, obj):
#         return obj.lessons.count()
#
#     def get_is_subscribed(self, obj):
#         course_subs = obj.subscriptions
#         current_user = self.context["request"].user
#
#         if course_subs.filter(user=current_user).exists():
#             return "подписка оформлена"
#         else:
#             return "подписка не оформлена"
#
#     class Meta:
#         model = Course
#         fields = "__all__"




    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super(MailingForm, self).__init__(*args, **kwargs)
    #     self.fields['recipient'].queryset = MailingRecipient.objects.filter(owner=user)
    #     self.fields['message'].queryset = EmailMessage.objects.filter(owner=user)
