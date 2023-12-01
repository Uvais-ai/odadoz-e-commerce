from django.db import models

# Create your models here.
class Contact(models.Model):
    name= models.CharField(max_length=300)
    email= models.EmailField()
    subject= models.CharField(max_length=500)
    message= models.TextField()

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name
    
