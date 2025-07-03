import networkx as nx
from django.core.cache import cache

from movies.models import Movie
from config.settings import CACHE_ENABLED, CACHE_TIMEOUT
from interactions.models import Interaction


def get_pagerank_recommendations(user_id, G, top_n=10):
    cache_key = 'pr_scores'

    if not G.nodes:
        return []

    if CACHE_ENABLED:
        pr = cache.get(cache_key )
        if pr is None:
            pr = nx.pagerank(G, weight='weight')
            cache.set(cache_key, pr, timeout=CACHE_TIMEOUT)
    else:
        pr = nx.pagerank(G, weight='weight')

    if not any(node.startswith('movie_') for node in pr):
        return []

    user_movies = set(Interaction.objects.filter(user_id=user_id).values_list('movie_id', flat=True))

    movie_scores = {
        int(node.split('_')[1]): score
        for node, score in pr.items()
        if node.startswith('movie_') and int(node.split('_')[1]) not in user_movies}

    if not movie_scores:
        return []

    top_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    movies = Movie.objects.filter(id__in=[movie_id for movie_id, _ in top_movies]).select_related('actor')

    return [{"movie": movie, "score": movie_scores[movie.id]} for movie in movies]