# thumbnailer/urls.py
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
  path('experiments/', views.experiment_list, name='experiment_list'),
  path('experiments/upload/', views.upload_experiment, name='upload_experiment'),
  path('experiments/<int:pk>/', views.delete_experiment, name='delete_experiment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
