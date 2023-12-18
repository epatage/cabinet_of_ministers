from django.shortcuts import redirect, render, get_object_or_404
from .models import Game
from users.models import User


def index(request):
    """Стартовая страница."""

    user = request.user
    form = GameCreateForm(request.POST or None)
    # game = Game.objects.create(creator=user)

    if form.is_valid():
        game = form.save(commit=False)
        game.save(creator=user)

        return redirect('games:active_game', game_id=game.id)

    games = Game.objects.all()

    return render(request, 'games/index.html', {'games': games, 'form': form})


def profile(request, username):
    """Профайл пользователя."""

    user = get_object_or_404(User, pk=username.id)

    return render(request, 'games/profile.html', {'user': user})


# Объединить со стартовой страницей
def games_list(request):
    """Список завершенных игр."""

    games = Game.objects.all()

    return render(request, 'games/games_list.html', {'games': games})


def game_detail(request, game_id):
    """Просмотр информации по игре (завершенной)."""

    game = get_object_or_404(Game, pk=game_id)

    return render(request, 'games/game_detail.html', {'game': game})


def game_start(request):
    """Создание новой игры."""

    user = request.user
    form = GameCreateForm(request.POST or None)
    # game = Game.objects.create(creator=user)

    if form.is_valid():
        game = form.save(commit=False)
        game.save(creator=user)

        return redirect('games:active_game', game_id=game.id)

    return render(request, 'games/game_start.html', {'form': form})


# Сделать отдельную страницу для активной (не завершенной) игры
def active_game(request, game_id):
    """Активная (не завершенная) игра."""

    game = get_object_or_404(Game, pk=game_id)

    return render(request, 'games/games_list.html', {'game': game})
