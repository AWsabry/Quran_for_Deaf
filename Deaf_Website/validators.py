import os
from django.core.exceptions import ValidationError
from Quran_for_Deaf import settings

def _ext_photo(file):
    extension = os.path.splitext(file.name)[1]
    allowed_ext = settings.ALLOWED_EXT_PHOTO
    
    if extension not in allowed_ext:
        raise ValidationError('the allowed extensions only are jpg, jpeg.')
    
    if file.size > settings.MAXIMUM_SIZE_ALLOWED_PHOTO:
        raise ValidationError(f'maximum allowed size is {settings.MAXIMUM_SIZE_ALLOWED_PHOTO/(1024 * 1024)} MB.')

def _ext_video(file):
    extension = os.path.splitext(file.name)[1]
    allowed_ext = settings.ALLOWED_EXT_VIDEO
    
    if extension not in allowed_ext:
        raise ValidationError('the allowed extensions only are mp4.')
    
    if file.size > settings.MAXIMUM_SIZE_ALLOWED_VIDEO:
        raise ValidationError(f'maximum allowed size is {settings.MAXIMUM_SIZE_ALLOWED_VIDEO/(1024 * 1024)} MB.')