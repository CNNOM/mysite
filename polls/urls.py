from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('poll/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('poll/<int:poll_id>/success/', views.vote_success, name='vote_success'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('poll/<int:poll_id>/results/', views.poll_results, name='poll_results'),
]