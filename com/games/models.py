import modulefinder
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from users.models import User


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


class Period(models.Model):
    """Модель периода (игрового года)."""

    game = models.ForeignKey(
        'Game',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='periods',
        verbose_name='Годовой период',
        help_text='Годовой период',
    )
    number = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.game.country_name} - {self.number}'


class Happiness(models.Model):
    """Модель индекса счастья."""

    index = models.DecimalField(
        'Индекс счастья',
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )
    gdp_per_soul = models.DecimalField(
        'ВВП на душу населения',
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
    """Модель безопасности и уверенности в завтрашнем дне."""

    index = models.DecimalField('Индекс безопасности', max_digits=5, decimal_places=2, null=True, blank=True)
    environment = models.DecimalField('Окружающая среда', max_digits=5, decimal_places=2, null=True, blank=True)
    remaining_resources = models.DecimalField('Остаток ресурсов', max_digits=12, decimal_places=2, null=True, blank=True)
    food_security = models.DecimalField('Продовольственная безопасность', max_digits=5, decimal_places=2, null=True, blank=True)
    food_reserve = models.DecimalField('Продовольственный резерв', max_digits=5, decimal_places=2, null=True, blank=True)
    food_quality = models.DecimalField('Качество продовольствия', max_digits=5, decimal_places=2, null=True, blank=True)
    national_debt = models.DecimalField('Государственный долг', max_digits=5, decimal_places=2, null=True, blank=True)
    period = models.OneToOneField(
        'Period',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='safety',
        verbose_name='Период',
        help_text='Период', )

    def __str__(self):
        return f'{self.period.game.country_name} - {self.period.number} - {self.index}'


class Warehouse(models.Model):
    """Хранилище финансов и материальных запасов."""

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


class BaseResources(models.Model):
    """
    Базовая модель ресурсов игры.

    Наследуется моделями с параметрами 'Количество' и 'Средняя цена'
    """

    amount = models.IntegerField()
    avg_price = models.DecimalField('Средняя цена за единицу', max_digits=5, decimal_places=2)


class NaturalResources(BaseResources):
    """Модель природных ресурсов."""


class Energy(BaseResources):
    """Модель энергоресурсов."""


class Goods(models.Model):
    """Модель товаров и оборудования."""

    quality = models.DecimalField('Качество товаров', max_digits=5, decimal_places=2)


class Food(models.Model):
    """Модель продуктов питания."""

    quality = models.DecimalField('Качество продуктов питания', max_digits=5, decimal_places=2)


class BaseMinistry(models.Model):
    """Базовая модель министерства."""

    number_workers = models.IntegerField()
    number_equipment = models.IntegerField()

    class Meta:
        abstract = True


class MinistryEducationLaborSocialProtection(models.Model):
    """Министерство образования, труда и социальной защиты."""

    ...


class MinistryNaturalResources(BaseMinistry):
    """Министерство природных ресурсов и экологии."""

    ...


class MinistryEnergy(BaseMinistry):
    """Министерство энергетики."""

    ...


class MinistryIndustry(BaseMinistry):
    """Министерство промышленности."""

    ...


class MinistryAgriculture(BaseMinistry):
    """Министерство сельского хозяйства."""

    ...


class MinistryTransport(BaseMinistry):
    """Министерство транспорта."""

    ...


class MinistryFinance(BaseMinistry):
    """Министерство финансов."""

    ...
