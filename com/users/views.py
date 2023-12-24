from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .forms import CreationForm
from .models import User
from django.contrib.auth.decorators import login_required


class SignUp(CreateView):
    """Авторизация пользователя."""

    form_class = CreationForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/signup.html'


@login_required()
def users_list(request):
    """Список зарегистрированных пользователей."""

    users = User.objects.all()

    context = {
        'users': users,
    }
    return render(request, 'users/users_list.html', context)


@login_required()
def profile(request, user_id):
    """
    Профайл пользователя.

    На странице выводятся все игры (активные и завершенные)
    данного пользователя.
    Можно посмотреть подробную информацию по завершенным играм и
    продолжить незавершенную игру.
    """

    user = get_object_or_404(User, pk=user_id)
    games = user.games.filter(creator=user)

    context = {
        'user': user,
        'games': games,
    }
    return render(request, 'users/profile.html', context)
