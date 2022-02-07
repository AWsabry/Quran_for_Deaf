from django.contrib import admin
from users.models import CustomUser
from Deaf_Website.models import Word, WordUser

# Register your models here.

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    model = Word
    list_display = ('id','name', 'slug' , 'active', 'created')
    list_display_links = ('name',)
    list_filter = ('user', 'name', 'slug' , 'active', 'created')
    list_editable = ('active',)
    fieldsets = (
        (None, {"fields": (
                'user', 'name', 'slug', 'description', 'image', 'video', 'active', 'updated', 'created'
            )})),

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user' and not request.user.is_superuser:
            # setting the user from the request object
            kwargs['initial'] = request.user.id
            # making the field readonly
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_readonly_fields(self, request, obj=None):
        obj = obj.user if obj else request.user
        if request.user.is_superuser:
            return self.readonly_fields + ('slug', 'updated', 'created')
        if  request.user == obj:
            return self.readonly_fields + ('slug','active', 'updated', 'created')
        else:
            return self.readonly_fields + ('user', 'name', 'slug', 'description', 'image', 'video', 'active', 'updated', 'created')        
        
        return self.readonly_fields
    
@admin.register(WordUser)
class WordUserAdmin(admin.ModelAdmin):
    model = WordUser