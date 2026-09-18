from django.test import TestCase, Client
from django.contrib.auth.models import User
from clans.models import Clan
from clans.forms import ClanCreateForm


class ClanModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='pass1234')

    def test_code_generated_on_save(self):
        """При создании клана автоматически генерируется код"""
        clan = Clan.objects.create(name='Берсерки', owner=self.user)
        self.assertTrue(len(clan.code) > 0)

    def test_valid_form(self):
        """Форма с названием валидна"""
        form = ClanCreateForm(data={'name': 'Охотники'})
        self.assertTrue(form.is_valid())


class ClanViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(username='owner', password='pass1234')
        self.member = User.objects.create_user(username='member', password='pass1234')
        self.clan = Clan.objects.create(name='Тестовый клан', owner=self.owner)
        self.clan.members.add(self.owner)

    def test_clans_view_authenticated(self):
        """Залогиненный видит список кланов"""
        self.client.login(username='owner', password='pass1234')
        response = self.client.get('/clans/')
        self.assertEqual(response.status_code, 200)

    def test_create_clan_creates_with_tasks(self):
        """Создание клана — автоматически добавляются 3 базовых задания"""
        self.client.login(username='member', password='pass1234')
        self.client.post('/clans/create/', {'name': 'Новый клан'})
        new_clan = Clan.objects.filter(owner=self.member).first()
        self.assertIsNotNone(new_clan)
        self.assertEqual(new_clan.tasks.count(), 3)

    def test_join_clan(self):
        """Пользователь вступает в клан"""
        self.client.login(username='member', password='pass1234')
        self.client.post(f'/clans/join/{self.clan.id}/')
        self.assertIn(self.member, self.clan.members.all())

    def test_delete_clan_by_owner(self):
        """Владелец может удалить клан"""
        self.client.login(username='owner', password='pass1234')
        self.client.post(f'/clans/delete/{self.clan.id}/')
        self.assertFalse(Clan.objects.filter(id=self.clan.id).exists())

    def test_delete_clan_by_non_owner_fails(self):
        """Не-владелец не может удалить клан"""
        self.clan.members.add(self.member)
        self.client.login(username='member', password='pass1234')
        self.client.post(f'/clans/delete/{self.clan.id}/')
        self.assertTrue(Clan.objects.filter(id=self.clan.id).exists())
