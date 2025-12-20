from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate

from apps.tasks.models import Task
from apps.accounts.models import User
from apps.tasks.serializers import (
    TaskListSerializer,
    TaskCreateSerializer,
    TaskStatusUpdateSerializer
)
from apps.tasks.views import (
    TaskListView,
    TaskCreateView,
    TaskStatusUpdateView,
    TaskDeleteView
)
from apps.common import data_tests


class TestTaskListView(APITestCase):
    def setUp(self):
        self.url = reverse('tasks:task-list')
        self.factory = APIRequestFactory()
        self.view = TaskListView.as_view()
        self.user = User.objects.create_user(**data_tests.test_user_register
                                             )
        self.admin = User.objects.create_user(
            **data_tests.test_admin_user_register
        )
        self.other_user = User.objects.create_user(
            **data_tests.test_other_user_register
        )
        self.task1 = Task.objects.create(
            user=self.user, **data_tests.test_tasks
        )
        self.task2 = Task.objects.create(
            user=self.user, **data_tests.test_tasks2
        )
        Task.objects.create(
            user=self.other_user, title="Other task", description="Other"
        )

    def test_get_tasks_authenticated(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        queryset = Task.objects.filter(user=self.user)
        serializer = TaskListSerializer(queryset, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, serializer.data)

    def test_get_tasks_unauthenticated(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tasks_only_own_tasks(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.other_user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotIn(self.task1.title, [t['title'] for t in response.data])


class TestTaskCreateView(APITestCase):
    def setUp(self):
        self.url = reverse('tasks:task-create')
        self.factory = APIRequestFactory()
        self.view = TaskCreateView.as_view()
        self.user = User.objects.create_user(**data_tests.test_user_register)

    def test_post_task_valid_data_authenticated(self):
        data = data_tests.test_tasks
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(
            user=self.user, title="Test").exists()
                        )
        self.assertEqual(response.data['title'], "Test")

    def test_post_task_invalid_data(self):
        data = {"name": "", "description": "Test"}
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_task_unauthenticated(self):
        data = data_tests.test_tasks
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTaskStatusUpdateView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = TaskStatusUpdateView.as_view()

        self.user = User.objects.create_user(**data_tests.test_user_register)
        self.other_user = User.objects.create_user(
            **data_tests.test_other_user_register
        )

        self.task = Task.objects.create(user=self.user, **data_tests.test_tasks)

    def test_patch_status_valid_authenticated_owner(self):
        data = {"status": "pending"}
        url = reverse('tasks:task-status-update', kwargs={'pk': self.task.pk})
        request = self.factory.patch(url, data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.task.pk)

        self.task.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task.status, "pending")
        self.assertEqual(response.data, TaskListSerializer(self.task).data)

    def test_patch_status_invalid_status(self):
        data = {"status": "invalid_status"}
        url = reverse('tasks:task-status-update', kwargs={'pk': self.task.pk})
        request = self.factory.patch(url, data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.task.pk)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_status_access_denied_other_user(self):
        data = {"status": "completed"}
        url = reverse('tasks:task-status-update', kwargs={'pk': self.task.pk})
        request = self.factory.patch(url, data, format='json')
        force_authenticate(request, user=self.other_user)
        response = self.view(request, pk=self.task.pk)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_status_unauthenticated(self):
        data = {"status": "completed"}
        url = reverse('tasks:task-status-update', kwargs={'pk': self.task.pk})
        request = self.factory.patch(url, data, format='json')
        response = self.view(request, pk=self.task.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestTaskDeleteView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = TaskDeleteView.as_view()

        self.user = User.objects.create_user(**data_tests.test_user_register)
        self.other_user = User.objects.create_user(
            **data_tests.test_other_user_register
        )

        self.task = Task.objects.create(
            user=self.user, **data_tests.test_tasks
        )

    def test_delete_task_authenticated_owner(self):
        url = reverse('tasks:task-delete', kwargs={'pk': self.task.pk})
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.task.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_task_access_denied_other_user(self):
        url = reverse('tasks:task-delete', kwargs={'pk': self.task.pk})
        request = self.factory.delete(url)
        force_authenticate(request, user=self.other_user)
        response = self.view(request, pk=self.task.pk)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_task_unauthenticated(self):
        url = reverse('tasks:task-delete', kwargs={'pk': self.task.pk})
        request = self.factory.delete(url)
        response = self.view(request, pk=self.task.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_nonexistent_task(self):
        url = reverse('tasks:task-delete', kwargs={'pk': 9999})
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=9999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)