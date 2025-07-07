from django.contrib import admin

from movies.models import Actor, Genre, Movie


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "surname")
    search_fields = (
        "name",
        "surname",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_actor_name",
        "description",
        "cover",
        "get_genres",
        "publish_date",
    )
    list_filter = ("genres",)
    search_fields = ("title", "actor__name", "genres__name")

    def get_actor_name(self, obj):
        return obj.actor.name if obj.actor.name else "No actor"

    get_actor_name.short_description = "Actor"

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = "Genres"
