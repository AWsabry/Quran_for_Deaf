from django.contrib import admin

from Deaf_Website.models import Word, WordUser

# Register your models here.

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    model = Word
    list_display = ('id','name', 'slug' , 'active', 'created')
    list_display_links = ('name',)
    list_filter = ('name', 'slug' , 'active', 'created')
    list_editable = ('active',)
    fieldsets = (
        (None, {"fields": (
                'user', 'name', 'slug', 'description', 'image', 'video', 'active', 'updated', 'created'
            )})),
        
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or request.user == obj.user:
            return self.readonly_fields + ('slug', 'updated', 'created')
        else:
            return self.readonly_fields + ('user', 'name', 'slug', 'description', 'image', 'video', 'active', 'updated', 'created')        
        
        return self.readonly_fields
    
@admin.register(WordUser)
class WordUserAdmin(admin.ModelAdmin):
    model = WordUser