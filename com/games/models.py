import modulefinder

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
    current_round = models.PositiveSmallIntegerField()
    game_over = models.BooleanField('Игра завершена', default=False)
    country_name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['-finish_date']

    def __str__(self):
        return f'{self.country_name}'


class Round(models.Model):
    """Модель раунда (игрового года) игры."""

    game = models.ForeignKey(
        'Game',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='rounds',
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
    )
    gdp_per_soul = models.DecimalField(
        'ВВП на душу населения',
        max_digits=20,
        decimal_places=2,
    )
    joblessness = models.DecimalField('Безработица', max_digits=5, decimal_places=2)
    birth_rate = models.DecimalField('Рождаемость', max_digits=5, decimal_places=2)
    mortality_rate = models.DecimalField('Смертность', max_digits=5, decimal_places=2)
    education = models.DecimalField('Образованность', max_digits=5, decimal_places=2)
    welfare = models.DecimalField('Благосостояние', max_digits=5, decimal_places=2)
    transport_accessibility = models.DecimalField('Транспортная доступность', max_digits=5, decimal_places=2)
    goods_provision = models.DecimalField('Обеспеченность товарами', max_digits=5, decimal_places=2)
    energy_provision = models.DecimalField('Обеспеченность энергоресурсами', max_digits=5, decimal_places=2)
    safety = models.DecimalField('Безопасность', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.index


class Safety(models.Model):
    """Модель безопасности и уверенности в завтрашнем дне."""

    index = models.DecimalField('Индекс безопасности', max_digits=5, decimal_places=2)
    environment = models.DecimalField('Окружающая среда', max_digits=5, decimal_places=2)
    remaining_resources = models.PositiveIntegerField('Окружающая среда', default=1000000)
    food_security = models.DecimalField('Продовольственная безопасность', max_digits=5, decimal_places=2)
    food_reserve = models.DecimalField('Продовольственный резерв', max_digits=5, decimal_places=2)
    food_quality = models.DecimalField('Качество продовольствия', max_digits=5, decimal_places=2)
    national_debt = models.DecimalField('Государственный долг', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.index


class Warehouse(models.Model):
    """Хранилище финансов и материальных запасов."""

    round = models.ForeignKey(
        'Round',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='warehouses',
        verbose_name='Хранилище',
        help_text='Хранилище финансов и материальных запасов', )
    finance = models.DecimalField('Финансы', max_digits=12, decimal_places=2)
    natural_resources = models.ForeignKey(
        'NaturalResources',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='natural_resources',
        verbose_name='Природные ресурсы',
        help_text='Природные ресурсы',
    )
    energy = models.ForeignKey(
        'Energy',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='energy',
        verbose_name='Энергоресурсы',
        help_text='Энергоресурсы',
    )
    goods = models.ForeignKey(
        'Goods',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='goods',
        verbose_name='Товары',
        help_text='Товары и оборудование',
    )
    food = models.ForeignKey(
        'Food',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='food',
        verbose_name='Продукты питания',
        help_text='Продукты питания',
    )
    national_debt = models.DecimalField('Финансы', max_digits=12, decimal_places=2)


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
