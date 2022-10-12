from django.db import models
from django.contrib.auth.models import AbstractUser

class Advertisement(models.Model):
    header = models.CharField(max_length=200)
    descriptions = models.TextField()
    images = models.ManyToManyField('ImagesAdvertisement')
    price = models.IntegerField()
    sity = models.ForeignKey('Sity',on_delete=models.SET(None))
    site = models.CharField(max_length=1000)
    category = models.ForeignKey('Category',on_delete=models.SET(None))

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"

    def __str__(self):
        return self.header


class ImagesAdvertisement(models.Model):
    img = models.ImageField(upload_to="AdvertisementImages",null=False,blank=False)

    class Meta:
        verbose_name = "ImagesAdvertisement"
        verbose_name_plural = "ImagesAdvertisements"

    def __str__(self):
        return self.img.url


class Sity(models.Model):
    sity = models.CharField(max_length=30)
    img = models.ImageField(upload_to="SityImage", null=True, blank=False)

    class Meta:
        verbose_name = "Sity"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.sity


class Category(models.Model):
    category = models.CharField(max_length=100)
    img = models.ImageField(upload_to="CategoryImages",null=True,blank=False)
    parent = models.ForeignKey('Category',on_delete=models.SET(None),related_name='Category_parent',null=True,blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class User(AbstractUser):
    img = models.ImageField(upload_to='UserImg', default='UserImg/user.png', null=True, blank=True)

    def __str__(self):
        return self.username