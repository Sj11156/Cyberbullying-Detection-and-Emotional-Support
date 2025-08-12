from django.db import models

class pmodel(models.Model):
    pos = models.CharField(max_length=100)
    userid = models.CharField(max_length=50)
    nme = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    post_image= models.FileField(upload_to='pictures')
    class Meta:
        db_table = "postadd"

		
class smodel(models.Model):
    uid = models.CharField(max_length=100)
    p_image= models.FileField(upload_to='profile')
    class Meta:
        db_table = "p_image"
class PredictionDetail(models.Model):
    pos = models.CharField(max_length=222)
    prediction = models.CharField(max_length=34)
    probability = models.CharField(max_length=34)
    time_of_visit = models.DateTimeField()
    userid = models.CharField(max_length=50)

    class Meta:
        db_table = "prediction_details"