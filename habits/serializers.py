from rest_framework import serializers
from rest_framework.serializers import ValidationError

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        # validators = [VideoReferenceValidator(field="video_reference")]

    def validate(self, data):
        if data.get('related_habit') and data('award'):
            raise ValidationError('Поля related_habit и award не могут быть одновременно заполнены')
        if data.get('is_pleasant') is True and data.get('award') or data.get('relared_field'):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
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
