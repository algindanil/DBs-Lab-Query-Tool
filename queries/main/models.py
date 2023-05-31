from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

from django.db import models
from django.urls import reverse

class JeweleryPiece(models.Model):
    piece_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    categories = models.ManyToManyField('Category', through='CategoryPiece', blank=True)
    maker_country = models.CharField(max_length=100)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('edit_jewelerypiece', kwargs={'pk': self.piece_id})
    
    def get_deletion_url(self):
        return reverse('delete_jewelerypiece', kwargs={'pk': self.piece_id})
    


class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    measurement_unit = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('edit_material', kwargs={'pk': self.material_id})
    
    def get_deletion_url(self):
        return reverse('delete_material', kwargs={'pk': self.material_id})


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey('Client', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50)

    def get_absolute_url(self):
       return reverse('edit_order', kwargs={'pk': self.order_id})

    def get_deletion_url(self):
        return reverse('delete_order', kwargs={'pk': self.order_id})


class OrderDetails(models.Model):
    details_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    piece_id = models.ForeignKey('JeweleryPiece', on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    def get_absolute_url(self):
        return reverse('edit_orderdetails', kwargs={'pk': self.details_id})
    
    def get_deletion_url(self):
        return reverse('delete_orderdetails', kwargs={'pk': self.details_id})


class Client(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('edit_client', kwargs={'pk': self.client_id})
    
    def get_deletion_url(self):
        return reverse('delete_cleint', kwargs={'pk': self.client_id})



class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('edit_category', kwargs={'pk': self.category_id})
    
    def get_deletion_url(self):
        return reverse('delete_category', kwargs={'pk': self.category_id})


    
class CategoryPiece(models.Model):
    category_piece_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    piece_id = models.ForeignKey('JeweleryPiece', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category_id.name} - {self.piece_id.name}'

