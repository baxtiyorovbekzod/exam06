from django.urls import path
from .views import *

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),
    path('create/', StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/edit/', StudentEditView.as_view(), name='student_edit'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
]