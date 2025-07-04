import random

from django.core.management import BaseCommand
from django.db.models import Avg
from django.utils import timezone

from movies.models import Genre, Actor, Movie
from interactions.models import Interaction
from users.models import User


class Command(BaseCommand):
    help = 'Generates test data for recommendation algorithms'
    base_genres = []

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_movies',
            type=int,
            default=100,
            help='Number of movies to create (default: 100)',
        )
        parser.add_argument(
            '--num_users',
            type=int,
            default=50,
            help='Number of users to create (default: 50)',
        )
        parser.add_argument(
            '--num_actors',
            type=int,
            default=20,
            help='Number of users to create (default: 50)',
        )

    def handle(self, *args, **options):
        num_movies = options['num_movies']
        num_users = options['num_users']
        num_actors = options['num_actors']

        self.stdout.write('Deleting old data...')
        Genre.objects.all().delete()
        Actor.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Interaction.objects.all().delete()

        self.stdout.write('Creating genres...')
        genres = [
            'Детективы', 'Новеллы', 'Наука',
            'Исторические', 'Фантастика', 'Триллеры']

        genre_objects = [Genre(name=name) for name in genres]
        Genre.objects.bulk_create(genre_objects)
        genres = Genre.objects.all()
        self.stdout.write(f'Создание {num_actors} актеров...')
        actors = [Actor(name=f'Actor {i}', surname=f'Актер {i} Фамилия') for i in range(1, num_actors + 1)]
        Actor.objects.bulk_create(actors)
        actors = Actor.objects.all()
        self.stdout.write(f'Создание {num_movies} Фильмов...')
        movies = []
        for i in range(1, num_movies + 1):
            movie = Movie(
                title=f'Фильм {i}',
                actor=random.choice(actors),
                description=f'Описание фильма {i}',
                publish_date=timezone.now().date())
            movies.append(movie)
        Movie.objects.bulk_create(movies)
        self.stdout.write('Добавить жанр...')
        all_movies = Movie.objects.all()
        for movie in all_movies:
            movie.genres.add(*random.sample(list(genres), k=random.randint(1, 3)))

        self.stdout.write('Создать пользователя...')
        for i in range(1, num_users + 1):
            user = User.objects.create_user(
                email=f'user{i}@example.com',
                password='testpass123'
            )
            user.preferred_genres.add(*random.sample(list(genres), k=random.randint(2, 4)))

        self.stdout.write('Создание взаимодействия...')
        interactions = []
        all_movies = list(Movie.objects.all())
        all_users = User.objects.all()

        for user in all_users:
            user_preferred_genres = user.preferred_genres.all()
            preferred_movies = Movie.objects.filter(genres__in=user_preferred_genres).distinct()
            other_movies = Movie.objects.exclude(genres__in=user_preferred_genres).distinct()

            num_interactions = random.randint(10, 24)
            num_preferred = int(num_interactions * 0.7)
            num_other = num_interactions - num_preferred

            try:
                preferred_sample = random.sample(list(preferred_movies), num_preferred)
                other_sample = random.sample(list(other_movies), num_other)
            except ValueError:
                continue

            for movie in preferred_sample + other_sample:
                rating = random.choices(
                    [None, round(random.uniform(3.0, 5.0), 1)],
                    weights=[0.3, 0.7]
                )[0]

                interactions.append(Interaction(
                    user=user,
                    movie=movie,
                    rating=rating,
                ))

        Interaction.objects.bulk_create(interactions)

        self.stdout.write('Обновление средних оценок...')
        movies_to_update = Movie.objects.filter(interaction__isnull=False).distinct()
        for movie in movies_to_update:
            movie.average_rating = Interaction.objects.filter(movie=movie).aggregate(
                Avg('rating')
            )['rating__avg'] or 0.0
            movie.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created:\n'
            f'- {Genre.objects.count()} жанры\n'
            f'- {Actor.objects.count()} актеры\n'
            f'- {Movie.objects.count()} фильмы\n'
            f'- {User.objects.count()} пользователи\n'
            f'- {Interaction.objects.count()} взаимодействие'))