from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email="test@test.com")
        self.habit = Habit.objects.create(
            action="test action", is_pleasant="True", is_public="True", user=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habits:habit-list")
        data = {
            "action": "выпить кофе",
            "is_pleasant": "True",
            "is_public": "True",
        }
        response = self.client.post(url, data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)
        self.assertEqual(data.get("action"), Habit.objects.get(pk=2).action)

    def test_lesson_update(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {
            "action": "выпить вкусный кофе",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)
        self.assertEqual(data.get("action"), "выпить вкусный кофе")

    def test_lesson_delete(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()
        print(data)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "related_habit": None,
                    "place": None,
                    "time": None,
                    "action": self.habit.action,
                    "is_pleasant": True,
                    "interval": 1,
                    "award": None,
                    "time_to_complete": None,
                    "is_public": True,
                    "user": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class HabitValidationTestCase(APITestCase):
    """Тестируем валидацию данных"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email="test@test.com")
        self.non_pleasant_habit = Habit.objects.create(
            place="Дома",
            time="21:00:00",
            action="Мыть посуду",
            is_pleasant="False",
            interval=1,
            award="Съесть сникерс",
            time_to_complete=timedelta(seconds=90),
            is_public="True",
            user=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_both_related_habit_and_prize(self):
        message = "У полезной привычки не могут быть одновременно связанная привычка и вознаграждение."
        data = {
            "related_habit": 12,
            "place": "Дома",
            "time": "21:00:00",
            "action": "Мыть посуду",
            "is_pleasant": False,
            "interval": 1,
            "award": "Съесть сникерс",
            "time_to_complete": "00:02:00",
            "is_public": True,
            "user": 2,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaisesMessage(Exception, message):
            serializer.validate(data)

    def test_pleasant_habit_on_related_habit(self):
        message = (
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )
        data = {
            "related_habit": 13,
            "action": "Мыть посуду",
            "is_pleasant": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaisesMessage(Exception, message):
            serializer.validate(data)

    def test_pleasant_habit_on_prize(self):
        message = (
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )
        data = {
            "award": "Съесть бутер",
            "action": "Мыть посуду",
            "is_pleasant": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaisesMessage(Exception, message):
            serializer.validate(data)

    def test_useful_habit_on_related_habit_or_prize(self):
        message = (
            "У полезной привычки должна быть связанная привычка или вознаграждение."
        )
        data = {
            "place": "Дома",
            "time": "21:00:00",
            "action": "Мыть посуду",
            "is_pleasant": False,
            "interval": 1,
            "time_to_complete": "00:02:00",
            "is_public": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaisesMessage(Exception, message):
            serializer.validate(data)

    def test_useful_habit_on_place(self):
        message = "Для полезной привычки необходимо указать время, место, время на выполнение."
        data = {
            "related_habit": 12,
            "time": "21:00:00",
            "action": "Мыть посуду",
            "is_pleasant": False,
            "interval": 1,
            "time_to_complete": "00:02:00",
            "is_public": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaisesMessage(Exception, message):
            serializer.validate(data)

    def test_time_to_complete(self):
        message = "Время выполнения должно быть не больше 120 секунд."
        data = {
            "id": 11,
            "place": "Дома",
            "time": "21:00:00",
            "action": "Мыть посуду",
            "is_pleasant": False,
            "interval": 1,
            "award": "Съесть сникерс",
            "time_to_complete": timedelta(seconds=150),
            "is_public": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaisesMessage(Exception, message):
            serializer.validate(data)

    def test_interval(self):
        message = "Периодичность выполнения не должна быть равна 0 или более 7."
        data = {
            "place": "Дома",
            "time": "21:00:00",
            "action": "Мыть посуду",
            "is_pleasant": False,
            "interval": 9,
            "award": "Съесть сникерс",
            "time_to_complete": timedelta(seconds=20),
            "is_public": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        with self.assertRaisesMessage(Exception, message):
            serializer.validate(data)
