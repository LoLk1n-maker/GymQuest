from django.test import TestCase, Client
from django.contrib.auth.models import User
from Tasks.models import ClanTask, ClanTaskCompletion
from Tasks.forms import ClanTaskForm
from clans.models import Clan
from Profiles.models import Profile


class ClanTaskFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='hero', password='pass1234')
        self.clan = Clan.objects.create(name='Тест', owner=self.user)

    def test_task_default_status_is_todo(self):
        """Новое задание по умолчанию имеет статус todo"""
        task = ClanTask.objects.create(clan=self.clan, title='Тест', xp_reward=50)
        self.assertEqual(task.status, 'todo')

    def test_valid_task_form(self):
        """Форма с заголовком валидна"""
        form = ClanTaskForm(data={'title': 'Сделать 50 отжиманий', 'xp_reward': 100, 'status': 'todo'})
        self.assertTrue(form.is_valid())


class TaskViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='hero', password='pass1234')
        self.other = User.objects.create_user(username='stranger', password='pass1234')
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.clan = Clan.objects.create(name='Клан', owner=self.user)
        self.clan.members.add(self.user)
        self.task = ClanTask.objects.create(clan=self.clan, title='Задание', xp_reward=100, status='todo')

    def test_clan_tasks_with_clan(self):
        """Участник клана видит задания"""
        self.client.login(username='hero', password='pass1234')
        response = self.client.get('/quests/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('tasks_todo', response.context)

    def test_start_task_adds_participant(self):
        """start_task добавляет пользователя в участники и ставит статус doing"""
        self.client.login(username='hero', password='pass1234')
        self.client.post(f'/quests/tasks/{self.task.id}/start/')
        self.task.refresh_from_db()
        self.assertIn(self.user, self.task.participants.all())
        self.assertEqual(self.task.status, 'doing')

    def test_complete_task_awards_xp(self):
        """Завершение задания начисляет XP участникам"""
        self.task.participants.add(self.user)
        self.task.status = 'doing'
        self.task.save()
        old_exp = self.profile.experience
        self.client.login(username='hero', password='pass1234')
        self.client.post(f'/quests/tasks/{self.task.id}/complete/')
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.experience, old_exp + self.task.xp_reward)

    def test_complete_already_done_task(self):
        """Повторное завершение уже выполненного задания не даёт XP дважды"""
        self.task.participants.add(self.user)
        self.task.status = 'done'
        self.task.save()
        exp_before = self.profile.experience
        self.client.login(username='hero', password='pass1234')
        self.client.post(f'/quests/tasks/{self.task.id}/complete/')
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.experience, exp_before)
