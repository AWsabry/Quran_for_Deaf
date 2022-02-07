from django.contrib import admin
from Deaf_Website.models import Word
from users.models import AccessToken, CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser', 'is_teacher')
    list_filter = ('email', 'is_active', 'is_staff', 'is_superuser', 'is_teacher')
    
    readonly_fields = ('date_joined','groups')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    def save_model(self, request, obj, form, change):
    # Override this to set the password to the value in the field if it's
    # changed.
        if change:
            orig_obj = CustomUser.objects.filter(pk=obj.pk)[0]
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()
    
    def get_fieldsets(self, request, obj=None):
        self.fieldsets = [
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
        ]
        if obj:
            if obj.is_teacher:
                self.fieldsets.append(('Teacher', {'fields': ('Age', 'PhoneNumber', 'ProfilePic', 'Experience', 'CV')}))
            
        return self.fieldsets
        
        # return [(None, {'fields': self.get_fields(request, obj)})]
        
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