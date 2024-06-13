from rest_framework import pagination, viewsets, status
from rest_framework.response import Response
from .models import Currency
from .serializers import CurrencySerializers
from rest_framework.filters import SearchFilter

class CustomPagination(pagination.PageNumberPagination):
    max_page_size = '15'
    page_size_query_param = 'page_size'
    page_size = '15'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.filter(is_active=True)
    serializer_class = CurrencySerializers
    filter_backends = [SearchFilter]
    search_fields = ['country', 'id', 'name']
    