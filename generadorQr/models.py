from django.db import models

# Create your models here.

from django.db import models

class QRCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    qr_image = models.ImageField(upload_to='qr_codes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
