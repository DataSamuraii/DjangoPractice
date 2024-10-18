from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html

from .models import User, UnbanRequest


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_banned', 'last_login', 'date_joined')
    list_filter = ('is_banned', 'last_login', 'date_joined')
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'is_banned')}),
        ('System Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ('username', )

    # Override the readonly fields to prevent non-superusers from editing critical permissions
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            readonly_fields += ('is_superuser', 'user_permissions', 'groups')
        return readonly_fields


class UnbanRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'linked_username', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'text')
    readonly_fields = ('text',)
    ordering = ('-date',)

    def linked_username(self, obj):
        link = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', link, obj.user.username)
    linked_username.short_description = 'User'


admin.site.register(User, UserAdmin)
admin.site.register(UnbanRequest, UnbanRequestAdmin)
