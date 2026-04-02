from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from src.config.access_control import ROLE_FABRICA


class SessionExpirationMiddlewareTests(TestCase):
    def setUp(self):
        self.dashboard_url = reverse("dashboard")

    def test_default_user_is_logged_out_after_10_minutes_idle(self):
        user = User.objects.create_user(username="idle-user", password="123")
        self.client.force_login(user)

        now = timezone.now()
        session = self.client.session
        session["login_at"] = now.isoformat()
        session["last_activity_at"] = (now - timedelta(minutes=11)).isoformat()
        session.save()

        self.client.get(self.dashboard_url)

        self.assertNotIn("_auth_user_id", self.client.session)

    def test_fabrica_user_is_logged_out_after_12_hours_even_with_activity(self):
        user = User.objects.create_user(username="fabrica-user", password="123")
        group, _ = Group.objects.get_or_create(name=ROLE_FABRICA)
        user.groups.add(group)

        self.client.force_login(user)

        now = timezone.now()
        session = self.client.session
        session["login_at"] = (now - timedelta(hours=13)).isoformat()
        session["last_activity_at"] = now.isoformat() 
        session.save()

        self.client.get(self.dashboard_url)

        self.assertNotIn("_auth_user_id", self.client.session)

    def test_fabrica_user_ignores_idle_timeout_before_12_hours(self):
        user = User.objects.create_user(username="fabrica-active", password="123")
        group, _ = Group.objects.get_or_create(name=ROLE_FABRICA)
        user.groups.add(group)

        self.client.force_login(user)

        now = timezone.now()
        session = self.client.session
        session["login_at"] = (now - timedelta(hours=2)).isoformat()
        session["last_activity_at"] = (now - timedelta(minutes=20)).isoformat()
        session.save()

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("_auth_user_id", self.client.session)
