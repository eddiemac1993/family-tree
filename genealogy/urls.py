from django.urls import path
from .views import family_tree_view

urlpatterns = [
    path('', family_tree_view, name='family_tree'),
]
