from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('game_nick', 'tel', 'admin')
    list_filter = ('admin', 'staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'game_nick', 'tel', 'password', 'avatar',)}),
        # ('Full name', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'guild_member', 'staff', 'is_active',)}),
        ('Мессенджеры', {'fields': ('whatsapp_boolean', 'telegram_boolean', 'telegram_name', 'viber_boolean')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'tel', 'game_nick', 'password1', 'password2')}
         ),
    )
    search_fields = ('tel', 'game_nick',)
    ordering = ('tel',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
