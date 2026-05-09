"""
Custom pagination class for DRF with metadata.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class with metadata.
    
    Features:
    - Configurable page size
    - Client can override page size
    - Includes metadata: total_pages, current_page, total_items
    """
    page_size = 10
    page_size_query_param = "page_size"
    page_size_query_description = "Number of results per page"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Return paginated response with metadata.
        """
        return Response({
            "success": True,
            "data": {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
                "pagination": {
                    "total_items": self.page.paginator.count,
                    "total_pages": self.page.paginator.num_pages,
                    "current_page": self.page.number,
                    "page_size": self.page_size,
                }
            }
        })
