from django.urls import path
from . import views

urlpatterns = [
    path('', views.FilmUserAPIView.as_view(), name="film"),
    path('all', views.FilmListAllAPIView.as_view(), name="all_film"),
    path('<int:id>', views.FilmUpdateAPIView.as_view(), name="update_film"),
]
