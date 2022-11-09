from rest_framework import serializers
from .models import Advertisement
from django.shortcuts import resolve_url


class AdvertisementFilterSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('image_url')
    href = serializers.SerializerMethodField('url')

    def image_url(self, obj):
        images = obj.images.all()[:1]
        if len(images) > 0:
            return images[0].img.url
        else:
            return ''

    def url(self, obj):
        return resolve_url('advertisement', obj.header, obj.pk)

    class Meta:
        model = Advertisement
        fields = ['header', 'image', 'href']
