from django.contrib import admin

from .models import Game, Round, Happiness, Safety, Warehouse, NaturalResources, Energy, Goods, Food


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'creator',
        'start_date',
        'finish_date',
        'current_round',
        'game_over',
        'country_name',
    )
    search_fields = ('country_name', 'creator')
    list_filter = ('start_date', 'finish_date', 'game_over')
    empty_value_display = '-'
    list_editable = ('country_name',)
