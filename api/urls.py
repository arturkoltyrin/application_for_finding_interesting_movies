from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (ActorViewSet, GenreViewSet, InteractionViewSet,
                       MovieViewSet, UserRegisterView, UserViewSet,
                       get_collaborative_recommendations,
                       get_knn_recommendations, get_pagerank_recommendations,
                       get_statistics_api)

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("movies", MovieViewSet)
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("interactions", InteractionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "login/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="refresh",
    ),
    path(
        "users/me/",
        UserViewSet.as_view({"get": "me", "put": "me", "patch": "me"}),
        name="user-me",
    ),
    path(
        "users/<int:pk>/block/",
        UserViewSet.as_view({"post": "block"}),
        name="user-block",
    ),
    path(
        "users/me/pagerank/",
        get_pagerank_recommendations,
        name="get-my-pr-recommendations",
    ),
    path(
        "users/me/collaborative/",
        get_collaborative_recommendations,
        name="get-my-collaborative-recommendations",
    ),
    path("users/me/knn/", get_knn_recommendations, name="get-my-knn-recommendations"),
    path(
        "recommendations/pagerank/<int:user_id>/",
        get_pagerank_recommendations,
        name="get-pr-recommendations",
    ),
    path(
        "recommendations/collaborative/<int:user_id>/",
        get_collaborative_recommendations,
        name="get-recommendations",
    ),
    path(
        "recommendations/knn/<int:user_id>/",
        get_knn_recommendations,
        name="get-knn-recommendations",
    ),
    path("statistics/", get_statistics_api, name="statistics"),
]
