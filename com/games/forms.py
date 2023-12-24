from django import forms
from .models import Game, Period, Happiness


class GameCreateForm(forms.ModelForm):
    """Форма создания игры."""

    class Meta:
        model = Game
        fields = ('country_name',)
        labels = {
            'country_name': 'Название государства',
        }


class MainForm(forms.Form):
    class Meta:
        model = Period
        fields = '__all__'
        # labels = {
        #     'country_name': 'Название государства',
        # }

class HappynessForm(forms.Form):
    class Meta:
        model = Happiness
        fields = '__all__'
        # labels = {
        #     'country_name': 'Название государства',
        # }