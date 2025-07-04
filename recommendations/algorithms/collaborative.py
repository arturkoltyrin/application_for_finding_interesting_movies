import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from movies.models import Movie
from interactions.models import Interaction


def user_based_collaborative_filtering(user_id, k=5, top_n=10):
    interactions = Interaction.objects.all()
    users = list(set(interactions.values_list('user_id', flat=True)))
    movies = list(set(interactions.values_list('movie_id', flat=True)))
    if not users or movies:
        return []

    user_movie_matrix = np.zeros((len(users), len(movies)))
    user_to_index = {user_id: i for i, user_id in enumerate(users)}
    movie_to_index = {movie_id: i for i, movie_id in enumerate(movies)}

    if user_id not in user_to_index:
        return []

    for interaction in interactions:
        user_idx = user_to_index[interaction.user_id]
        movie_idx = movie_to_index[interaction.movie_id]
        user_movie_matrix[user_idx, movie_idx] = interaction.rating or 0.0

    user_similarity = cosine_similarity(user_movie_matrix)
    target_user_idx = user_to_index[user_id]
    similar_users = np.argsort(user_similarity[target_user_idx])[-k - 1:-1][::-1]
    predicted_ratings = np.zeros(len(movies))
    for movie_idx in range(len(movies)):
        if user_movie_matrix[target_user_idx, movie_idx] == 0:
            numerator = sum(user_similarity[target_user_idx, user_idx] * user_movie_matrix[user_idx, movie_idx]
                            for user_idx in similar_users if user_movie_matrix[user_idx, movie_idx] != 0)
            denominator = sum(user_similarity[target_user_idx, user_idx] for user_idx in similar_users)

            if denominator:
                predicted_ratings[movie_idx] = numerator / denominator

    recommended_movies_indices = np.argsort(predicted_ratings)[-top_n:][::-1]
    recommended_movies_ids = [movies[idx] for idx in recommended_movies_indices]
    movies_queryset = Movie.objects.filter(id__in=recommended_movies_ids).select_related('actor')
    movies_dict = {movie.id: movie for movie in movies_queryset}

    if not movies_dict:
        return []

    recommendations = [
        {
            "movie": movies_dict[movie_id],
            "predicted_rating": predicted_ratings[movies.index(movie_id)]
        }
        for movie_id in recommended_movies_ids
    ]

    return recommendations