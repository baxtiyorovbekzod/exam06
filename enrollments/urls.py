from django.urls import path
from .views import *

urlpatterns = [
    path('', EnrollmentListView.as_view(), name='enrollment_list'),
    path('create/', EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('<int:pk>/delete/', EnrollmentDeleteView.as_view(), name='enrollment_delete'),
]