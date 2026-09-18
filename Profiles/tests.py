from django.test import TestCase, Client
from django.contrib.auth.models import User
from Profiles.models import Profile
from Profiles.forms import RegistrationForm


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='hero', password='pass1234')
        self.profile, _ = Profile.objects.get_or_create(user=self.user)

    def test_level_calculated_from_experience(self):
        """Уровень = experience // 100"""
        self.profile.experience = 250
        self.assertEqual(self.profile.level, 2)

    def test_task_achievement_50(self):
        """50 заданий — Легенда"""
        self.profile.completed_tasks = 50
        self.assertIn('Легенда', self.profile.task_achievement)

    def test_next_level_exp(self):
        """Опыт до следующего уровня считается правильно"""
        self.profile.experience = 170
        self.assertEqual(self.profile.next_level_exp, 30)


class RegistrationFormTest(TestCase):

    def test_valid_form(self):
        """Корректные данные — форма валидна"""
        form = RegistrationForm(data={
            'username': 'paladin1',
            'email': 'paladin@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'character_class': 'paladin',
        })
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        """Разные пароли — форма невалидна"""
        form = RegistrationForm(data={
            'username': 'paladin2',
            'email': 'p@example.com',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass999!',
            'character_class': 'mage',
        })
        self.assertFalse(form.is_valid())

    def test_save_creates_profile_with_class(self):
        """После сохранения у пользователя есть профиль с нужным классом"""
        form = RegistrationForm(data={
            'username': 'ranger1',
            'email': 'r@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'character_class': 'ranger',
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.profile.character_class, 'ranger')


class ProfileViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass1234')
        Profile.objects.get_or_create(user=self.user)

    def test_profile_authenticated_returns_200(self):
        """Залогиненный получает страницу профиля"""
        self.client.login(username='tester', password='pass1234')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_public_profile_nonexistent_user(self):
        """Публичный профиль несуществующего пользователя — 404"""
        response = self.client.get('/profile/nobody_exists_xyz/')
        self.assertEqual(response.status_code, 404)
