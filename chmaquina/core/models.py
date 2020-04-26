from django.db import models


def custom_upload_to(instance, filename):
    old_instance = ArchivosCh.objects.get(pk=instance.pk)
    old_instance.archivo.delete()
    return 'archivosCh/' + filename


# Create your models here.

class ArchivosCh(models.Model):
    
    archivo = models.FileField(upload_to=custom_upload_to, null=True, blank =True)
    #memoria = models.IntegerField(null=True, blank =True)
    #kernel = models.IntegerField(null=True, blank =True)

    #nombre = archivo.name
        #archivo = models.FileField(upload_to='archivosCh/', null=True, blank =True)