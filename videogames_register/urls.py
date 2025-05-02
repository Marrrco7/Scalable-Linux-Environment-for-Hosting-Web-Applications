from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.videogame_form,name='videogame_insert'), # get and post req. for insert operation
    path('<int:id>/', views.videogame_form,name='videogame_update'), # get and post req. for update operation
    path('delete/<int:id>/',views.videogame_delete,name='videogame_delete'), # get and post req. for deleting operation
    path('list/',views.videogame_list,name='videogame_list'),  # get req. to retrieve and display all records

    path('reports/top-genres', views.report_top_genres, name = 'report_top_genres'),

    path('reports/releases-over-time/', views.report_releases_over_time, name='report_releases_over_time'),

]