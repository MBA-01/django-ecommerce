from django.urls import path
from .admin import DomainAdmin
from . import views

urlpatterns = [
    path('scrape/', views.scrape_domain, name='scrape_domain'),
    path('validate/<int:pk>/', views.validate_product, name='validate_product'),
    path('modify/<int:pk>/', views.modify_product, name='modify_product'),
    path('cancel/<int:pk>/', views.cancel_product, name='cancel_product'),
    path('import/<int:pk>/', DomainAdmin.import_domain, name='scraper_import_domain'),


]
