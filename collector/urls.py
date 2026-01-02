from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fill/', views.fill_form, name='fill_form'),
    path('review/', views.review_person, name='review_person'),
]