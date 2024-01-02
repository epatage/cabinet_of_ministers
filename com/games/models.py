import modulefinder
from django.db.models.signals import post_save
from django.dispatch import receiver

import games.constants as const

from django.db import models
from users.models import User





class Period(models.Model):
    """
    Модель периода (игрового года).

    Сочетание объекта игры к которому относиться период
    и номера периода должно быть уникальным.
    """

    game = models.ForeignKey(
        'Game',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='periods',
        verbose_name='Годовой период',
        help_text='Годовой период',
    )
    number = models.PositiveSmallIntegerField('Номер периода', default=0, null=False, blank=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['game', 'number'],
    #             name='unique_game_number'
    #         )
    #     ]

    def __str__(self):
        return f'{self.game.country_name} - {self.number}'


class General(models.Model):
    """
    Общие показатели.

    Отображены основные показатели, напрямую касающиеся населения
    по результатам решений за игровой период.
    """

    population = models.PositiveIntegerField('Население', null=False, default=0)
    education = models.DecimalField('Уровень образования населения', max_digits=5, decimal_places=2, null=True, blank=True)
    healthcare = models.DecimalField('Уровень здравоохранения', max_digits=5, decimal_places=2, null=True, blank=True)
    living_cost = models.DecimalField('Прожиточный минимум', max_digits=7, decimal_places=2, null=True, blank=True)
    birth_rate = models.DecimalField('Уровень рождаемости', max_digits=7, decimal_places=1, null=True, blank=True)
    mortality_rate = models.DecimalField('Уровень смертности', max_digits=7, decimal_places=1, null=True, blank=True)
    natural_environment = models.DecimalField('Окружающая среда', max_digits=5, decimal_places=4, null=True, blank=True)
    transport_efficiency = models.DecimalField('Транспортная эффективность', max_digits=5, decimal_places=3, null=True, blank=True)
    energy_efficiency = models.DecimalField('Энергетическая эффективность', max_digits=5, decimal_places=3, null=True, blank=True)
    gdp = models.PositiveIntegerField('ВВП', null=True, blank=True)
    gdp_per_soul = models.DecimalField('ВВП на душу населения (абсолютный показатель)', max_digits=7, decimal_places=3, null=True, blank=True)
    population_on_social_security = models.PositiveIntegerField('Количество населения на социальном обеспечении', null=True, blank=True)


class Welfare(models.Model):
    """Благосостояние населения."""

    welfare_level = models.DecimalField('Уровень благосостояния', max_digits=5, decimal_places=3, null=True, blank=True)
    general = models.OneToOneField('General', verbose_name='Общие показатели', on_delete=models.CASCADE, null=False, blank=False)


class GroupIncomeLevel(models.Model):
    """
    Уровень дохода по группам населения.

    Поле title заполняется при создании объекта из списка групп населения.
    """

    title = models.CharField('Группа населения', max_length=50, null=False)
    group_share = models.DecimalField('Доля группы населения в общем количестве', max_digits=5, decimal_places=4, null=True, blank=True)
    average_income = models.DecimalField('Средний доход на человека', max_digits=7, decimal_places=2, null=True, blank=True)
    walfare = models.ForeignKey(
        'Welfare',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='groups_population',
        verbose_name='Благосостояние',
        help_text='Благосостояние',
    )


class Happiness(models.Model):
    """Индекс счастья."""

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
    period = models.OneToOneField(
        'Period',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='happiness',
        verbose_name='Период',
        help_text='Период', )

    def __str__(self):
        return f'{self.period.game.country_name} - {self.period.number} - {self.index}'


class Safety(models.Model):
    """Безопасность и уверенности в завтрашнем дне."""

    index = models.DecimalField('Индекс безопасности', max_digits=5, decimal_places=2, null=True, blank=True)
    environment = models.DecimalField('Окружающая среда', max_digits=5, decimal_places=2, null=True, blank=True)
    remaining_resources = models.DecimalField('Остаток ресурсов', max_digits=12, decimal_places=2, null=True, blank=True)
    food_security = models.DecimalField('Продовольственная безопасность', max_digits=5, decimal_places=2, null=True, blank=True)
    food_reserve = models.DecimalField('Продовольственный резерв', max_digits=5, decimal_places=2, null=True, blank=True)
    food_quality = models.DecimalField('Качество продовольствия', max_digits=5, decimal_places=2, null=True, blank=True)
    national_debt = models.DecimalField('Государственный долг', max_digits=5, decimal_places=2, null=True, blank=True)
    happiness = models.OneToOneField(
        'Happiness',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='happiness_safety',
        verbose_name='Безопасность',
        help_text='Безопасность', )

    def __str__(self):
        return f'{self.happiness.period.game.country_name} - {self.happiness.period.number} - {self.index}'


class Workers(models.Model):
    """
    Рабочие.

    Распределение рабочих по специальностям.
    """

    title = models.CharField('Название профиля образования', max_length=50, null=False, blank=False)
    workers_part = models.PositiveSmallIntegerField('Доля работников')
    number_workers = models.PositiveIntegerField('Количество работников отрасли')
    min_population = models.OneToOneField(
        'MinistryPopulation',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='workers',
        verbose_name='Рабочие по группам образования',
        help_text='Рабочие по группам образования', )


class Warehouse(models.Model):
    """Хранилище финансов и материальных запасов."""

    # Переделывать!

    title = models.CharField('Название', max_length=50, null=False, blank=False)
    amount = models.IntegerField('Количество', null=False, blank=True, default=0)
    avg_price = models.DecimalField('Цена за единицу', max_digits=5, decimal_places=2, null=True, blank=True)
    quality = models.DecimalField('Качество', max_digits=5, decimal_places=2, null=True, blank=True)
    amount_finance = models.DecimalField('Финансовый параметр', max_digits=12, decimal_places=2, null=True, blank=True)
    remaining_resources = models.PositiveIntegerField('Остаток ресурсов', default=1000000)
    period = models.ForeignKey(
        'Period',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='warehouses',
        verbose_name='Период',
        help_text='Период', )

    def __str__(self):
        return f'{self.period.game.country_name} - {self.period.number} - {self.title}'


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


class BaseWorkersMinistry(BaseMinistry):
    """
    Базовая модель министерств с сотрудниками.

    Наследуется моделями министерств, где задействованы сотрудники
    и оборудование.
    """

    number_workers = models.IntegerField('Количество работников', null=False, blank=True, default=0, help_text='Количество работников')
    equipment_amount = models.IntegerField('Количество оборудования', null=False, blank=True, default=0)
    equipment_quality = models.DecimalField('Качество оборудования', max_digits=5, decimal_places=3, null=False, default=0)
    # Необходимо проверить как работает при искусственном увеличении себестоимости до предельных размеров
    equipment_price = models.DecimalField('Цена оборудования', max_digits=8, decimal_places=3, null=False, default=0)
    salary_fund = models.DecimalField('Фонд заработной платы', max_digits=10, decimal_places=2, null=False, blank=True, default=0)
    energy_provision = models.DecimalField('Энергоснабжение', max_digits=10, decimal_places=2, null=False, blank=True, default=0)

    class Meta(BaseMinistry.Meta):
        abstract = True


class BaseProductionMinistry(BaseWorkersMinistry):
    """
    Базовая модель производственных министерств.

    Наследуется моделями министерств, где осуществляется производство
    продукции.
    """

    # Поля производства продукции

    amount_products_produced = models.IntegerField('Количество произведенной продукции', null=False, blank=True, default=0)

    class Meta(BaseWorkersMinistry.Meta):
        abstract = True


class MinistryPopulation(BaseMinistry):
    """Министерство народонаселения."""

    ...

    class Meta(BaseMinistry.Meta):
        ...


class MinistryNaturalResources(BaseProductionMinistry):
    """Министерство природных ресурсов и экологии."""

    ...

    class Meta(BaseProductionMinistry.Meta):
        ...


class MinistryEnergy(BaseProductionMinistry):
    """Министерство энергетики."""

    ...

    class Meta(BaseProductionMinistry.Meta):
        ...


class MinistryIndustry(BaseProductionMinistry):
    """Министерство промышленности."""

    ...

    class Meta(BaseProductionMinistry.Meta):
        ...


class MinistryAgriculture(BaseProductionMinistry):
    """Министерство сельского хозяйства."""

    ...

    class Meta(BaseProductionMinistry.Meta):
        ...


class MinistryTransport(BaseWorkersMinistry):
    """Министерство транспорта."""

    ...

    class Meta(BaseWorkersMinistry.Meta):
        ...


class MinistryFinance(BaseMinistry):
    """Министерство финансов."""

    money = models.DecimalField(verbose_name='Финансы', max_digits=12, decimal_places=2, null=False, default=0)

    class Meta(BaseMinistry.Meta):
        ordering = ['period']


"""Список объектов создаваемых при создании игры"""
game_objects_list = [
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
    current_period = models.PositiveSmallIntegerField('Текущий период', default=1)
    game_over = models.BooleanField('Игра завершена', default=False)
    country_name = models.CharField('Название государства', max_length=50, unique=True)

    class Meta:
        ordering = ['-finish_date']

    def __str__(self):
        return f'{self.country_name}'

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)

        if created:
            # Количество периодов включает стартовый (нулевой) период
            periods = const.periods + 1

            for obj in game_objects_list:
                for i in range(periods):
                    obj.objects.create(game=self, period=i)
