from django.urls import path
from . import views

app_name = 'testing'

urlpatterns = [
    path('test/<pk>/delete/', views.TestDelete.as_view(), name='test_delete'),
    path('subjects/<subject_id>/tests', views.test_list, name='test_list'),
    path('subjects', views.subject_list, name='subject_list'),
    path('subjects/add', views.subject_add, name='subject_add'),
    path('subjects/<subject_id>/update', views.subject_update, name='subject_update'),
    path('subjects/<pk>/delete/', views.SubjectDelete.as_view(), name='subject_delete'),
    path('subjects/<subject_id>/tests/add', views.test_add, name='test_add'),
    path('subjects/<subject_id>/tests/<test_id>/update', views.test_update, name='test_update'),
    path('subjects/<subject_id>/tests/<test_id>/download', views.test_download, name='test_download'),

    path('all_tests', views.all_tests, name='all_tests'),
    path('subjects/<subject_id>/tests/<test_id>/update', views.test_update, name='test_update'),

]