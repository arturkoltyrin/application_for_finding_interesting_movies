from django.core.exceptions import PermissionDenied
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

import movies.models
import users.models


NULLABLE = {
    'blank': True,
    'null': True}


class Interaction(models.Model):
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE)
    movie = models.ForeignKey(movies.models.Movie, on_delete=models.CASCADE)
    rating = models.FloatField(
        **NULLABLE,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'
        unique_together = (('user', 'movie'),)
        indexes = [
            models.Index(fields=['user', 'movie'])
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            original = Interaction.objects.get(pk=self.pk)
            if original.user != self.user:
                raise PermissionDenied("You can't change someone else's interactions.")
        super().save(*args, **kwargs)
        self.movie.average_rating = Interaction.objects.filter(movie=self.movie).aggregate(
            Avg('rating')
        )['rating__avg'] or 0.0

        self.movie.save()
