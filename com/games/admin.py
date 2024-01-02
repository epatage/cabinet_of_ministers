from django.contrib import admin

from .models import Game, Period, Happiness, Safety, Warehouse, MinistryNaturalResources, MinistryFinance


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


admin.site.register(Period)

admin.site.register(Warehouse)

admin.site.register(Happiness)
admin.site.register(Safety)
admin.site.register(MinistryNaturalResources)
admin.site.register(MinistryFinance)
