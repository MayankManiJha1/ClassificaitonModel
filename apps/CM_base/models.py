from django.db import models

# Create your models here.

class ModelDB(models.Model):
    unique_id=models.CharField(name='KEY_ID',max_length=15,primary_key=True)
    Task_NM=models.CharField(name='Task_NM',max_length=50,blank=False,null=False)
    CREATE_TIME=models.DateTimeField(name='CREATE_TIME',blank=False,null=False)
    CLOSED_TIME=models.DateTimeField(name='CLOSED_TIME',blank=True,null=True)
    NW_ID=models.CharField(name='NW_ID',max_length=50,blank=True,null=True)
    FUSION_ID=models.CharField(name='FUSION_ID',max_length=20,blank=True,null=True)
    META=models.TextField(name='META',null=True)
    INFO=models.TextField(name='TSK_INFO',null=False)
    STATUS=models.CharField(name='STATUS',max_length=50,null=False,blank=False)
    RESULT_STATUS=models.CharField(name='RESULT_STATUS',max_length=20,null=True,blank=True)

    class Meta:
        app_label='apps.CM_base'
        db_table='"RPA"."ML_CL_TASK_INFO"'
    