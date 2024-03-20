from django.shortcuts import render
from core.utils.base_view_utils import APIResponseView, CustomPagination, PaginationAPIResponse
from core.utils.exception_utils import AppRequestException
from modules.client.repositories import ClientRepository
from modules.client.serializers import ClientSerializer, ClientGetSerializer, ClientUpdateSerializer
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
from modules.client.filters import ClientFilter
# Create your views here.


class ClientUpdateView(APIResponseView, ClientRepository):
  serializer_class = ClientUpdateSerializer
  queryset = None
  
  def perform_update_logic(self, resource_id, payload):
    try:
      instance = self.client_repo_get_one(resource_id)
      serializer = self.serializer_class
      if serializer.is_valid(raise_exception=True):
        validated_data = serializer.validated_data
        updated = self.client_repo_update(instance, validated_data)
        re_serialize = self.serializer_class(updated)
        response = re_serialize.data
        return response
    except Exception as exception:
      raise AppRequestException(
        field="Client",
        message="The Client update process Failed",
        error_info="The perform update logic process failed",
        child_error=exception
      )
      
  def put(self, request, resource_id):
    try:
      request_data = request.data
      response = self.perform_update_logic(resource_id, request_data)
      
      if response:
        return self.handle_success_response(
          description=f"Update user concluded sucessfully",
          message_code='SUCCESS',
          status_code='200',
          response=response
        )
        
      else:
        return self.handle_error_response(
        exception=None,
        status_code="400",
        message_code="BAD_REQUEST",
        description = f"A Client update one was failure.",
        )
      
    except Exception as exception:
      return self.handle_error_response(
            exception=exception,
            status_code="400",
            message_code="Bad Request",
            description = f"A Client update was failure.",
				)

class ClientRemoveView(APIResponseView, ClientRepository):
  serializer_class = ClientSerializer
  
  def perform_remove_logic(self, resource_id):
    try:
      response = self.client_repo_remove(resource_id)
      return response
    
    except Exception as exception:
      raise AppRequestException(
        field='Client',
        message='Failed to delete client',
        error_info='The process of perform delete logic failed',
        child_error=exception
      )
  
  def delete(self, request, resource_id):
    try:
      response = self.perform_remove_logic(resource_id)
      return self.handle_success_response(
        description=f"Delete client successfully deleted",
        message_code="Success",
        status_code="200",
        response=response
      )
    except Exception as exception:
      return self.handle_error_response(
        exception=exception,
        status_code='400',
        message_code='Bad Request',
        description=f'Delete client process failed.'
        
      )
    
class ClientGetAllView(PaginationAPIResponse, ClientRepository):
  pagination_class = CustomPagination
  serializer_class = ClientSerializer
  queryset = None
  filter_backends = [filters.SearchFilter, DjangoFilterBackend]
  filterset_class = ClientFilter
  
  def perform_get_all_logic(self, sorting):
    try:
      self.queryset = self.client_repo_get_all(sorting=sorting)
      queryset = self.filter_queryset(self.queryset)
      page = self.paginate_queryset(queryset=queryset)
      if page is not None:
        serializer = self.serializer_class(page, many=True)
        response = self.get_paginated_response(data=serializer.data)
        return response
      else:
        serializer = self.get_serializer(queryset, many=True)
        return self.handle_success_response(
          description=f"Get all clients suceded",
          message_code='Success',
          status_code="200",
          response=serializer.data
        )
    except Exception as exception:
      raise AppRequestException(
        field='Client',
        message=f"Failed to perform get all clients logic",
        error_info="The proccess of get all clients was failed",
        child_error=exception
      )
      
  def get(self, request):
    try:
      sort = request.GET.get('sort')
      if sort != None:
        sorting = sort
      else:
        sorting = '-created_at'
      return self.perform_get_all_logic(sorting=sorting)
    except Exception as exception:
      return self.handle_error_response(
        exception=exception,
        status_code='400',
        message_code='Bad Request',
        description=f'Get clients failed'
      )
      
class ClientGetView(APIResponseView):
  
  serializer_class = ClientSerializer
  
  repo = ClientRepository()
  queryset = None
  def perform_get_one_logic(self, resource_id):
    try:
      self.queryset = self.repo.client_repo_get_one(resource_id=resource_id)
      if self.queryset:
         serializer = self.serializer_class(self.queryset, many=False)
         return serializer.data
       
    except Exception as exception:
      raise AppRequestException(
        field="Client",
        message="Failed to get client",
        error_info="The peform get logic process failed",
        child_error=exception
      )
  def get(self, request, resource_id):
    try:
      print(type(resource_id))
      response = self.perform_get_one_logic(resource_id)
      if response:
        return self.handle_success_response(
          description=f'The get client process was concluded successfully.',
          message_code="Success",
          status_code="200",
          response=response
        )
        
      else:
        return self.handle_error_response(
          exception=None,
          status_code="400",
          message_code="Bad Request",
          description=f"Get client process failed"
        )
      
    except Exception as exception:
      return self.handle_error_response(
        exception=exception,
        status_code="400",
        message_code="Bad Request",
        description=f"Get client process failed"
      )
      
class ClientCreateView(APIResponseView):
  
  serializer_class = ClientSerializer
  
  repo = ClientRepository()
  queryset = None
  def perform_create_logic(self, payload):
    
    try:
      serializer = self.serializer_class(data=payload)
      
      if serializer.is_valid(raise_exception=True):
        validated_data = serializer.validated_data
        instance = self.repo.client_repo_create(validated_data)
        re_serialize = self.serializer_class(instance=instance)
        response = re_serialize.data
        return response
      
    except Exception as exception:
      raise AppRequestException(
        field='Client',
        message='Failed to create a new client',
        error_info='The perform logic process failed',
        child_error=exception
      )
        
  def post(self, request):
    try:
      request_data = request.data
      response = self.perform_create_logic(request_data)
      return self.handle_success_response(
        description=f'The creation process was concluded successfuly',
        message_code='SUCCESS',
        status_code='20000',
        response=response
      )
      
    except Exception as exception:
        return self.handle_error_response(
          exception=exception,
          status_code='40000',
          message_code='Bad Request',
          description=f'Create client proccess failed'
        )
        
