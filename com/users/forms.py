from django.contrib.auth.forms import UserCreationForm
from .models import User


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'
