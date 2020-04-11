from django.db import models


# Create your models here.

class ArchivosCh(models.Model):
    archivo = models.FileField(upload_to='archivosCh/', null=True, blank =True)
    
