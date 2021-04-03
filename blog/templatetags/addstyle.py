from django import template
register = template.Library()


@register.filter(name='addstyle')
def addstyle(field, style):
    return field.as_widget(attrs={"class": style})
