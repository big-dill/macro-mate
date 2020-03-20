from django import template

register = template.Library()

# From https://stackoverflow.com/questions/401025/define-css-class-in-django-forms
# Allows aa filter to add css classes to any elements contained in a template tag
@register.filter(name='addcss')
def addcss(value, arg):
    css_classes = value.field.widget.attrs.get('class', '').split(' ')
    if css_classes and arg not in css_classes:
        css_classes = '%s %s' % (css_classes, arg)
    return value.as_widget(attrs={'class': css_classes})
