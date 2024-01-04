from django.shortcuts import redirect, render, get_object_or_404
import pandas as pd
from .models import Game, Warehouse, Happiness, Safety, MinistryNaturalResources, MinistryFinance
from users.models import User
from .forms import GameCreateForm, MinistryNaturalResourcesForm, MinistryEnergyForm, MinistryPopulationForm, \
    MinistryIndustryForm, MinistryAgricultureForm, MinistryTransportForm, MinistryFinanceForm
import games.algorithms as a
import games.constants as const
from .translation import translation_dict


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
        try:
            game.max_periods = const.periods
        except AttributeError as err:
            pass

        game.save()

        return redirect('games:active_game', game_id=game.id)

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
        game.save(creator=user, max_periods=const.periods)

        return redirect('games:active_game', game_id=game.id)

    return render(request, 'games/game_start.html', {'form': form})


# Сделать отдельную страницу для активной (не завершенной) игры
def active_game(request, game_id):
    """Активная (не завершенная) игра."""

    game = get_object_or_404(Game, pk=game_id)

    # Получаем текущий период игры
    cur_period = game.current_period

    m_fin = MinistryFinance.objects.get(game_id=game_id, period=cur_period)


    # Перечисляем все формы министерств
    form_min_population = MinistryPopulationForm(request.POST or None)
    form_min_natural_resource = MinistryNaturalResourcesForm(request.POST or None)
    form_min_energy = MinistryEnergyForm(request.POST or None)
    form_min_industry = MinistryIndustryForm(request.POST or None)
    form_min_agriculture = MinistryAgricultureForm(request.POST or None)
    form_min_transport = MinistryTransportForm(request.POST or None)
    form_min_finance = MinistryFinanceForm(request.POST or None, instance=m_fin)


    if request.method == 'POST':
        # Создаем новый период с соответствующим порядковым номером
        # new_period = Period.objects.create(game_id=game_id, number=game.current_period + 1)

        if form_min_finance.is_valid():
            # Производит операции по расчету следующего периода

            # Создаем объекты хранилища для нового периода с заполненным полем title
            for title in a.WAREHOUSE_OBJECTS:
                # Warehouse.objects.create(period_id=new_period.pk, title=title)
                ...

            # happiness = Happiness.objects.create(period_id=new_period.pk)
            # safety = Safety.objects.create(happiness_id=happiness.pk)

            form_min_finance.save()

            # Увеличиваем порядковый номер текущего периода в игре
            game.current_period += 1

            game.save()

            return redirect('games:active_game', game_id=game.id)

    # Берем все данные мин.финансов
    min_finance_data = game.games_ministryfinance.all()
    # Для заполнения таблицы создаем датафрейм
    df = pd.DataFrame(min_finance_data.values())
    # Транспонируем датафрейм для оптимальной визуализации данных
    tr_df = df.transpose()



    context = {
        'game': game,
        'df': tr_df,
        'tr_dict': translation_dict,
        'form_min_finance': form_min_finance,
        'form_min_energy': form_min_energy,
        'form_min_natural_resource': form_min_natural_resource
    }
    return render(request, 'games/active_game.html', context)
