from django.urls import path
from . import views
from .views import create_superuser
urlpatterns = [
    path('', views.home, name='home'),
    path("create-superuser/", create_superuser),
    path('fill/', views.fill_form, name='fill_form'),
    path('review/', views.review_person, name='review_person'),
    path('export/', views.export_excel, name='export_excel'),

]
