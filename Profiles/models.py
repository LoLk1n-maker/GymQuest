from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Profile(models.Model):
    # Связь с пользователем
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # ---- Базовые поля из профиля ----
    # Класс персонажа
    class CharacterClass(models.TextChoices):
        RANGER = 'ranger', '🏹 Рейнджер (кардио и ноги)'
        PALADIN = 'paladin', '🛡️ Паладин (грудь и жим)'
        BARBARIAN = 'barbarian', '⚔️ Варвар (спина и сила)'
        MAGE = 'mage', '🧙 Маг (кор и мобильность)'


    character_class = models.CharField(
        max_length=20,
        choices=CharacterClass.choices,
        default=CharacterClass.PALADIN,
        verbose_name='Класс'
    )

    # Игровые параметры

    @property
    def level(self):
        return self.experience // 100

    # rank = models.CharField(max_length=100, default='Серебряный крестоносец', verbose_name='Ранг')

    experience = models.PositiveIntegerField(default=0, verbose_name='Опыт')
    # Для процента до следующего уровня можно вычислять, но для простоты храним текущий опыт и требуемый

    # ---- Настройки и предпочтения ----
    # Предпочтения (можно хранить как текстовые поля)
    favorite_dungeon = models.CharField(max_length=100, blank=True, default='', verbose_name='Любимое подземелье')

    # Профиль
    home_location = models.CharField(max_length=100, blank=True, verbose_name='Домашняя локация')
    main_goal = models.CharField(max_length=200, blank=True, verbose_name='Главная цель')
    bio = models.TextField(blank=True, verbose_name='Биография / девиз')

    display_name = models.CharField(max_length=150, blank=True, verbose_name='Отображаемое имя')

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        verbose_name='Аватар'
    )

    # ---- Достижения ----
    completed_tasks = models.PositiveIntegerField(default=0, verbose_name='Выполнено заданий')

    @property
    def next_level(self):
        return self.level + 1

    @property
    def next_level_exp(self):
        return 100 - (self.experience % 100)


    def __str__(self):
        return f'Профиль {self.user.username}'

    @property
    def task_achievement(self):
        count = self.completed_tasks

        if count >= 50:
            return "🏆 Легенда подземелий(>50 заданий)"
        elif count >= 20:
            return "⚔️ Ветеран квестов(>20 заданий)"
        elif count >= 10:
            return "🛡️ Опытный искатель(>10 заданий)"
        elif count >= 5:
            return "🗡️ Новобранец(>5 заданий)"
        else:
            return "🌱 Начинающий"


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


