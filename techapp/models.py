from django.db import models

# Create your models here.
class Projects(models.Model):
    project_name       = models.CharField(max_length=100)
    project_reason     = models.CharField(max_length=100)
    project_type       = models.CharField(max_length=100)
    project_division   = models.CharField(max_length=100)
    project_category   = models.CharField(max_length=100)
    project_priority   = models.CharField(max_length=100)
    project_department = models.CharField(max_length=100)
    project_start_date = models.CharField(max_length=100)
    project_end_date   = models.CharField(max_length=100)
    project_location   = models.CharField(max_length=100)
    project_status     = models.CharField(max_length=100)








   