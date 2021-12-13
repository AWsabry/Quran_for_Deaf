from django.contrib import admin
from users.models import AccessToken, CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser', 'is_teacher')
    list_filter = ('email', 'is_active', 'is_staff', 'is_superuser', 'is_teacher')
    fieldsets = (
        ('General', {"fields": (
                'email', 'password', 'first_name', 'last_name', 'country'
            )}),
        ('Permissions', {'fields': (
            'is_superuser', 'groups', 'user_permissions'
        )}),
        ('Confirmation', {'fields': (
            'is_staff', 'is_active', 'is_teacher'
        )}),
        ('DateTime', {'fields': (
            'date_joined', 'last_login'
        )}),
        ('Questions', {'fields': (
            'question_one', 'question_two', 'question_three'
        )})
    )
    
    readonly_fields = ('date_joined','groups')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    search_fields = ('email',)
    ordering = ('email',)

class AccessTokenAdmin(admin.ModelAdmin):
    model = CustomUser
    fieldsets = (
        (None, {"fields": (
                'user', 'token', 'expires', 'created'
            )}),
    )
    readonly_fields = ('token','created')
    list_display = ('user', 'token', 'created')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)