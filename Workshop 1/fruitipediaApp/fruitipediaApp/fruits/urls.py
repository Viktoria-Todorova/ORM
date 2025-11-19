from django.contrib import admin
from django.urls import path,include

from fruitipediaApp.fruits.views import index_view, dashboard_view, create_fruit, fruit_details_view, edit_fruit_view, \
    delete_fruit_view, create_category_view

urlpatterns = [
    path('',index_view, name='index'),
    path('dashboard/',dashboard_view, name='dashboard'),
    path('create-fruit/',create_fruit, name='create-fruit'),
    path('<int:pk>/', include([
        path('fruit-details',fruit_details_view,name='fruit-details'),
        path('fruit-edit',edit_fruit_view,name='edit-fruit'),
        path('delete-fruit',delete_fruit_view,name='delete-fruit')
    ])),
    path('create-category',create_category_view,name='create-category'),

]
#•	http://localhost:8000/<fruitId>/details-fruit/