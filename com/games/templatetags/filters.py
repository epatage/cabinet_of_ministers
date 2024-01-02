from django import template

register = template.Library()


@register.filter(name='translator')
def translator(obj: str, dic: dict) -> str:
    """Фильтр для перевода полей в таблицах."""

    show = obj
    for key, val in dic.items():
        if obj == key:
            show = val
            break

    return show
