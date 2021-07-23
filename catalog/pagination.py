from rest_framework.pagination import LimitOffsetPagination 


class CatalogPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 3
    limit_query_param = 'limit'
    offset_query_param = 'offset'

# class CategoryPagination(LimitOffsetPagination):
#     default_limit = 2
#     max_limit = 3
#     limit_query_param = 'limit'
#     offset_query_param = 'offset'