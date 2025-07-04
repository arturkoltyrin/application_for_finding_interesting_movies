import numpy as np
from django.core.cache import cache
from sklearn.metrics.pairwise import cosine_similarity

from config.settings import CACHE_ENABLED, CACHE_TIMEOUT
from interactions.models import Interaction
from users.models import User


def find_k_nearest_neighbors(user_id, k=5):
    cache_key = f"user_neighbors_{user_id}_{k}"

    if CACHE_ENABLED:
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

    interactions = Interaction.objects.all()
    users = list(set(interactions.values_list('user_id', flat=True)))
    movies = list(set(interactions.values_list('movie_id', flat=True)))

    if not users or not movies:
        return []

    # Filling the matrix
    user_to_index = {user_id: i for i, user_id in enumerate(users)}
    movie_to_index = {movie_id: i for i, movie_id in enumerate(movies)}

    if user_id not in user_to_index:
        return []
    user_movie_matrix = np.zeros((len(users), len(movies)))

    for interaction in interactions:
        user_idx = user_to_index[interaction.user_id]
        movie_idx = movie_to_index[interaction.movie_id]
        user_movie_matrix[user_idx, movie_idx] = interaction.rating or 0.0

    user_similarity = cosine_similarity(user_movie_matrix)

    target_user_idx = user_to_index[user_id]
    nearest_neighbors = np.argsort(user_similarity[target_user_idx])[-k - 1:-1][::-1]

    if not nearest_neighbors.size:
        return []

    result = User.objects.filter(id__in=[users[idx] for idx in nearest_neighbors])

    if CACHE_ENABLED:
        cache.set(cache_key, result, timeout=CACHE_TIMEOUT)

    return result