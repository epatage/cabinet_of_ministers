from django.contrib import admin

from .models import Game, Happiness, Safety, Warehouse, MinistryNaturalResources, MinistryFinance, MinistryPopulation, \
    Workers


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'creator',
        'start_date',
        'finish_date',
        'current_period',
        'game_over',
        'country_name',
    )
    search_fields = ('country_name', 'creator')
    list_filter = ('start_date', 'finish_date', 'game_over')
    empty_value_display = '-'
    list_editable = ('country_name',)



admin.site.register(Warehouse)

admin.site.register(Happiness)
admin.site.register(Safety)
admin.site.register(MinistryPopulation)
admin.site.register(Workers)
admin.site.register(MinistryNaturalResources)
admin.site.register(MinistryFinance)
