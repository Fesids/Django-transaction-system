from django.urls import include, path
from . import views

client_url = [
  path('/', views.ClientGetAllView.as_view(), name='user_get_all'),
  path('/create', views.ClientCreateView.as_view(), name='client_create'),
  path('/update/<int:resource_id>', views.ClientUpdateView.as_view(), name="client_update"),
  path('/id/<int:resource_id>', views.ClientGetView.as_view(), name='client_get_one'),
  path("/remove/<int:resource_id>", views.ClientRemoveView.as_view(),
       name="client_remove")
]

client_api_urlpatterns = [
  path('clients', include(client_url))
]