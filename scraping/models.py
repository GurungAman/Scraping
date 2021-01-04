from django.db import models

# Create your models here.
class details(models.Model):
    url         = models.URLField(max_length=100)
    is_complete = models.BooleanField(default=False)
    count_js    = models.IntegerField()
    count_image = models.IntegerField()
    count_css   =  models.IntegerField(default=0)

    def __str__(self):
        return self.url

