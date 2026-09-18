<div align="center">

# ⚔️ GymQuest Kingdom

**Фитнес-трекер в стиле средневековой MMORPG**

Создай героя, вступи в клан, выполняйте задания вместе — и поднимайся в таблице лидеров.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)

Главная страница целиком:
<img width="1919" height="953" alt="image" src="https://github.com/user-attachments/assets/3a84e014-85ca-4d33-87ef-7a5bd54c50aa" />


</div>

---

## 📜 О проекте

GymQuest Kingdom превращает тренировки в ролевую игру. Каждый пользователь — герой одного из четырёх классов. Герои объединяются в кланы, берут общие задания из журнала клана и получают за них опыт. Опыт повышает уровень героя, число выполненных заданий — его ранг, а таблица лидеров показывает, кто сильнейший в королевстве.

## ✨ Возможности

### 🧙 Герои и классы

При регистрации игрок выбирает один из четырёх классов. Класс отражает, на чём герой делает упор в тренировках, и отображается в профиле и в рейтинге.

| Класс | Упор |
|---|---|
| 🏹 Рейнджер | кардио и ноги |
| 🛡️ Паладин | грудь и жим |
| ⚔️ Варвар | спина и сила |
| 🧙 Маг | кор и мобильность |

<img width="583" height="742" alt="image" src="https://github.com/user-attachments/assets/b7bdbb74-d79d-4bf5-a7b6-5d389fe1962e" />


### 🏰 Кланы

- создание собственного клана (игрок может состоять только в одном клане);
- уникальный 8-символьный код приглашения генерируется автоматически;
- вступление в клан из списка или по коду;
- выход из клана и роспуск клана владельцем;
- при создании клана в журнал сразу добавляются три стартовых задания.


<img width="1920" height="951" alt="image" src="https://github.com/user-attachments/assets/de403d62-dded-43e7-85da-e67e20a30903" />


### 📋 Журнал заданий клана

- задания разложены по трём категориям: **доступные → в процессе → завершённые**;
- любой участник клана может создать задание с описанием, наградой (1–1000 XP) и дедлайном;
- видно, кто взялся за задание и кто его завершил;
- опыт за выполненное задание получают все его участники.


<img width="1919" height="951" alt="image" src="https://github.com/user-attachments/assets/d37f41fe-4a0c-447e-ad74-acd79d461c1c" />


<img width="556" height="609" alt="image" src="https://github.com/user-attachments/assets/43691ae7-a4e1-4e33-9348-8c941774432d" />


### 📈 Опыт, уровни и ранги

- каждые **100 XP** — новый уровень;
- полоса прогресса в профиле показывает, сколько опыта осталось до следующего уровня;
- ранг искателя зависит от количества выполненных заданий:

| Ранг | Заданий |
|---|---|
| 🌱 Начинающий | 0 |
| 🗡️ Новобранец | 5 |
| 🛡️ Опытный искатель | 10 |
| ⚔️ Ветеран квестов | 20 |
| 🏆 Легенда подземелий | 50 |

### 👤 Профиль героя

- загрузка аватара (jpg, jpeg, png, gif);
- отображаемое имя, e-mail, домашняя локация, главная цель, девиз и любимое «подземелье»;
- смена класса;
- история последних выполненных заданий;
- публичный профиль любого героя по адресу `/profile/<username>/`.

Личный профиль

<img width="1920" height="951" alt="image" src="https://github.com/user-attachments/assets/e251232e-d476-42a5-a3e9-0d94a4952095" />

Публичный профиль другого игрока

<img width="1920" height="948" alt="image" src="https://github.com/user-attachments/assets/eaee91e3-5ac4-4cbb-93bc-5cd25f2e6517" />

### 🏆 Таблица лидеров

Топ-5 героев по опыту с медалями за первые три места и личное место текущего игрока в общем зачёте.

<img width="1920" height="951" alt="image" src="https://github.com/user-attachments/assets/658101cc-e888-4453-b21f-a14a307719b9" />


---

## 🛠 Технологии

- **Backend:** Python 3.12+, Django 6.0
- **База данных:** SQLite (для разработки)
- **Frontend:** Django Templates, Bootstrap 5.3, собственные стили
- **Изображения:** Pillow (загрузка аватаров)
- **Документация:** Sphinx + Read the Docs theme

## 🚀 Запуск локально

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<your-username>/GymQuest.git
cd GymQuest

# 2. Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать файл с переменными окружения
cp .env.example .env              # Windows: copy .env.example .env
# и вписать в .env свой DJANGO_SECRET_KEY (команда для генерации — ниже)

# 5. Применить миграции и создать администратора
python manage.py migrate
python manage.py createsuperuser

# 6. Запустить сервер
python manage.py runserver
```

Сайт откроется на http://127.0.0.1:8000/, админка — на http://127.0.0.1:8000/admin/.

Сгенерировать секретный ключ:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Переменные окружения

| Переменная | Описание | Пример |
|---|---|---|
| `DJANGO_SECRET_KEY` | секретный ключ Django | `сгенерированная-строка` |
| `DJANGO_DEBUG` | режим отладки | `True` |
| `DJANGO_ALLOWED_HOSTS` | разрешённые хосты через запятую | `127.0.0.1,localhost` |

## 🧪 Тесты

```bash
python manage.py test
```

Тесты покрывают модели, формы и основные представления приложений `Profiles`, `clans` и `Tasks`.

## 📚 Документация

Документация кода собирается Sphinx:

```bash
pip install sphinx sphinx-rtd-theme
cd docs
make html                         # Windows: make.bat html
```

После сборки она доступна на сайте по адресу `/docs/`.

## 🗂 Структура проекта

```
GymQuest/
├── GymQuest/          # настройки проекта, корневые urls, главная и рейтинг
│   └── templates/     # base.html, index.html, rating.html
├── Profiles/          # регистрация, вход, профиль, аватар, публичные профили
├── clans/             # кланы: создание, вступление, коды приглашений
├── Tasks/             # задания клана и начисление опыта
├── static/            # общие стили
├── media/             # загруженные аватары (не хранится в git)
├── docs/              # исходники документации Sphinx
└── manage.py
```
