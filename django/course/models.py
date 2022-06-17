from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100,null=True)
    age = models.PositiveIntegerField(null=True)
    linkedin = models.CharField(max_length=100,null=True)
    learningpath=models.CharField(max_length=100,null=True,blank=True)
    user_cv =models.FileField(null=True)

    def __str__(self):
        return '{}.{}'.format(self.id,self.name)

# tag
class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Course(models.Model):
    CATEGORIES = (
        ("ML","Machine Learning"),
        ("CC","Cloud Computing"),
        ("AD","Android Developer"),
        ("ID","iOS Developer"),
    )
    name = models.CharField(max_length=100,null=True)
    id = models.PositiveIntegerField(primary_key=True)
    tags  = models.ManyToManyField(Tag,null=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    category =  models.CharField(max_length=50,null=True,choices=CATEGORIES)
    datecreated = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return '{}.{}'.format(self.id,self.name)    

class Order(models.Model):
    STATUS = (
        ('On Progress','On Progress'),
        ('Finished','Finished')
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Course,null=True,on_delete=models.SET_NULL)
    #datecreated = models.DateField(auto_now_add=True,null=True)
    status = models.CharField(null=True,max_length=50,choices=STATUS)

    def __str__(self):
        return '{}.{}'.format(self.id,self.product.name) 
