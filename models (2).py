from django.db import models


# Create your models here.
class Product(models.Model):
    prod_id = models.AutoField
    prod_name = models.CharField(max_length=20)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.prod_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")

    desc = models.CharField(max_length=3000)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5200, default="")
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=45, default="")
    address = models.CharField(max_length=505, default="")
    zip_code = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    phone = models.IntegerField(default=0)
    amount= models.IntegerField(default=0)


class Orderupdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=500)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "......"
