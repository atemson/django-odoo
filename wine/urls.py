from django.conf.urls import url, include
from . import views
from rest_framework import routers
from django.views.generic import TemplateView



router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
#router.register(r'index', views.IndexView)

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^customer/$', views.customer, name='customer'),
    url(r'^product/$', views.product, name='product'),
    url(r'^sale/$', views.sale, name='sale'),
    url(r'^purchase/$', views.purchase, name='purchase'),
    url(r'^delete/$', views.delete, name='delete'),
    # url(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name='delete_view'),   
    #url(r'^delete/$', views.CustomerDelete.as_view(), name='delete'),
    #url(r'^(?P<pk>\d+)/delete/$', views.CustomerDelete.as_view(), name='delete'),
    #url(r'^update/(?P<id>[0-9]+)/$', views.updatec, name='update'),
    #url(r'^$', views.PartnerListView.as_view(), name='list'),
    url(r'^', include(router.urls)),
   
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
