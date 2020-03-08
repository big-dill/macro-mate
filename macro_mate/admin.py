from django.contrib import admin
from macro_mate.models import User_Profile

from macro_mate.models import Meal
# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoryAdmin():
    admin.site.register(User_Profile)

    admin.site.register(Meal)
