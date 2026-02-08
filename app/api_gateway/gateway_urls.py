from django.urls import path, include

urlpatterns = [
    path('auth/', include('app.api_gateway.auth_urls')),
    path('api/products/', include('app.api_gateway.product_urls')),
    path('api/orders/', include('app.api_gateway.order_urls')),
]