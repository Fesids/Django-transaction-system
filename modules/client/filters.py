from django_filters import FilterSet, CharFilter, DateFilter
from datetime import datetime
from modules.client.models import Client


class ClientFilter(FilterSet):
  name = CharFilter(field_name='name', lookup_expr='iexact')
  CPF = CharFilter(field_name='CPF', lookup_expr='iexact')
  email = CharFilter(field_name='email', lookup_expr='email')
  created_at = CharFilter(method='filter_created_at_iso')
  updated_at = CharFilter(method='filter_updated_at_iso')
  
  class Meta:
    model = Client
    fields = [
      'name',
      'CPF',
      'email',
      'created_at',
      'updated_at'
    ]
    
  def filter_created_at_iso(self, queryset, name, value):
    from datetime import datetime
    iso_datetime = datetime.fromisoformat(value)
    return queryset.filter(created_at_date=iso_datetime.date())
  
  def filter_updated_at_iso(self, queryset, name, value):
    from datetime import datetime
    iso_datetime = datetime.fromisoformat(value)
    return queryset.filter(updated_at__date=iso_datetime.date())
     
    