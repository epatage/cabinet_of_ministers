from django import forms
from django.forms import modelformset_factory

from .models import Game, Happiness, MinistryNaturalResources, MinistryEnergy, MinistryIndustry, \
    MinistryAgriculture, MinistryTransport, MinistryFinance, MinistryPopulation, Workers


class GameCreateForm(forms.ModelForm):
    """Форма создания игры."""

    class Meta:
        model = Game
        fields = ('country_name',)
        labels = {
            'country_name': 'Название государства',
        }


class BaseMinistryForm(forms.ModelForm):
    """
    Базовая форма министерства.

    Наследуется министерствами с использованием сотрудников и оборудования.
    """

    class Meta:
        fields = '__all__'
        exclude = ('period', 'game')
        # fields = (
        #     'number_workers',
        #     'equipment_amount',
        #     'salary_fund',
        #     'energy_provision',
        # )


class MinistryPopulationForm(forms.ModelForm):
    """
    Форма министерства народонаселения.

    Для передачи данных, предоставленных министерством народонаселения
    за текущий период.
    """
    class Meta:
        model = MinistryPopulation
        fields = '__all__'
        exclude = ('period', 'game')


class MinistryNaturalResourcesForm(BaseMinistryForm):
    """
    Форма министерства природных ресурсов.

    Для передачи данных, предоставленных министерством природных ресурсов
    за текущий период.
    """

    class Meta(BaseMinistryForm.Meta):
        model = MinistryNaturalResources
        fields = (
            'number_workers',
            'salary_fund',
            'energy',
            'production_contribution_damage_reduction',
        )


class MinistryEnergyForm(BaseMinistryForm):
    """
    Форма министерства энергетики.

    Для передачи данных, предоставленных министерством энергетики
    за текущий период.
    """

    class Meta(BaseMinistryForm.Meta):
        model = MinistryEnergy


class MinistryIndustryForm(BaseMinistryForm):
    """
    Форма министерства промышленности.

    Для передачи данных, предоставленных министерством промышленности
    за текущий период.
    """

    class Meta(BaseMinistryForm.Meta):
        model = MinistryIndustry


class MinistryAgricultureForm(BaseMinistryForm):
    """
    Форма министерства сельского хозяйства.

    Для передачи данных, предоставленных министерством сельского хозяйства
    за текущий период.
    """

    class Meta(BaseMinistryForm.Meta):
        model = MinistryAgriculture


class MinistryTransportForm(BaseMinistryForm):
    """
    Форма министерства транспорта.

    Для передачи данных, предоставленных министерством транспорта
    за текущий период.
    """

    class Meta(BaseMinistryForm.Meta):
        model = MinistryTransport


class MinistryFinanceForm(forms.ModelForm):
    """
    Форма министерства финансов.

    Для передачи данных, предоставленных министерством финансов
    за текущий период.
    """
    class Meta:
        model = MinistryFinance
        fields = '__all__'
        exclude = ('game', 'period')


class WorkersForm(forms.ModelForm):
    """
    Форма распределения рабочих для обучения.

    Процентное отношение рабочих для обучения по специальностям.
    Передается министерством народонаселения.
    Используется при POST-запросе.
    """
    class Meta:
        model = Workers
        fields = ('workers_part',)


class WorkersGetForm(WorkersForm):
    """
    Форма GET-запроса распределения рабочих для обучения.

    Необходима для вывода полей title в качестве обозначений полей формы при
    GET-запросе.
    """
    class Meta(WorkersForm.Meta):
        fields = ('title',) + WorkersForm.Meta.fields


"""FormSet POST-запроса для распределения обучения рабочих."""
WorkersFormSet = modelformset_factory(
    Workers,
    form=WorkersForm,
    extra=0,
)


"""FormSet GET-запроса для распределения обучения рабочих."""
WorkersGetFormSet = modelformset_factory(
    Workers,
    form=WorkersGetForm,
    extra=0,
)
