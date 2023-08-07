# default imports
from django.contrib import admin

# import models
from user.models.user import MyUser

class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

admin.site.register(MyUser, MyUserAdmin)
