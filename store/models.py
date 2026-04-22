from django.db import models
import datetime
# Create your models here.

#categories of Products
class Category(models.Modelodel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


#Customers
class Customer(models.Modelodel):
 first_name= models.CharField(max_length=50)
 last_name= models.CharField(max_length=50)
 phone= models.CharField(max_length=10)
 email= models.EmailField(max_length=50)
 password= models.CharField(max_length=50)
 

 def __str__(self):
    return f'{self.first_name} {self.last_name}'


class Product(models.Modelodel):
   name=models.CharField(max_length=100)
   price=models.DecimalField(default=0, decimal_places=2 , max_digit=6)
   category=models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
   description=models.CharField(max_length=250, default='', blank=True, null=True)
   image=models.ImageField(upload_to='uploads/product')

   def __str__(self):
        return self.name





class Order(models.Modelodel):