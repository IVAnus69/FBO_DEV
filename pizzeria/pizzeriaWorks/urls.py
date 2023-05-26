from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import Ajax2View

urlpatterns = [
    # path('', views.index, name='home'),
    path('registration/', views.registration, name='registration'),
    path('authentication/', views.auth, name='auth'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.close_log, name='logout'),
    path('', views.product_view, name='products'),
    path('products/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('ajax/example2/', Ajax2View.as_view(), name='ajax_example2'),
    path('baskets/add/<int:product_id>',views.basket_add, name='basket_add'),
    path('baskets/remove/<int:product_id>', views.basket_remove, name='basket_remove'),
    path('modal-product/<int:product_id>/', views.modalproduct, name='modal-product'),
    path('user/make-order', views.make_order, name='make-order'),
    path('setCookies', views.setCookies),
    path('ajax/resp', views.ajax_resp)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)