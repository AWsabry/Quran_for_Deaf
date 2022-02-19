from django.contrib import admin
from users.models import CustomUser
from Deaf_Website.models import Word, WordUser
from django.db.models import Q

# Register your models here.

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    model = Word
    list_display = ('id','name', 'slug' , 'active', 'created')
    list_display_links = ('name',)
    list_filter = ('user', 'user__is_teacher', 'user__is_superuser', 'name', 'active', 'created')
    list_editable = ('active',)
    
    def get_fieldsets(self, request, obj=None):
        self.fieldsets = [
            (None, {"fields": (
                'user', 'name', 'slug', 'description', 'image', 'video', 'active', 'updated', 'created'
            )})]
        
        if obj:
            if obj.word_attach:
                self.fieldsets.append(('Attached Word', {'fields': ('word_attach',)}))
        
        return self.fieldsets
    
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
            return self.readonly_fields + ('slug', 'updated', 'created', 'word_attach')
        if  request.user == obj:
            return self.readonly_fields + ('slug','active', 'updated', 'created', 'word_attach')
        else:
            return self.readonly_fields + ('user', 'name', 'slug', 'description', 'image', 'video', 'active', 'updated', 'created', 'word_attach')        

@admin.register(WordUser)
class WordUserAdmin(admin.ModelAdmin):
    model = WordUser
    list_display = ('id',)
    filter_horizontal = ('vote_approved', 'vote_denied')

    def save_model( self, request, obj, form, change):
        if request.user.is_teacher:
            if obj.vote_teacher:
                if request.user in obj.vote_denied.all():
                    obj.vote_denied.remove(request.user)
                obj.vote_approved.add(request.user)
            else:
                if request.user in obj.vote_approved.all():
                    obj.vote_approved.remove(request.user)
                obj.vote_denied.add(request.user)
        else:
            obj.save()

    def get_fieldsets(self, request, obj=None):
        self.fieldsets = [
            (None, {"fields": (
                    'user', 'word', 'image', 'video', 'vote_approved', 'vote_denied','vote_nothing' 
                )}),
            ('Voting Results', {'fields': ( 'vote_percentage', 'teacher_approved', 'teacher_denied', 'teacher_num')})
        ]
        
        if obj:
            if request.user.is_teacher:
                self.fieldsets.append(('Voting', {'fields': ('vote_teacher',)}))
                if request.user in obj.vote_approved.all():
                    obj.vote_teacher = True
                elif request.user not in obj.vote_approved.all() and request.user not in obj.vote_denied.all():
                    obj.vote_teacher = None
                else:
                    obj.vote_teacher = False
            
            if request.user:
                obj.teacher_approved = obj.vote_approved.exclude(is_superuser=True).count()
                obj.teacher_denied = obj.vote_denied.exclude(is_superuser=True).count()
                obj.teacher_num = CustomUser.objects.filter(is_teacher=True, is_active=True).count()
                
                teachers = CustomUser.objects.filter(Q(is_teacher=True) | Q(is_superuser=True))
                teachers_votes = obj.vote_approved.all()
                percentage = (teachers_votes.count()/teachers.count())*100 #teachers.difference(teachers_votes).count()
                obj.vote_percentage = f'{round(percentage,1)} %'

                nothing = CustomUser.objects.filter(Q(is_teacher=True, is_active=True) & ~Q(email__in=obj.vote_approved.all().values('email')) & ~Q(email__in=obj.vote_denied.all().values('email')))
                obj.vote_nothing.set(nothing)
            
            obj.save()
            
            
        return self.fieldsets

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(WordUserAdmin, self).get_form(request, obj, **kwargs)
        if obj and request.user.is_teacher:
            if request.user not in obj.vote_approved.all() and request.user not in obj.vote_denied.all():
                form.base_fields['vote_teacher'].help_text = 'لم يتم التصويت بعد'
        return form

    def get_readonly_fields(self, request, obj=None):
        obj = obj.user if obj else request.user
        if request.user.is_superuser:
            return self.readonly_fields + ('vote_nothing', 'vote_percentage', 'teacher_approved', 'teacher_denied', 'teacher_num')
        if  request.user.is_teacher:
            return self.readonly_fields + ('user', 'word', 'image', 'video', 'vote_approved', 'vote_denied','vote_nothing', 'vote_percentage', 'teacher_approved', 'teacher_denied', 'teacher_num')
        else:
            return self.readonly_fields + ('user', 'word', 'image', 'video', 'vote_approved', 'vote_denied','vote_nothing', 'vote_percentage', 'teacher_approved', 'teacher_denied', 'teacher_num')       

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):     
        if db_field.name == 'vote_approved' or db_field.name == 'vote_denied':
            kwargs["queryset"] = CustomUser.objects.filter(Q(is_teacher=True, is_active=True) | Q(is_superuser=True)).order_by('-is_superuser')
        
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs["queryset"] = CustomUser.objects.filter(is_teacher=False, is_superuser=False, is_active=True)
        
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)