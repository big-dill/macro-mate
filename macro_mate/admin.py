from django.contrib import admin
from macro_mate.models import UserProfile 

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display= ('title', 'category', 'url')

class CategoryAdmin():
    admin.site.register(UserProfile)