from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


# Define an inline admin descriptor for Employee model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# register Profile
admin.site.register(Profile)
