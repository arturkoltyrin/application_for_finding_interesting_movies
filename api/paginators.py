from rest_framework.pagination import PageNumberPagination


class GenrePaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class ActorPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class MoviePaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


class UserPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


class InteractionPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 20
