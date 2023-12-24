from django.shortcuts import redirect, render, get_object_or_404
from .models import Game, Period, Warehouse, Happiness, Safety
from users.models import User
from .forms import GameCreateForm, MainForm, HappynessForm
import games.algorithms as a


def index(request):
    """
    Стартовая страница.

    Выводится форма для начала игры.
    Выводиться список всех последних завершенных игр.
    """

    user = request.user
    form = GameCreateForm(request.POST or None)

    if form.is_valid():
        game = form.save(commit=False)
        game.creator = user
        game.save()

        return redirect('games:active_game', game_id=game.id, username=user.username)

    # В выборку на главной странице должны попадать только завершенные игры
    games = Game.objects.filter(game_over=True)

    return render(request, 'games/index.html', {'games': games, 'form': form})


def games_list(request):
    """Список игр."""

    games = Game.objects.all()

    return render(request, 'games/games_list.html', {'games': games})


def game_detail(request, game_id):
    """Просмотр информации по игре (завершенной)."""

    game = get_object_or_404(Game, pk=game_id)

    if not game.game_over:
        return redirect('games:active_game', game_id=game_id)

    return render(request, 'games/game_detail.html', {'game': game})


# Не нужна ?
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
    form = MainForm(request.POST)
    form2 = HappynessForm(request.POST)

    # Брать текущий период

    if request.method == 'POST':
        form = MainForm(request.POST)
        form2 = HappynessForm(request.POST)
        if form.is_valid():
            # Производит операции по расчету следующего периода

            # Увеличиваем порядковый номер текущего периода в игре
            game.current_period += 1

            # Создаем новый период с новым порядковым номером
            new_period = Period.objects.create(game_id=game.id, number=game.current_period)

            # Создаем объекты хранилища для нового периода с заполненным полем title
            for title in a.WAREHOUSE_OBJECTS:
                Warehouse.objects.create(period_id=new_period.pk, title=title)

            happiness = Happiness.objects.create(period_id=new_period.pk)
            safety = Safety.objects.create(period_id=new_period.pk)



            game.save()

    print(game.current_period)
    wh = game.periods.filter(number=game.current_period)
    print('wh', wh)


    return render(request, 'games/active_game.html', {'game': game, 'form': form, 'form2': form2})
