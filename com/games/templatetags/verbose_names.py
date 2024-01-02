from django import template
register = template.Library()


@register.simple_tag(name='vn')
def get_verbose_field_name(instance, field_name):
    """
    Возвращает verbose_name в поле.
    """
    return instance._meta.get_field(field_name).verbose_name.title()
