
from django.contrib import admin
from django.urls import path, include
from modules.client.urls import client_api_urlpatterns

api_urlpatterns = [
    path('', include(client_api_urlpatterns)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns))
]
