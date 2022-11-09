from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver


class Advertisement(models.Model):
    header = models.CharField(max_length=200)
    descriptions = models.TextField()
    images = models.ManyToManyField('ImagesAdvertisement')
    price = models.IntegerField()
    sity = models.ForeignKey('Sity', on_delete=models.SET(None))
    site = models.CharField(max_length=1000)
    category = models.ForeignKey('Category', on_delete=models.SET(None))
    autor = models.ForeignKey('User', on_delete=models.SET(None), null=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.SET(None), null=True, blank=True,
                                related_name='company_advertisement')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"

    def __str__(self):
        return self.header


class ImagesAdvertisement(models.Model):
    img = models.ImageField(upload_to="AdvertisementImages", null=False, blank=False)

    class Meta:
        verbose_name = "ImagesAdvertisement"
        verbose_name_plural = "ImagesAdvertisements"


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
    img = models.ImageField(upload_to="CategoryImages", null=True, blank=False)
    parent = models.ForeignKey('Category', on_delete=models.SET(None), related_name='Category_parent', null=True,
                               blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class User(AbstractUser):
    img = models.ImageField(upload_to='UserImg', default='UserImg/user.png', null=True, blank=True)
    companies = models.ManyToManyField('Company', null=True, blank=True)

    def __str__(self):
        return self.username


class Company(models.Model):
    logo = models.ImageField(upload_to='Company_logo', null=True, blank=False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    contact_phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=False, blank=False, default='')
    advertisements = models.ManyToManyField('Advertisement', null=True, blank=True, related_name='advertisementCompany')

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=ImagesAdvertisement)
def images_advertisement_delete(sender, instance, **kwargs):
    instance.img.delete()


@receiver(pre_delete, sender=Advertisement)
def images_advertisement_delete(sender, instance, **kwargs):
    for i in instance.images.all():
        i.delete()


@receiver(pre_delete, sender=Company)
def old_images_company_delete(sender, instance, **kwargs):
    try:
        old_instance = Company.objects.get(id=instance.pk)
        if old_instance.logo:
            old_instance.logo.delete(False)
    except Company.DoesNotExist:
        pass


@receiver(pre_save, sender=Company)
def old_images_company_delete(sender, instance, **kwargs):
    try:
        old_instance = Company.objects.get(id=instance.pk)
        if old_instance.logo != instance.logo:
            old_instance.logo.delete(False)
    except Company.DoesNotExist:
        pass


@receiver(pre_save, sender=User)
def old_images_company_delete(sender, instance, **kwargs):
    try:
        old_instance = User.objects.get(id=instance.pk)
        if old_instance.img:
            old_instance.img.delete(False)
    except User.DoesNotExist:
        pass
