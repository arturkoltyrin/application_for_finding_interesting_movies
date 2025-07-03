from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


NULLABLE = {
    'blank': True,
    'null': True}

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE)
    description = models.TextField(**NULLABLE)
    cover = models.ImageField(
        upload_to='movies/',
        **NULLABLE)
    genres = models.ManyToManyField('Genre')
    publish_date = models.DateField(auto_now_add=True)
    average_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title
