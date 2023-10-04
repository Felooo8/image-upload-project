from django.contrib import admin
from django.contrib.auth.models import User
from .models import Account, Tier, Image, ThumbnailImage

# Register your models here.

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'account'

class UserAdmin(admin.ModelAdmin):
    inlines = (AccountInline,)

class TierAdmin(admin.ModelAdmin):
    pass

class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'upload_timestamp', 'user')
    list_filter = ('upload_timestamp', 'user')
    search_fields = ('upload_timestamp', 'image', 'user__username')

class ThumbnailImageAdmin(admin.ModelAdmin):
    
    list_display = ('__str__', 'original_image', 'thumbnail_size', 'get_user_username')
    list_filter = ('thumbnail_size', 'original_image__user')
    search_fields = ('original_image__user__username',)

    def get_user_username(self, obj):
        return obj.original_image.user.username

    get_user_username.admin_order_field = 'original_image__user__username'
    get_user_username.short_description = 'Original Image User'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tier, TierAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ThumbnailImage, ThumbnailImageAdmin)