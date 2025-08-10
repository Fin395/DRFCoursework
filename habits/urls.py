from django.urls import path
from rest_framework.routers import DefaultRouter
from habits.apps import HabitsConfig
from habits.views import HabitViewSet, PublicHabitListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"habit", HabitViewSet, basename="habit")
urlpatterns = [
    path('public-habit/', PublicHabitListAPIView.as_view(), name="public-habit-list"),
    # path("lesson/", LessonListAPIView.as_view(), name="lesson-list"),
    # path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-get"),
    # path(
    #     "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"
    # ),
    # path(
    #     "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"
    # ),
    # path("subs/create/", SubscriptionAPIView.as_view(), name="subs-create"),
] + router.urls
