from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # Стартовая страница
    path('', views.index, name='index'),
    # Страница пользователя; перечислены все проведенные игры, кнопка начала новой игры
    # Проверить, что username формата слаг
    # УБРАТЬ !
    # path('profile/<slug:username>/', views.profile, name='profile'),

    # Просмотр списка всех законченных игр (начиная с последней в обратном порядке)
    path('games/', views.games_list, name='games_list'),

    # Начало новой игры
    path('start/', views.game_start, name='game_start'),
    # Страница активной игры
    # УБРАТЬ !
    path('<int:game_id>/active/', views.active_game, name='active_game'),
    # Просмотр результата отдельной игры (завершенной)
    path('<int:game_id>/', views.game_detail, name='game_detail'),
]
