"""
Здесь собраны все константы и алгоритмы для вычислений при завершении
игрового периода.
"""

from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
import pandas as pd
from .models import Game, Storage, Happiness, Safety, MinistryNaturalResources, MinistryFinance, MinistryPopulation, \
    MinistryEnergy, MinistryIndustry, MinistryAgriculture, MinistryTransport, Workers
from users.models import User
from .forms import GameCreateForm, MinistryNaturalResourcesForm, MinistryEnergyForm, MinistryPopulationForm, \
    MinistryIndustryForm, MinistryAgricultureForm, MinistryTransportForm, MinistryFinanceForm, WorkersForm, \
    WorkersFormSet, WorkersGetFormSet
import games.algorithms as a
import games.constants as const
from .translation import translation_dict


# Стартовый индекс счастья
HAPPINESS_INDEX = 5.5

# Объекты Хранилища (Warehouse), используются для заполнения поля title
# WAREHOUSE_OBJECTS = [
#     'Финансы',
#     'Государственный долг',
#     'Природные ресурсы',
#     'Энергоресурсы',
#     'Товары и оборудование',
#     'Продукты питания',
# ]


# Объекты
MIN_OBJECTS = {

}



def d(*args, **kwargs):
    """
    Производит полный расчет предоставленных данных от министерств,
    заполняет все таблицы связанные с периодом,
    создает новый период с заполненными стартовыми данными.
    """

    request = kwargs['request']
    game_id = None
    if 'game_id' in kwargs:
        game_id = kwargs['game_id']
    else:
        # Сделать логирование ошибки отсутствия ID игры
        raise Exception

    game = get_object_or_404(Game, pk=game_id)

    # Получаем текущий период игры
    cur_period = game.current_period

    # Выбираем объекты текущего игрового периода для заполнения данных через формы
    m_populat = MinistryPopulation.objects.get(game_id=game_id, period=cur_period)
    m_nat_res = MinistryNaturalResources.objects.get(game_id=game_id, period=cur_period)
    m_energy = MinistryEnergy.objects.get(game_id=game_id, period=cur_period)
    m_industry = MinistryIndustry.objects.get(game_id=game_id, period=cur_period)
    m_agro = MinistryAgriculture.objects.get(game_id=game_id, period=cur_period)
    m_trans = MinistryTransport.objects.get(game_id=game_id, period=cur_period)
    m_fin = MinistryFinance.objects.get(game_id=game_id, period=cur_period)

    # Сопутствующие объекты периода для заполнения данных через формы
    workers = m_populat.workers.exclude(title__in=('Все рабочие',))

    # Перечисляем все формы для заполнения в текущем периоде
    form_m_populat = MinistryPopulationForm(request.POST or None, instance=m_populat)
    form_m_nat_res = MinistryNaturalResourcesForm(request.POST or None, instance=m_nat_res)
    form_m_energy = MinistryEnergyForm(request.POST or None, instance=m_energy)
    form_m_industry = MinistryIndustryForm(request.POST or None, instance=m_industry)
    form_m_agro = MinistryAgricultureForm(request.POST or None, instance=m_agro)
    form_m_trans = MinistryTransportForm(request.POST or None, instance=m_trans)
    form_m_fin = MinistryFinanceForm(request.POST or None, instance=m_fin)

    # Формсет распределения рабочих для обучения
    # используется FormSet для GET-запроса
    formset_workers = WorkersGetFormSet(queryset=workers)

    # Собираем данные всех периодов игры
    m_populat_data = game.games_ministrypopulation.all()
    m_nat_res_data = game.games_ministryfinance.all()
    m_energy_data = game.games_ministryfinance.all()
    m_industry_data = game.games_ministryfinance.all()
    m_agro_data = game.games_ministryfinance.all()
    m_trans_data = game.games_ministryfinance.all()
    m_fin_data = game.games_ministryfinance.all()

    # Для заполнения таблицы создаем датафреймы и транспонируем их
    m_populat_df = pd.DataFrame(m_populat_data.values()).transpose()
    m_nat_res_df = pd.DataFrame(m_nat_res_data.values()).transpose()
    m_energy_df = pd.DataFrame(m_energy_data.values()).transpose()
    m_industry_df = pd.DataFrame(m_industry_data.values()).transpose()
    m_agro_df = pd.DataFrame(m_agro_data.values()).transpose()
    m_trans_df = pd.DataFrame(m_trans_data.values()).transpose()
    m_fin_df = pd.DataFrame(m_fin_data.values()).transpose()

    context = {
        'game': game,

        'tr_dict': translation_dict,

        'm_populat_df': m_populat_df,
        'm_nat_res_df': m_nat_res_df,
        'm_energy_df': m_energy_df,
        'm_industry_df': m_industry_df,
        'm_agro_df': m_agro_df,
        'm_trans_df': m_trans_df,
        'm_fin_df': m_fin_df,

        'form_m_populat': form_m_populat,
        'form_m_nat_res': form_m_nat_res,
        'form_m_energy': form_m_energy,
        'form_m_industry': form_m_industry,
        'form_m_agro': form_m_agro,
        'form_m_trans': form_m_trans,
        'form_m_fin': form_m_fin,
        'formset_workers': formset_workers,
    }

    return context

def main(*args, **kwargs):
    """
    Производит полный расчет предоставленных данных от министерств,
    заполняет все таблицы связанные с периодом,
    создает новый период с заполненными стартовыми данными.
    """

    request = kwargs['request']
    game_id = None
    if 'game_id' in kwargs:
        game_id = kwargs['game_id']
    else:
        # Сделать логирование ошибки отсутствия ID игры
        raise Exception

    game = get_object_or_404(Game, pk=game_id)

    # Получаем текущий период игры
    cur_period = game.current_period

    # Выбираем объекты текущего игрового периода для заполнения данных через формы
    m_populat = MinistryPopulation.objects.get(game_id=game_id, period=cur_period)
    m_nat_res = MinistryNaturalResources.objects.get(game_id=game_id, period=cur_period)
    m_energy = MinistryEnergy.objects.get(game_id=game_id, period=cur_period)
    m_industry = MinistryIndustry.objects.get(game_id=game_id, period=cur_period)
    m_agro = MinistryAgriculture.objects.get(game_id=game_id, period=cur_period)
    m_trans = MinistryTransport.objects.get(game_id=game_id, period=cur_period)
    m_fin = MinistryFinance.objects.get(game_id=game_id, period=cur_period)

    # Сопутствующие объекты периода для заполнения данных через формы
    workers = m_populat.workers.exclude(title__in=('Все рабочие',))

    # Перечисляем все формы для заполнения в текущем периоде
    form_m_populat = MinistryPopulationForm(request.POST or None, instance=m_populat)
    form_m_nat_res = MinistryNaturalResourcesForm(request.POST or None, instance=m_nat_res)
    form_m_energy = MinistryEnergyForm(request.POST or None, instance=m_energy)
    form_m_industry = MinistryIndustryForm(request.POST or None, instance=m_industry)
    form_m_agro = MinistryAgricultureForm(request.POST or None, instance=m_agro)
    form_m_trans = MinistryTransportForm(request.POST or None, instance=m_trans)
    form_m_fin = MinistryFinanceForm(request.POST or None, instance=m_fin)

    # Формсет распределения рабочих для обучения
    # используется FormSet для GET-запроса
    formset_workers = WorkersGetFormSet(queryset=workers)

    if request.method == 'POST':

        # При отправке POST-запроса FormSet обучения рабочих меняется
        # В данном формсете не используется поле title
        formset_workers = WorkersFormSet(request.POST or None, queryset=workers)

        # Нужно добавить проверку формы рабочих !!!!
        if form_m_populat.is_valid() and form_m_nat_res.is_valid() \
            and form_m_energy.is_valid() and form_m_industry.is_valid() and form_m_agro.is_valid() \
            and form_m_trans.is_valid() and form_m_fin.is_valid() \
            and formset_workers.is_valid():

            # Производит операции по расчету следующего периода

            ###########
            # Создаем объекты хранилища для нового периода с заполненным полем title
            '''
            for title in a.WAREHOUSE_OBJECTS:
                # Warehouse.objects.create(period_id=new_period.pk, title=title)
                ...
            '''

            # happiness = Happiness.objects.create(period_id=new_period.pk)
            # safety = Safety.objects.create(happiness_id=happiness.pk)
            #############

            # Сохраняем все объекты с переданными данными из формы
            form_m_populat.save()
            form_m_nat_res.save()
            form_m_energy.save()
            form_m_industry.save()
            form_m_agro.save()
            form_m_trans.save()
            form_m_fin.save()

            formset_workers.save()

            # Увеличиваем порядковый номер текущего периода в игре
            game.current_period += 1
            game.save()

            return redirect('games:active_game', game_id=game.id)

    # Собираем данные всех периодов игры
    m_populat_data = game.games_ministrypopulation.all()
    m_nat_res_data = game.games_ministryfinance.all()
    m_energy_data = game.games_ministryfinance.all()
    m_industry_data = game.games_ministryfinance.all()
    m_agro_data = game.games_ministryfinance.all()
    m_trans_data = game.games_ministryfinance.all()
    m_fin_data = game.games_ministryfinance.all()

    # Для заполнения таблицы создаем датафреймы и транспонируем их
    m_populat_df = pd.DataFrame(m_populat_data.values()).transpose()
    m_nat_res_df = pd.DataFrame(m_nat_res_data.values()).transpose()
    m_energy_df = pd.DataFrame(m_energy_data.values()).transpose()
    m_industry_df = pd.DataFrame(m_industry_data.values()).transpose()
    m_agro_df = pd.DataFrame(m_agro_data.values()).transpose()
    m_trans_df = pd.DataFrame(m_trans_data.values()).transpose()
    m_fin_df = pd.DataFrame(m_fin_data.values()).transpose()

    context = {
        'game': game,

        'tr_dict': translation_dict,

        'm_populat_df': m_populat_df,
        'm_nat_res_df': m_nat_res_df,
        'm_energy_df': m_energy_df,
        'm_industry_df': m_industry_df,
        'm_agro_df': m_agro_df,
        'm_trans_df': m_trans_df,
        'm_fin_df': m_fin_df,

        'form_m_populat': form_m_populat,
        'form_m_nat_res': form_m_nat_res,
        'form_m_energy': form_m_energy,
        'form_m_industry': form_m_industry,
        'form_m_agro': form_m_agro,
        'form_m_trans': form_m_trans,
        'form_m_fin': form_m_fin,
        'formset_workers': formset_workers,
    }

    return context


def create_tables(game) -> None:
    print(120301293812371029)

    for i in range(11):
        MinistryFinance.objects.create(game=game.id, period=i)
        print(i)

