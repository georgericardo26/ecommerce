from django.utils import timezone
from django.conf import settings
import os
from uuid import uuid4


def path_and_rename(instance, filename, upload_to):
    ext = filename.split('.')[-1]

    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)

    fullname = os.path.join(settings.MEDIA_ROOT + '/' + upload_to,
                            filename)
    if os.path.exists(fullname):
        os.remove(fullname)

    return os.path.join(upload_to, filename)


def path_and_rename_product(instance, filename):
    upload_to = 'images/product'
    return path_and_rename(instance, filename, upload_to)


def delete_image_file(obj):
        try:
            this = obj
            if this.image and this.image != self.image:
                if os.path.isfile(this.image.path):
                    os.remove(this.image.path)
        except Exception as e:
            pass
