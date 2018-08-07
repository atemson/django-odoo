# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User, Group
from . import models
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer
from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DeleteView, DetailView
import xmlrpclib
import datetime
import xmlrpclib, httplib
from django.views.decorators.csrf import csrf_protect
from wine.forms import CustomerForm
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from xmlrpclib import Marshaller

import json
# Create your views here.


def dump_decimal(value, write):
    write("<value><double>")
    write(str(value))
    write("</double></value>\n")

Marshaller.dispatch[Decimal] = dump_decimal


url = "http://winetest.polarwin.cn/"

db = 'newera'
username = 'admin'
password = 'admin'
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
model = 'res.partner'


partners = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[]],
{'fields': ['name', 'city','email','phone'], 'limit': 100})
for partner in partners:
    print partner['id'], partner['name'], partner['city'], partner['email'], partner['phone']


'''
 ************************CUSTOMER / PARTNER PAGE (MODULE)*************************************

'''
class CustomerForm(ModelForm):


    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'res.partner'

    fields = ['name', 'city', 'email', 'phone']
    


def customer(request):
    t = get_template('customer.html')
    html = t.render({'partners':partners})
    return HttpResponse(html)

def customer_list(request, template_name='customer_list.html'):
    partner = 'res.partner'.objects.all()
    data = {}
    data['object_list'] = partner
    return render(request, template_name, data)


def updatec(request, id):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'res.partner'
    partners = model.objects.get(pk=id)
    partner.name = request.POST.get('name')
    partner.city = request.POST.get('city')
    partner.email = request.POST.get('email')
    partner.phone = request.POST.get('phone')
    partner.save()
    return HttpResponse('updated')



@csrf_exempt
def delete(request):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'res.partner'
    partners = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[]],
    {'fields': ['name', 'city','email','phone'], 'limit': 5})
    for partner in partners:
        '''
        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])
        return HttpResponse("Partner deleted")    
        print id
        '''
        id = partner['id']
        if id:
            print partner['id']
        else:
            results = sock.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])

        return HttpResponse("Partner deleted")
        
        '''
        names = partner['name']

        args = [[['id','=',partner['id']]]]
        ids = models.execute_kw(db, uid, password,
                'res.partner', 'search', [[['name','=',partner['name']]]])
        #ids = ids[0] if ids else False
        if ids:
            ids = ids[0]
            print ids
            
        else:
        #ids=[121]
           results = sock.execute_kw(db, uid, password, 'res.partner', 'unlink', [[ids]])
        '''
        
        #return HttpResponse("Partner deleted")
    #results = sock.execute(db, uid, password, 'res.partner', 'unlink', ids)
      

def createcustomer(request):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'res.partner'
    partner = {}
    fields = ['name']
    fields = ['city']
    fields = ['email']
    fields = ['phone']
    success_url = reverse_lazy('customer')
    partner_id = sock.execute(db, uid, password, 'res.partner', 'create', partner)
    print partner_id


'''
 ***************************HOME / INDEX PAGE (MODULE)****************************************

'''
@csrf_exempt
def index(request):

    #partners = model.objects.all()
    view = "index"
    t = get_template('index.html')
    html = t.render({'name':view})
    return HttpResponse(html)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



'''
 ***************************PRODUCT PAGE (MODULE)************************************

'''
@csrf_exempt
def product(request):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'product.template'


    products = models.execute_kw(db, uid, password,
    'product.template', 'search_read',
    [[]],
    {'fields': ['name', 'product_color','product_vintage','product_grade','type','list_price'], 'limit': 500})
    for product in products:
        print product['id'], product['name'], product['product_color'], product['product_vintage'], product['product_grade'], product['type'], product['list_price']

        t = get_template('product.html')
        html = t.render({'products':products})
        return HttpResponse(html)

class ProductList(ListView):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model ='product.template'

class ProductView(DetailView):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'product.template'

class ProductCreate(CreateView):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'product.template'
    fields = ['name', 'product_color','product_vintage','product_grade','type','list_price']
    success_url = reverse_lazy('product_list')

class ProductUpdate(UpdateView):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'product.template'
    fields = ['name', 'product_color','product_vintage','product_grade','type','list_price']
    success_url = reverse_lazy('product_list')

class ProductDelete(DeleteView):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'product.template'
    success_url = reverse_lazy('product_list')


'''
 **************************************SALE ORDER PAGE (MODULE)******************************

'''
@csrf_exempt
def sale(request):
    url = "http://winetest.polarwin.cn/"

    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'sale.order.line'


    sales = models.execute_kw(db, uid, password,
    'sale.order.line', 'search_read',
    [[]],
    {'fields': ['name', 'product_uom_qty','price_unit','price_subtotal', 'price_total','product_id' ], 'limit': 500})
    for sale in sales:
        print sale['id'], sale['name'], sale['product_uom_qty'], sale['price_unit'], sale['price_subtotal'], sale['price_total'], sale['product_id']

        t = get_template('sales.html')
        html = t.render({'sales':sales})
        return HttpResponse(html)




'''
 ********************************PURCHASE ORDER PAGE (MODULE)************************************
'''
@csrf_exempt
def purchase(request):
    url = "http://winetest.polarwin.cn/"

    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'purchase.order.line'


    purchases = models.execute_kw(db, uid, password,
    'purchase.order.line', 'search_read',
    [[]],
    {'fields': ['name', 'product_qty','price_unit','qty_invoiced','order_id', 'price_subtotal', 'price_total' ], 'limit': 500})
    for purchase in purchases:
        print purchase['id'], purchase['name'], purchase['product_qty'], purchase['qty_invoiced'],purchase['price_unit'], purchase['price_subtotal'], purchase['price_total'], purchase['order_id']

        t = get_template('purchase.html')
        html = t.render({'purchases':purchases})
        return HttpResponse(html)






'''
*******************************************************************************************
'''



class CustomerUpdate(UpdateView):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'res.partner'

    fields = ['name']
    fields = ['city']
    fields = ['email']
    fields = ['phone']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('customer')
