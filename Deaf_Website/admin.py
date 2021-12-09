from django.contrib import admin

from Deaf_Website.models import Category, PendingUploads, Results, TeacherProfile, UploadedImage, UploadedVideo

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "created", "brand")
    list_display = ('name', "created", "id", 'brand','active')
    
class UploadedVideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "created",)
    list_display = ('name', "category", "id", 'created','counter','PositiveFeedBack','NegativeFeedBack','active')
    

class UploadedImagesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "created",)
    list_display = ('name', "category", "id", 'created','counter','PositiveFeedBack','NegativeFeedBack','active')


class TeacherProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('username',), }
    list_filter = ("username",)
    list_display = ('username', "FirstName", "LastName", 'Age','last_modified','PhoneNumber','last_modified','active')


class PendingUploadsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "created",)
    list_display = ('name', "category", "id", 'created','counter','PositiveFeedBack','NegativeFeedBack','active')
    


class ResultsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_filter = ("name", "created",)
    list_display = ('name', "category", "id", 'created','counter','PositiveFeedBack','NegativeFeedBack','Confrimed')




admin.site.register(TeacherProfile,TeacherProfileAdmin)
admin.site.register(UploadedVideo,UploadedVideoAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(UploadedImage,UploadedImagesAdmin)
admin.site.register(PendingUploads,PendingUploadsAdmin)
admin.site.register(Results,ResultsAdmin)