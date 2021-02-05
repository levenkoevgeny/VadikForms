from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('subjects', views.subject_list, name='subject_list'),
    path('subjects/<subject_id>/tests', views.test_list, name='test_list'),
    path('subjects/<subject_id>/test/<test_id>/passing', views.test_passing, name='test_passing'),
    path('subjects/<subject_id>/test/<test_id>/result', views.test_result, name='test_result'),
    path('subjects/<subject_id>/test/<test_id>/result/<result_id>', views.test_result, name='test_result'),
    path('results', views.test_all_results, name='test_all_results'),
]