import networkx as nx

from interactions.models import Interaction
from movies.models import Movie
from users.models import User


def build_user_movie_graph():
    G = nx.Graph()

    for user in User.objects.all():
        G.add_node(f"user_{user.id}", type="user")

    for movie in Movie.objects.all():
        G.add_node(f"movie_{movie.id}", type="movie")

    for interaction in Interaction.objects.select_related("user", "movie"):
        user_node = f"user_{interaction.user.id}"
        movie_node = f"movie_{interaction.movie.id}"
        weight = interaction.rating if interaction.rating else 0.5
        G.add_edge(user_node, movie_node, weight=weight)

    return G
