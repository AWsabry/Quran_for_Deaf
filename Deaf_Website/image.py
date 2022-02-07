from moviepy.editor import VideoFileClip
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile


def image_thumbnail(video_file):

    clips = VideoFileClip(video_file.path)
    frames = clips.reader.fps
    duration = int(clips.duration) + 1

    cut = clips.get_frame(duration//2)
    image = Image.fromarray(cut)
    file = BytesIO()
    image.save(file, format='JPEG')
    django_file = ContentFile(file.getvalue())
    return django_file