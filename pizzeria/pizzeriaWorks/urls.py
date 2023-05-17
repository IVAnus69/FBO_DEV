from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    # path('', views.index, name='home'),
    path('registration/', views.registration, name='registration'),
    path('authentication/', views.auth, name='auth'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.close_log, name='logout'),
    path('', views.product_view, name='products'),
    path('products/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)