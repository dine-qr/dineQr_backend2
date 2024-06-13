from rest_framework import pagination, viewsets
from rest_framework.response import Response
from .models import Otp
from .serializers import OtpSerializers

class CustomPagination(pagination.PageNumberPagination):
    max_page_size = '15'
    page_query_param = 'page_size'
    page_size = '15'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
    
class OtpViewSet(viewsets.ModelViewSet):
    queryset = Otp.objects.all()
    serializer_class = OtpSerializers
    pagination_class = CustomPagination
    