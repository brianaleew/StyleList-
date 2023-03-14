from django.contrib import admin
from .models import Apparel, Outfit, User 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from main_app.models import UserProfile

# Register your models here.
admin.site.register(Apparel)

admin.site.register(Outfit)

# 
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False 
    verbose_name_plural = 'user profile'

# 
class UserAdmin(BaseUserAdmin): 
    inlines = (UserProfileInline,)


# Re-register UserAdmin with new info 
admin.site.unregister(User)
admin.site.register(User, UserAdmin)