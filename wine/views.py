# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
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
from django.views.generic import ListView, DeleteView
import xmlrpclib
import datetime
import xmlrpclib, httplib
from django.views.decorators.csrf import csrf_protect


# Create your views here.

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
 CUSTOMER / PARTNER PAGE (MODULE)

'''



def customer(request):    
    t = get_template('customer.html')
    html = t.render({'partners':partners})
    return HttpResponse(html)
    # return render(request,'templates/index.html',{'partners':partners})
    # html = "<html><body><h1>Odoo Partner</h1>"
    # for partner in partners:

    #     print(partner)
    #     name = partner['name'].encode("utf-8")
    #     html += "<div>"+name+": "+str(partner['city'])+" "+str(partner['email'])+" "+str(partner['phone'])+" "+str(partner['id'])+"</div>"
    #     html += "</body></html>"
    #     print("---------------------")
    #     # return HttpResponse(partner)
    #     return HttpResponse(html)
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

def deletec(request, id):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'res.partner'
    #partners = model.objects.get(pk=id)
    partners = get_object_404(model,pk=partner.id)    
    partner.delete()
    return HttpResponse('deleted')
    

class CustomerDelete(DeleteView):
    url = "http://winetest.polarwin.cn/"
    db = 'newera'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    sock = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'res.partner'
    template_name ='templates/delete.html'
    Context_object_name = 'partner'
    success_url = reverse_lazy('customer')
    
    '''   
    def delete(request, id):
        partners = model.objects.filter(id=id).delete()

        for partner in partners:
            partner.delete()
            return HttpResponse('deleted')   
    '''   

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

    t = get_template('delete.html')
    html = t.render({'partners':partners})
    return HttpResponse(html)



'''
 HOME / INDEX PAGE (MODULE)

'''

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
 PRODUCT PAGE (MODULE)

'''

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




'''
 SALE ORDER PAGE (MODULE)

'''
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
 PURCHASE ORDER PAGE (MODULE)

'''
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



