from django.urls import path
from . import views


urlpatterns = [
    path('game/', views.CountdownGameView.as_view(), name='countdown_game'),
]
