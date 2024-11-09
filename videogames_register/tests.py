from django.contrib.auth.models import User
from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse
from django.contrib.auth.models import Permission
from .models import Genre, VideoGame
from django.utils import timezone
from .forms import VideogameForm

# Create your tests here.


class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(title='Action')

    def test_genre_creation(self):
        self.assertTrue(isinstance(self.genre, Genre))
        self.assertEqual(self.genre.title, 'Action')


class VideoGameModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(title="Adventure")
        self.videogame = VideoGame.objects.create(
            title="The Legend of Zelda",
            release_date=timezone.now().date(),
            description="An epic adventure game.",
            genre=self.genre
        )

    def test_videogame_creation(self):
        self.assertEqual(self.videogame.title, "The Legend of Zelda")
        self.assertEqual(self.videogame.genre.title, "Adventure")
        self.assertTrue(isinstance(self.videogame, VideoGame))



class VideogameFormTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(title="Strategy")

    def test_valid_form(self):
        data = {
            'title': 'Chess Master',
            'release_date': '2023-01-01',
            'description': 'A strategy game.',
            'genre': self.genre

        }
        form = VideogameForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'title': '',
            'release_date': '',
            'description': '',
            #genre is missing intentionally to make the form invalid

        }
        form = VideogameForm(data=data)
        self.assertFalse(form.is_valid())


class VideogameListViewTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username = 'marco', password = 'test')
        self.client.login(username='marco', password='test')

        permission = Permission.objects.get(codename='view_videogame')
        self.user.user_permissions.add(permission)


        self.genre = Genre.objects.create(title='Adventure')
        self.videogame = VideoGame.objects.create(
            title="The Legend of Zelda",
            release_date=timezone.now().date(),
            description="An epic adventure game.",
            genre=self.genre
        )

    def test_videogame_list_view(self):

        response = self.client.get(reverse('videogame_list'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'videogames_register/videogame_list.html')

        self.assertContains(response, self.videogame.title)
        self.assertContains(response, self.videogame.genre.title)
        self.assertContains(response, self.videogame.description)

class VideogameFormViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username = 'tester', password = 'test')
        self.client.login(username='tester', password='test')
        user.user_permissions.add(Permission.objects.get(codename='view_videogame'))
        user.user_permissions.add(Permission.objects.get(codename='add_videogame'))



        self.genre = Genre.objects.create(title='Adventure')
        self.videogame = VideoGame.objects.create(
            title="The Legend of Zelda",
            release_date=timezone.now().date(),
            description="An epic adventure game.",
            genre=self.genre
        )


    def test_videogame_view_form(self):
        response = self.client.get(reverse('videogame_insert'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'videogames_register/videogame_form.html')

        response = self.client.post(reverse('videogame_insert'), {
            'title': 'Adventure',
            'genre': self.genre.id,
            'description': 'A strategy game.',
            'release_date': '2023-01-01',
        })

        self.assertEqual(response.status_code, 302)

