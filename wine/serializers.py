from django.contrib.auth.models import User, Group
from . import models
from rest_framework import serializers
import xmlrpclib
import datetime
import xmlrpclib, httplib


url = "http://winetest.polarwin.cn/"
db = 'newera'
username = 'admin'
password = 'admin'
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
model = 'res.partner'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
'''
class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = res.partner
        fields = ('name', 'city','id')
       #fields= '__all__'
'''       