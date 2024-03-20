from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.http import JsonResponse

class APIFormatException:
	def handle_format_exception(self, exception):
		try:
			if hasattr(exception, 'to_dict') and callable(exception.to_dict):
				error_data = exception.to_dict()
			else:
				error_data = str(exception)
		except Exception as e:
			error_data = str(e)
		return error_data

class APIResponseFormat:
    def handle_created_response(self, status_code="20001", message_code="CREATED", description="The request was successfully", response={}, http_status=status.HTTP_201_CREATED, pagination={}):
        response = {
			"status_code": status_code,
			'message_code': message_code,
			"description": description,
			'data': response,
		}
        
        return JsonResponse(response, status=http_status)
    
    
    def handle_success_response(self, status_code="20000", message_code="SUCCESS", description="The request was successfully", response={}, http_status=status.HTTP_200_OK, pagination={}):
        if pagination != {}:
            response = {
				"status_code": status_code,
				'message_code': message_code,
				"description": description,
				'data': response,
				'pagination':pagination
			}
        else:
            response = {
				"status_code": status_code,
				'message_code': message_code,
				"description": description,
				'data': response,
			}
        return JsonResponse(response, status=http_status)
    
    def handle_error_response(self, status_code="40000", message_code="BAD_REQUEST", description="Error response", response=None, http_status=status.HTTP_400_BAD_REQUEST, exception=None):
        try:
            error_data = self.handle_format_exception(exception)
        except:
            error_data = str(exception)
        response = {
				"status_code": status_code,
				"message_code": message_code,
				"description": description,
				"data": response,
				"error": error_data if exception else None
		}
        return JsonResponse(response, status=http_status)

class APIResponseView(APIView,  APIFormatException, APIResponseFormat):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)


class PaginationAPIResponse(ListAPIView, APIFormatException, APIResponseFormat):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
class CustomPagination(PageNumberPagination, APIResponseView):
	page = DEFAULT_PAGE
	page_size = DEFAULT_PAGE_SIZE
	page_size_query_param = 'limit'
 
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
  
	def get_paginated_response(self, data=None, status_code="20000", message_code="SUCCESS", message="The request process success"):
		try:
			response = {
				"status_code": status_code,
				"message_code": message_code,
				"message": message,
				"data": data,
				"pagination": {
					"links": {
						"next": self.get_next_link(),
						"previous": self.get_previous_link()
					},
					"total": self.page.paginator.count,
					"page": int(self.request.GET.get("page", DEFAULT_PAGE)),
					"page_size": int(self.request.GET.get("limit", self.page_size))
				}
				}
			return JsonResponse(response, status=status.HTTP_200_OK)
		except Exception as exception:
			response ={
				"status_code": "400001",
				"message_code": "Error",
				"message": "The request failed.",
				"data": [],
				"pagination": {
					"links": {
							"next": self.get_next_link(),
							"previous": self.get_previous_link()
						},
				"total": self.page.paginator.count,
				"page": int(self.request.GET.get("page", DEFAULT_PAGE)),
				"page_size": int(self.request.GET.get("limit", self.page_size))
				}
			}
			return JsonResponse(response, status=status.HTTP_200_OK)