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


class ExtendedBaseMinistryForm(forms.ModelForm):
    """
    Базовая (расширенная) форма министерства.

    Наследуется формами министерств с затратами финансов и товаров.
    """

    class Meta:
        fields = (
            'total_finance_provision',
            'total_goods_provision',
        )
        exclude = ('period', 'game')


class BaseWorkersEquipmentForm(forms.ModelForm):
    """
    Базовая форма министерств с сотрудниками и оборудованием.

    Наследуется формами министерств, где задействованы сотрудники
    и оборудование.
    """

    class Meta:
        fields = (
            'number_workers',
            'salary_fund',
        )


class BaseEnergyForm(forms.ModelForm):
    """
    Базовая форма министерств расходующих энергоресурсы.

    Наследуется формами министерств расходующих энергоресурсы.
    """

    class Meta:
        fields = (
            'energy_provision',
        )


class BaseNaturalResourceForm(forms.ModelForm):
    """
    Базовая форма министерств расходующих природные ресурсы.

    Наследуется формами министерств расходующих природные ресурсы.
    """

    class Meta:
        fields = (
            'natural_resource_provision',
        )


class BaseAgroForm(forms.ModelForm):
    """
    Базовая форма министерств расходующих сельскохозяйственную продукцию.

    Наследуется формами министерств расходующих сельскохозяйственную продукцию.
    """

    class Meta:
        fields = (
            'agro_provision',
        )


class BaseGoodsForm(forms.ModelForm):
    """
    Базовая форма министерств расходующих товары.

    Наследуется формами министерств расходующих товары.
    """

    class Meta:
        fields = (
            'goods_provision',
        )


class MinistryPopulationForm(
    ExtendedBaseMinistryForm,
    BaseAgroForm,
    BaseGoodsForm,
    BaseEnergyForm,
):
    """
    Форма министерства народонаселения.

    Для передачи данных, предоставленных министерством народонаселения
    за текущий период.
    """
    class Meta(
        ExtendedBaseMinistryForm.Meta,
        BaseAgroForm.Meta,
        BaseGoodsForm.Meta,
        BaseEnergyForm.Meta,
    ):
        model = MinistryPopulation
        fields = ExtendedBaseMinistryForm.Meta.fields + \
            BaseAgroForm.Meta.fields + BaseGoodsForm.Meta.fields + \
            BaseEnergyForm.Meta.fields + \
            (
                'social_benefits',
                'education_goods_contribution',
                'healthcare_goods_contribution',
            )


class MinistryNaturalResourcesForm(
    ExtendedBaseMinistryForm,
    BaseWorkersEquipmentForm,
    BaseEnergyForm,
):
    """
    Форма министерства природных ресурсов.

    Для передачи данных, предоставленных министерством природных ресурсов
    за текущий период.
    """

    class Meta(
        ExtendedBaseMinistryForm.Meta,
        BaseWorkersEquipmentForm.Meta,
        BaseEnergyForm.Meta,
    ):
        model = MinistryNaturalResources
        fields = ExtendedBaseMinistryForm.Meta.fields + \
            BaseWorkersEquipmentForm.Meta.fields + \
            BaseEnergyForm.Meta.fields + \
            (
                'damage_reduction_goods_contribution',
            )


class MinistryEnergyForm(
    ExtendedBaseMinistryForm,
    BaseWorkersEquipmentForm,
    BaseEnergyForm,
    BaseNaturalResourceForm,
):
    """
    Форма министерства энергетики.

    Для передачи данных, предоставленных министерством энергетики
    за текущий период.
    """

    class Meta(
        ExtendedBaseMinistryForm.Meta,
        BaseWorkersEquipmentForm.Meta,
        BaseEnergyForm.Meta,
        BaseNaturalResourceForm.Meta,
    ):
        model = MinistryEnergy
        fields = \
            ExtendedBaseMinistryForm.Meta.fields + \
            BaseWorkersEquipmentForm.Meta.fields + \
            BaseEnergyForm.Meta.fields + \
            BaseNaturalResourceForm.Meta.fields + \
            (
                'energy_efficiency_goods_contribution',
            )


class MinistryIndustryForm(
    ExtendedBaseMinistryForm,
    BaseWorkersEquipmentForm,
    BaseEnergyForm,
    BaseNaturalResourceForm,
):
    """
    Форма министерства промышленности.

    Для передачи данных, предоставленных министерством промышленности
    за текущий период.
    """

    class Meta(
        ExtendedBaseMinistryForm.Meta,
        BaseWorkersEquipmentForm.Meta,
        BaseEnergyForm.Meta,
        BaseNaturalResourceForm.Meta,
    ):
        model = MinistryIndustry
        fields = \
            ExtendedBaseMinistryForm.Meta.fields + \
            BaseWorkersEquipmentForm.Meta.fields + \
            BaseEnergyForm.Meta.fields + \
            BaseNaturalResourceForm.Meta.fields + \
            (
                'quality_goods_contribution',
                'wasteless_production_goods_contribution',
            )


class MinistryAgricultureForm(
    ExtendedBaseMinistryForm,
    BaseWorkersEquipmentForm,
    BaseEnergyForm,
):
    """
    Форма министерства сельского хозяйства.

    Для передачи данных, предоставленных министерством сельского хозяйства
    за текущий период.
    """

    class Meta(
        ExtendedBaseMinistryForm.Meta,
        BaseWorkersEquipmentForm.Meta,
        BaseEnergyForm.Meta,
    ):
        model = MinistryAgriculture
        fields = \
            ExtendedBaseMinistryForm.Meta.fields + \
            BaseWorkersEquipmentForm.Meta.fields + \
            BaseEnergyForm.Meta.fields + \
            (
                'quality_goods_contribution',
            )


class MinistryTransportForm(
    ExtendedBaseMinistryForm,
    BaseWorkersEquipmentForm,
    BaseEnergyForm,
):
    """
    Форма министерства транспорта.

    Для передачи данных, предоставленных министерством транспорта
    за текущий период.
    """

    class Meta(
        ExtendedBaseMinistryForm.Meta,
        BaseWorkersEquipmentForm.Meta,
        BaseEnergyForm.Meta,
    ):
        model = MinistryTransport
        fields = \
            ExtendedBaseMinistryForm.Meta.fields + \
            BaseWorkersEquipmentForm.Meta.fields + \
            BaseEnergyForm.Meta.fields + \
            (
                'transport_efficiency_goods_contribution',
                'transport_environmental_friendliness_goods_contribution',
            )


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
