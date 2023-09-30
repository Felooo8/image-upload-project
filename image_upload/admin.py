from django.contrib import admin
from django.contrib.auth.models import User
from .models import Account, Tier

# Register your models here.

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'account'

class UserAdmin(admin.ModelAdmin):
    inlines = (AccountInline,)

class TierAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tier, TierAdmin)