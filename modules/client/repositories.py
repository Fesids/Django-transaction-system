from core.utils.exception_utils import AppExceptionHelper, AppRepositoryException
from .models import Client
from django.db import transaction


class ClientRepository(AppExceptionHelper):
  
  def client_repo_get_all(self, sorting=None):
    try:
      if not sorting:
        return Client.objects.all()
      else:
        return Client.objects.all().order_by(sorting)
    except Client.DoesNotExist as exception:
      self.raise_repository_instance_not_found_exception(
        field='Client',
        exception_type='ClientNotFound'
      )
      
    except Exception as exception:
      raise AppRepositoryException(
        field='Client',
        message='Retrieve clients list process failed',
        error_info="The list is empty or dosn't exist",
        child_error=exception
      )
  
  def client_repo_get_one(self, resource_id):
    try:
      return Client.objects.get(id=resource_id)
    except Client.DoesNotExist as exception:
      self.raise_repository_instance_not_found_exception(field='Client', exception_type='ClientNotFound')
    except Exception as exception:
      raise AppRepositoryException(
        field='Client',
        message='Retrieve client process failed',
        error_info=f'Retrieve Cliente where resource id : {resource_id} failed',
        child_error=exception
      )
  
  @transaction.atomic
  def client_repo_create(self, client):
    with transaction.atomic():
      try:
        return Client.objects.create(**client)
      except Exception as exception:
        raise AppRepositoryException(
          field='Client',
          message='create client proccess failed',
          error_info=f'Create client process suffered an error',
          child_error=exception
        )
  
  @transaction.atomic
  def client_repo_remove(self, resource_id):
    with transaction.atomic():
      try:
        client = self.client_repo_get_one(resource_id)
        client.delete()
        return True

      except Client.DoesNotExist as exception:
        self.raise_repository_instance_not_found_exception(
          field='Client',
          exception_type='ClientNotFound'
        )
        
      except Exception as exception:
        raise AppRepositoryException(
          field='Client',
          message='Delete client process failed',
          error_info=f"Delete client where id : {resource_id} failed",
          child_error=exception
        )
        
  @transaction.atomic
  def client_repo_update(self, instance, validated_data):
    with transaction.atomic():
      try:
        instance.name = validated_data.get('name', instance.name)
        instance.tier = validated_data.get('tier', instance.tier)
        instance.CPF = validated_data.get('CPF', instance.CPF)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.company_id = validated_data.get('company_id', instance.company_id)
        instance.save()
        return instance
      except Exception as exception:
        raise AppRepositoryException(
          field="Client",
          message="Update client process failed",
          error_info=f"Update client failed",
          child_error=exception
        )  