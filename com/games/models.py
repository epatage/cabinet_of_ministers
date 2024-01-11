import modulefinder
from django.db.models.signals import post_save
from django.dispatch import receiver

import games.constants as const

from django.db import models
from users.models import User

from games.exceptions import ConstantException


#
# class Period(models.Model):
#     """
#     Модель периода (игрового года).
#
#     Сочетание объекта игры к которому относиться период
#     и номера периода должно быть уникальным.
#     """
#
#     game = models.ForeignKey(
#         'Game',
#         blank=False,
#         null=False,
#         on_delete=models.CASCADE,
#         related_name='periods',
#         verbose_name='Годовой период',
#         help_text='Годовой период',
#     )
#     number = models.PositiveSmallIntegerField('Номер периода', default=0, null=False, blank=False)
#
#     # class Meta:
#     #     constraints = [
#     #         models.UniqueConstraint(
#     #             fields=['game', 'number'],
#     #             name='unique_game_number'
#     #         )
#     #     ]
#
#     def __str__(self):
#         return f'{self.game.country_name} - {self.number}'


# class Welfare(models.Model):
#     """Благосостояние населения."""
#
#     welfare_level = models.DecimalField('Уровень благосостояния', max_digits=5, decimal_places=3, null=True, blank=True)
#     general = models.OneToOneField('General', verbose_name='Общие показатели', on_delete=models.CASCADE, null=False, blank=False)


class Welfare(models.Model):
    """
    Уровень благосостояния населения по группам.

    Объекты создаются при создании объекта General. Поле title заполняется
    при создании объекта из списка групп населения.
    """

    title = models.CharField('Группа населения', max_length=50, null=False)
    group_ratio = models.DecimalField('Доля группы населения в общем количестве', max_digits=5, decimal_places=4, null=True, blank=True)
    average_income = models.DecimalField('Средний доход на человека', max_digits=7, decimal_places=2, null=True, blank=True)
    general = models.ForeignKey(
        'General',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='welfares',
        verbose_name='Благосостояние',
        help_text='Благосостояние',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['general', 'title'],
                name='welfare_unique_general_title'
            )
        ]


    # def __str__(self):
    #     return f'{self.welfare.general.game.country_name} - {self.period.number} - {self.index}'


class General(models.Model):
    """
    Общие показатели.

    Отображены основные показатели, напрямую касающиеся населения
    по результатам решений за игровой период.
    """
    game = models.ForeignKey(
        'Game',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='generals',
        verbose_name='Игра',
        help_text='Игра',
    )
    period = models.PositiveSmallIntegerField('Период', null=False, blank=False)
    population = models.PositiveIntegerField('Население', null=False, default=0)
    education = models.DecimalField('Уровень образования населения', max_digits=5, decimal_places=2, null=True, blank=True)
    healthcare = models.DecimalField('Уровень здравоохранения', max_digits=5, decimal_places=2, null=True, blank=True)
    welfare_level = models.DecimalField('Уровень благосостояния', max_digits=5, decimal_places=3, null=True, blank=True)
    living_cost = models.DecimalField('Прожиточный минимум', max_digits=7, decimal_places=2, null=True, blank=True)
    birth_rate = models.DecimalField('Уровень рождаемости', max_digits=7, decimal_places=1, null=True, blank=True)
    mortality_rate = models.DecimalField('Уровень смертности', max_digits=7, decimal_places=1, null=True, blank=True)
    natural_environment = models.DecimalField('Окружающая среда', max_digits=5, decimal_places=4, null=True, blank=True)
    transport_efficiency = models.DecimalField('Транспортная эффективность', max_digits=5, decimal_places=3, null=True, blank=True)
    energy_efficiency = models.DecimalField('Энергетическая эффективность', max_digits=5, decimal_places=3, null=True, blank=True)
    gdp = models.PositiveIntegerField('ВВП', null=True, blank=True)
    gdp_per_soul = models.DecimalField('ВВП на душу населения (абсолютный показатель)', max_digits=7, decimal_places=3, null=True, blank=True)
    population_on_social_security = models.PositiveIntegerField('Количество населения на социальном обеспечении', null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['game', 'period'],
                name='%(class)s_unique_game_period'
            )
        ]

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)

        if created:
            try:
                # Берем список групп населения из модуля константы
                groups: list = const.population_groups
            except AttributeError as err:
                # Сделать логирование ошибки <--
                raise ConstantException(f'Ошибка {err}')

            for group in groups:
                Welfare.objects.create(general=self, title=group)


class Happiness(models.Model):
    """Индекс счастья."""

    game = models.ForeignKey(
        'Game',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='happinesses',
        verbose_name='Игра',
        help_text='Игра',
    )
    period = models.PositiveSmallIntegerField('Период', null=False, blank=False)
    index = models.DecimalField(
        'Индекс счастья',
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )
    gdp_per_soul = models.DecimalField(
        'ВВП на душу населения(коэффициент)',
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    joblessness = models.DecimalField('Безработица', max_digits=5, decimal_places=2, null=True, blank=True)
    birth_rate = models.DecimalField('Рождаемость', max_digits=5, decimal_places=2, null=True, blank=True)
    mortality_rate = models.DecimalField('Смертность', max_digits=5, decimal_places=2, null=True, blank=True)
    education = models.DecimalField('Образованность', max_digits=5, decimal_places=2, null=True, blank=True)
    welfare = models.DecimalField('Благосостояние', max_digits=5, decimal_places=2, null=True, blank=True)
    transport_accessibility = models.DecimalField('Транспортная доступность', max_digits=5, decimal_places=2, null=True, blank=True)
    goods_provision = models.DecimalField('Обеспеченность товарами', max_digits=5, decimal_places=2, null=True, blank=True)
    energy_provision = models.DecimalField('Обеспеченность энергоресурсами', max_digits=5, decimal_places=2, null=True, blank=True)
    safety = models.DecimalField('Безопасность', max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['game', 'period'],
                name='%(class)s_unique_game_period'
            )
        ]

    def __str__(self):
        return f'{self.game.country_name} - {self.period} - {self.index}'


class Safety(models.Model):
    """Безопасность и уверенности в завтрашнем дне."""

    game = models.ForeignKey(
        'Game',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='safeties',
        verbose_name='Игра',
        help_text='Игра',
    )
    period = models.PositiveSmallIntegerField('Период', null=False, blank=False)
    index = models.DecimalField('Индекс безопасности', max_digits=5, decimal_places=2, null=True, blank=True)
    environment = models.DecimalField('Окружающая среда', max_digits=5, decimal_places=2, null=True, blank=True)
    remaining_resources = models.DecimalField('Остаток ресурсов', max_digits=12, decimal_places=2, null=True, blank=True)
    food_security = models.DecimalField('Продовольственная безопасность', max_digits=5, decimal_places=2, null=True, blank=True)
    food_reserve = models.DecimalField('Продовольственный резерв', max_digits=5, decimal_places=2, null=True, blank=True)
    food_quality = models.DecimalField('Качество продовольствия', max_digits=5, decimal_places=2, null=True, blank=True)
    national_debt = models.DecimalField('Государственный долг', max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['game', 'period'],
                name='%(class)s_unique_game_period'
            )
        ]

    def __str__(self):
        return f'{self.game.country_name} - {self.period} - {self.index}'


class Workers(models.Model):
    """
    Рабочие.

    Распределение рабочих по специальностям.
    """

    title = models.CharField('Название профиля образования', max_length=50, null=False)
    workers_part = models.PositiveSmallIntegerField('Доля работников', null=True, blank=True, default=0)
    number_workers = models.PositiveIntegerField('Количество работников отрасли', null=True, default=0)
    min_population = models.ForeignKey(
        'MinistryPopulation',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='workers',
        verbose_name='Рабочие по группам образования',
        help_text='Рабочие по группам образования', )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['min_population', 'title'],
                name='workers_unique_min_population_title'
            )
        ]

    def __str__(self):
        return f'{self.min_population.game.country_name} - {self.min_population.period} - {self.title}'


class Storage(models.Model):
    """Хранилище финансов и материальных запасов."""

    # Переделывать!

    game = models.ForeignKey(
        'Game',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='warehouses',
        verbose_name='Игра',
        help_text='Игра',
    )
    period = models.PositiveSmallIntegerField('Период', null=False, blank=False)
    title = models.CharField('Название', max_length=50, null=False, blank=False)
    amount = models.IntegerField('Количество', null=False, blank=True, default=0)
    avg_price = models.DecimalField('Цена за единицу', max_digits=5, decimal_places=2, null=True, blank=True)
    quality = models.DecimalField('Качество', max_digits=5, decimal_places=2, null=True, blank=True)
    amount_finance = models.DecimalField('Финансовый параметр', max_digits=12, decimal_places=2, null=True, blank=True)
    remaining_resources = models.PositiveIntegerField('Остаток ресурсов', default=1000000)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['game', 'period', 'title'],
                name='%(class)s_unique_game_period_title'
            )
        ]

    def __str__(self):
        return f'{self.game.country_name} - {self.period} - {self.title}'


class BaseMinistry(models.Model):
    """
    Базовая модель министерств.

    Наследуется моделями всех министерств.
    """

    game = models.ForeignKey(
        'Game',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
        verbose_name='Игра',
        help_text='Игра',
    )
    period = models.PositiveSmallIntegerField('Период', null=False, blank=False)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['game', 'period'],
                name='%(class)s_unique_game_period'
            )
        ]

    def __str__(self):
        return f'{self.game.country_name} - {self.period} - {self.__class__.__doc__}'


class ExtendedBaseMinistry(models.Model):
    """
    Расширенная базовая модель министерств.

    Наследуется моделями министерств с затратами финансов и товаров.
    """

    env_damage = models.DecimalField('Нанесенный вред ОС', max_digits=5, decimal_places=3, null=False, default=0)
    total_finance_provision = models.DecimalField('Суммарное финансовое обеспечение', max_digits=12, decimal_places=2, null=True, blank=True, default=0, help_text='Суммарное финансовое обеспечение')
    total_costs = models.DecimalField('Суммарные финансовые затраты', max_digits=12, decimal_places=2, null=True, default=0)
    total_goods_provision = models.IntegerField('Суммарное обеспечение товарами', null=True, default=0, help_text='Суммарное обеспечение товарами')
    total_equipment_costs = models.IntegerField('Суммарные товарные вложения', null=True, default=0)

    class Meta:
        abstract = True


class BaseWorkersEquipment(models.Model):
    """
    Базовая модель министерств с сотрудниками и оборудованием.

    Наследуется моделями министерств, где задействованы сотрудники
    и оборудование.
    """

    number_workers = models.IntegerField('Количество работников', null=False, blank=True, default=0, help_text='Количество работников')
    equipment_amount = models.IntegerField('Количество оборудования', null=False, blank=True, default=0)
    equipment_quality = models.DecimalField('Качество оборудования', max_digits=5, decimal_places=3, null=False, default=0)
    # Необходимо проверить как работает при искусственном увеличении себестоимости до предельных размеров
    equipment_price = models.DecimalField('Цена оборудования', max_digits=12, decimal_places=2, null=False, default=0)
    salary_fund = models.DecimalField('Фонд заработной платы', max_digits=12, decimal_places=2, null=False, blank=True, default=0)
    equipment_wear = models.IntegerField('Износ оборудования', null=True, default=0)
    equipment_purchase = models.IntegerField('Приобретение оборудования', null=True, blank=True, default=0, help_text='Приобретение оборудования')
    equipment_costs = models.DecimalField('Финансовые затраты на приобретение оборудования', max_digits=10, decimal_places=2, null=True, default=0)

    class Meta:
        abstract = True


class BaseEnergy(models.Model):
    """
    Базовая модель министерств расходующих энергоресурсы.

    Наследуется моделями министерств расходующих энергоресурсы.
    """

    energy_provision = models.IntegerField('Обеспечение энергоресурсами', null=True, blank=True, default=0, help_text='Обеспечение энергоресурсами')
    energy_consumption = models.IntegerField('Потребление энергоресурсов', null=True, blank=True, default=0)
    energy_costs = models.DecimalField('Финансовые затраты на приобретение энергоресурсов', max_digits=12, decimal_places=2, null=True, default=0)

    class Meta:
        abstract = True


class BaseNaturalResource(models.Model):
    """
    Базовая модель министерств расходующих природные ресурсы.

    Наследуется моделями министерств расходующих природные ресурсы.
    """

    natural_resource_provision = models.IntegerField('Обеспечение природными ресурсами', null=True, blank=True, default=0, help_text='Обеспечение природными ресурсами')
    natural_resource_consumption = models.IntegerField('Потребление природных ресурсов', null=True, blank=True, default=0)
    natural_resource_costs = models.DecimalField('Финансовые затраты на приобретение природных ресурсов', max_digits=12, decimal_places=2, null=True, default=0)

    class Meta:
        abstract = True


class BaseAgro(models.Model):
    """
    Базовая модель министерств расходующих сельскохозяйственную продукцию.

    Наследуется моделями министерств расходующих сельскохозяйственную продукцию.
    """

    agro_provision = models.IntegerField('Обеспечение сельскохозяйственной продукцией', null=True, blank=True, default=0, help_text='Обеспечение сельскохозяйственной продукцией')
    agro_consumption = models.IntegerField('Потребление сельскохозяйственной продукцией', null=True, blank=True, default=0)
    agro_costs = models.DecimalField('Финансовые затраты на приобретение сельскохозяйственной продукции', max_digits=12, decimal_places=2, null=True, default=0)

    class Meta:
        abstract = True


class BaseGoods(models.Model):
    """
    Базовая модель министерств расходующих товары.

    Наследуется моделями министерств расходующих товары.
    """

    goods_provision = models.IntegerField('Обеспечение товарами', null=True, blank=True, default=0, help_text='Обеспечение товарами')
    goods_consumption = models.IntegerField('Потребление товаров', null=True, blank=True, default=0)
    goods_costs = models.DecimalField('Финансовые затраты на приобретение товаров', max_digits=12, decimal_places=2, null=True, default=0)

    class Meta:
        abstract = True


class BaseProduction(models.Model):
    """
    Базовая модель производственных министерств.

    Наследуется моделями министерств, где осуществляется производство
    продукции.
    """

    products_produced = models.IntegerField('Количество произведенной продукции', null=True, blank=True, default=0)
    cost_price = models.DecimalField('Себестоимость', max_digits=12, decimal_places=2, null=True, default=0)
    stake_gdp = models.DecimalField('Доля в ВВП', max_digits=5, decimal_places=3, null=True, default=0)

    class Meta:
        abstract = True


class MinistryPopulation(
    BaseMinistry,
    BaseAgro,
    BaseGoods,
    BaseEnergy,
    ExtendedBaseMinistry,
):
    """Министерство народонаселения."""

    social_benefits = models.DecimalField('Социальное пособие', max_digits=12, decimal_places=2, null=True, blank=True, default=0, help_text='Социальное пособие')
    education_decrease = models.DecimalField('Снижение уровня образования', max_digits=6, decimal_places=4, null=True, default=0)
    education_goods_contribution = models.IntegerField('Вклад товаров в образование', null=True, blank=True, default=0, help_text='Вклад товаров в образование')
    education_finance_contribution = models.DecimalField('Финансовые затраты на образование', max_digits=12, decimal_places=2, null=True, default=0)
    education_improving = models.DecimalField('Повышение уровня образования', max_digits=6, decimal_places=4, null=True, default=0)
    healthcare_decrease = models.DecimalField('Снижение уровня здравоохранения', max_digits=6, decimal_places=4, null=True, default=0)
    healthcare_goods_contribution = models.IntegerField('Вклад товаров в здравоохранения', null=True, blank=True, default=0, help_text='Вклад товаров в здравоохранения')
    healthcare_finance_contribution = models.DecimalField('Финансовые затраты на здравоохранения', max_digits=12, decimal_places=2, null=True, default=0)
    healthcare_improving = models.DecimalField('Повышение уровня здравоохранения', max_digits=6, decimal_places=4, null=True, default=0)

    class Meta(BaseMinistry.Meta):
        ...

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)

        if created:
            try:
                # Берем список групп рабочих из модуля константы
                groups: list = const.workers_groups
            except AttributeError as err:
                # Сделать логирование ошибки <--
                raise ConstantException(f'Ошибка {err}')

            # Создаем таблицы для распределения обучения рабочих
            for group in groups:
                Workers.objects.create(min_population=self, title=group)


class MinistryNaturalResources(
    BaseMinistry,
    ExtendedBaseMinistry,
    BaseEnergy,
    BaseWorkersEquipment,
    BaseProduction,
):
    """Министерство природных ресурсов и экологии."""

    resources_remaining = models.IntegerField('Остаток ресурсов', null=False, default=1000000, help_text='Остаток ресурсов')
    total_env_damage = models.DecimalField('Суммарный ущерб ОС от всех источников', max_digits=6, decimal_places=4, null=True, help_text='Суммарный ущерб окружающей среде от всех источников')
    damage_reduction_goods_contribution = models.IntegerField('Товарный вклад в снижение вреда ОС', null=True, blank=True, default=0, help_text='Товарный вклад в снижение вреда ОС')
    damage_reduction_finance_contribution = models.DecimalField('Финансовый вклад в снижение вреда ОС', max_digits=12, decimal_places=2, null=True, blank=True, default=0, help_text='Финансовый вклад в снижение вреда ОС')
    damage_env_reduction = models.DecimalField('Снижение ущерба ОС', max_digits=6, decimal_places=4, null=True, default=0, help_text='Снижение ущерба ОС')
    env_changing = models.DecimalField('Изменения состояния ОС', max_digits=6, decimal_places=4, null=True, default=0)

    class Meta(BaseMinistry.Meta):
        ...


class MinistryEnergy(
    BaseMinistry,
    ExtendedBaseMinistry,
    BaseWorkersEquipment,
    BaseEnergy,
    BaseNaturalResource,
    BaseProduction,
):
    """Министерство энергетики."""

    energy_efficiency_reduce = models.DecimalField('Снижение энергоэффективности', max_digits=5, decimal_places=3, null=True)
    energy_efficiency_goods_contribution = models.IntegerField('Товарный вклад в энергоэффективность', null=True, blank=True, default=0, help_text='Товарный вклад в энергоэффективность')
    energy_efficiency_finance_contribution = models.DecimalField('Финансовый вклад в энергоэффективность', max_digits=10, decimal_places=2, null=True, blank=True, default=0, help_text='Финансовый вклад в энергоэффективность')
    energy_efficiency_increase = models.DecimalField('Увеличение энергоэффективности', max_digits=5, decimal_places=3, null=True, default=0)

    class Meta(BaseMinistry.Meta):
        ...


class MinistryIndustry(
    BaseMinistry,
    ExtendedBaseMinistry,
    BaseWorkersEquipment,
    BaseEnergy,
    BaseNaturalResource,
    BaseProduction,
):
    """Министерство промышленности."""

    quality_manufactured_goods = models.DecimalField('Уровень качества производимых товаров', max_digits=6, decimal_places=4, null=True, help_text='Уровень качества производимых товаров')
    quality_reduce = models.DecimalField('Снижение качества производимых товаров', max_digits=6, decimal_places=4, null=True)
    quality_goods_contribution = models.IntegerField('Вклад товаров в увеличение качества производимых товаров', null=True, blank=True, default=0, help_text='Вклад товаров в увеличение качества производимых товаров')
    quality_finance_contribution = models.DecimalField('Финансовый вклад в увеличение качества производимых товаров', max_digits=12, decimal_places=2, null=True, default=0, help_text='Финансовый вклад в увеличение качества производимых товаров')
    quality_increase = models.DecimalField('Увеличение качества производимых товаров', max_digits=6, decimal_places=4, null=True, default=0)
    wasteless_production_level = models.DecimalField('Уровень безотходного производства', max_digits=6, decimal_places=4, null=True, help_text='Уровень безотходного производства')
    wasteless_production_reduce = models.DecimalField('Снижение уровня безотходного производства', max_digits=6, decimal_places=4, null=True)
    wasteless_production_goods_contribution = models.IntegerField('Вклад товаров в увеличение уровня безотходного производства', null=True, blank=True, default=0, help_text='Вклад товаров в увеличение уровня безотходного производства')
    wasteless_production_finance_contribution = models.DecimalField('Финансовый вклад в увеличение уровня безотходного производства', max_digits=12, decimal_places=2, null=True, default=0)
    wasteless_production_increase = models.DecimalField('Увеличение уровня безотходного производства', max_digits=6, decimal_places=4, null=True, default=0)

    class Meta(BaseMinistry.Meta):
        ...


class MinistryAgriculture(
    BaseMinistry,
    ExtendedBaseMinistry,
    BaseWorkersEquipment,
    BaseEnergy,
    BaseProduction,
):
    """Министерство сельского хозяйства."""

    quality_manufactured_food = models.DecimalField('Уровень качества производимых продуктов', max_digits=6, decimal_places=4, null=True, help_text='Уровень качества производимых продуктов')
    quality_reduce = models.DecimalField('Снижение качества производимых продуктов', max_digits=6, decimal_places=4, null=True)
    quality_goods_contribution = models.IntegerField('Вклад товаров в увеличение качества производимых продуктов', null=True, blank=True, default=0, help_text='Вклад товаров в увеличение качества производимых продуктов')
    quality_finance_contribution = models.DecimalField('Финансовый вклад в увеличение качества производимых продуктов', max_digits=12, decimal_places=2, null=True, default=0, help_text='Финансовый вклад в увеличение качества производимых продуктов')
    quality_increase = models.DecimalField('Увеличение качества производимых продуктов', max_digits=6, decimal_places=4, null=True, default=0)

    class Meta(BaseMinistry.Meta):
        ...


class MinistryTransport(
    BaseMinistry,
    ExtendedBaseMinistry,
    BaseWorkersEquipment,
    BaseEnergy,
):
    """Министерство транспорта."""

    transport_efficiency_level = models.DecimalField('Уровень транспортной эффективности', max_digits=6, decimal_places=4, null=True, help_text='Уровень транспортной эффективности')
    transport_efficiency_reduce = models.DecimalField('Снижение уровня транспортной эффективности', max_digits=6, decimal_places=4, null=True)
    transport_efficiency_goods_contribution = models.IntegerField('Вклад товаров в увеличение транспортной эффективности', null=True, blank=True, default=0, help_text='Вклад товаров в увеличение транспортной эффективности')
    transport_efficiency_finance_contribution = models.DecimalField('Финансовый вклад в увеличение транспортной эффективности', max_digits=12, decimal_places=2, null=True, default=0)
    transport_efficiency_increase = models.DecimalField('Увеличение транспортной эффективности', max_digits=6, decimal_places=4, null=True, default=0)
    transport_environmental_friendliness_level = models.DecimalField('Уровень экологичности транспорта', max_digits=6, decimal_places=4, null=True, help_text='Уровень экологичности транспорта')
    transport_environmental_friendliness_reduce = models.DecimalField('Снижение уровня экологичности транспорта', max_digits=6, decimal_places=4, null=True)
    transport_environmental_friendliness_goods_contribution = models.IntegerField('Вклад товаров в увеличение экологичности транспорта', null=True, blank=True, default=0, help_text='Вклад товаров в увеличение экологичности транспорта')
    transport_environmental_friendliness_finance_contribution = models.DecimalField('Финансовый вклад в увеличение экологичности транспорта', max_digits=12, decimal_places=2, null=True, default=0)
    transport_environmental_friendliness_increase = models.DecimalField('Увеличение экологичности транспорта', max_digits=6, decimal_places=4, null=True, default=0)

    class Meta(BaseMinistry.Meta):
        ...


class MinistryFinance(BaseMinistry):
    """Министерство финансов."""

    money = models.DecimalField(verbose_name='Финансы', max_digits=12, decimal_places=2, null=False, default=0)

    class Meta(BaseMinistry.Meta):
        ordering = ['period']


"""Список объектов создаваемых при создании игры"""
game_objects_list = [
    General,
    Happiness,
    Safety,
    Storage,

    MinistryPopulation,
    MinistryNaturalResources,
    MinistryEnergy,
    MinistryIndustry,
    MinistryAgriculture,
    MinistryTransport,
    MinistryFinance,
]


class Game(models.Model):
    """Модель игры."""

    creator = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name='games',
        verbose_name='Игра',
        help_text='Игра',
    )
    start_date = models.DateTimeField(
        'Дата и время начала игры',
        auto_now_add=True,
        null=False,
        blank=False,
    )
    finish_date = models.DateTimeField(
        'Дата и время завершения игры',
        auto_now=True,
        null=False,
        blank=False,
    )
    current_period = models.PositiveSmallIntegerField('Текущий период', null=False, default=1)
    game_over = models.BooleanField('Игра завершена', default=False)
    country_name = models.CharField('Название государства', max_length=50, unique=True)
    max_periods = models.IntegerField('Количество периодов в игре', null=False, default=10)

    class Meta:
        ordering = ['-finish_date']
        indexes = [
            models.Index(fields=['-finish_date'])
        ]

    def __str__(self):
        return f'{self.country_name}'

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)

        if created:
            try:
                # Количество периодов включает стартовый (нулевой) период
                periods: int = const.periods + 1
            except AttributeError as err:
                periods: int = self.max_periods + 1

            for obj in game_objects_list:
                for i in range(periods):
                    obj.objects.create(game=self, period=i)
