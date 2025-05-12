from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.videogame_form,name='videogame_insert'), # get and post req. for insert operation
    path('<int:id>/', views.videogame_form,name='videogame_update'), # get and post req. for update operation
    path('delete/<int:id>/',views.videogame_delete,name='videogame_delete'), # get and post req. for deleting operation
    path('list/',views.videogame_list,name='videogame_list'),  # get req. to retrieve and display all records

    path('developer/list/', views.developer_list, name='developer_list'),
    path('developer/add/', views.developer_form, name='developer_add'),

    path('review/list/', views.review_list, name='review_list'),
    path('review/add/', views.review_form, name='review_add'),

    path('userprofile/list/', views.userprofile_list, name='userprofile_list'),
    path('userprofile/add/', views.userprofile_form, name='userprofile_add'),

    path('copy/list/', views.copy_list, name='copy_list'),
    path('copy/add/', views.copy_form, name='copy_add'),

    path('reports/top-genres', views.report_top_genres, name = 'report_top_genres'),

    path('reports/releases-over-time/', views.report_releases_over_time, name='report_releases_over_time'),

    path('reports/cumulative/', views.report_cumulative_releases, name='report_cumulative'),

    path('reports/', views.report_dashboard, name='report_dashboard'),


]