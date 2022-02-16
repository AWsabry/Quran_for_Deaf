from django.contrib import admin
from users.models import CustomUser
from Deaf_Website.models import Word, WordUser
from django.db.models import Q
from django.forms import ValidationError

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

@admin.register(WordUser)
class WordUserAdmin(admin.ModelAdmin):
    model = WordUser
    list_display = ('id',)
    filter_horizontal = ('vote_approved', 'vote_denied')
    
    def save_model( self, request, obj, form, change):
        print('#####save_modle######')
        print(obj.vote_approved.all())
        print(obj.vote_denied.all())
        
        if request.user.is_teacher:
            if obj.vote_teacher:
                obj.vote.add(request.user)
            else:
                obj.vote.remove(request.user)
        else:
            obj.save()
    
    def get_fieldsets(self, request, obj=None):
        self.fieldsets = [
            (None, {"fields": (
                    'user', 'word', 'image', 'video', 'vote_approved', 'vote_denied' 
                )}),
            ('Voting Results', {'fields': ( 'vote_percentage', 'teacher_approved', 'teacher_denied', 'teacher_num')})
        ]
        if obj:
            if request.user.is_teacher:
                self.fieldsets.append(('Voting', {'fields': ('vote_teacher',)}))
                check_vote_teacher = True if request.user in obj.vote.all() else False
                obj.vote_teacher = check_vote_teacher
            
            if request.user:
                obj.teacher_approved = obj.vote_approved.all().count()
                obj.teacher_denied = obj.vote_denied.all().count()
                obj.teacher_num = CustomUser.objects.filter(is_teacher=True).count()
            
            obj.save()
            
            
        return self.fieldsets
    
    def get_readonly_fields(self, request, obj=None):
        obj = obj.user if obj else request.user
        if request.user.is_superuser:
            return self.readonly_fields + ('vote_percentage', 'teacher_approved', 'teacher_denied', 'teacher_num')
        if  request.user.is_teacher:
            return self.readonly_fields + ('user', 'word', 'image', 'video', 'vote_approved', 'vote_denied', 'vote_percentage', 'teacher_approved', 'teacher_denied', 'teacher_num')
        else:
            return self.readonly_fields + ('user', 'word', 'image', 'video', 'vote_approved', 'vote_denied', 'vote_percentage', 'teacher_approved', 'teacher_denied', 'teacher_num')       


    def formfield_for_manytomany(self, db_field, request=None, **kwargs):     
        if db_field.name == 'vote_approved' or db_field.name == 'vote_denied':
            kwargs["queryset"] = CustomUser.objects.filter(Q(is_teacher=True) | Q(is_superuser=True)).order_by('-is_superuser')
        
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs["queryset"] = CustomUser.objects.filter(is_teacher=False, is_superuser=False, is_active=True)
        
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)