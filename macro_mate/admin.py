from django.contrib import admin

from macro_mate.models import Comment, MealCategory, Meal, UserProfile

# Admin page not really live, just used for debugging.


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoryAdmin():
    admin.site.register(Comment)
    admin.site.register(Meal)
    admin.site.register(MealCategory)
    admin.site.register(UserProfile)
