from django.urls import path, include

from app.view.product_view import ProductView, ProductDetailView

urlpatterns = [
    path('<int:pk>', ProductView.as_view(), name='product-view'),
    path('create-product', ProductView.as_view(), name='products-view-create-product'),
    path('get-all', ProductDetailView.as_view(), name='product-detail-view-all'),
    path('update-product', ProductDetailView.as_view(), name='product-detail-view-update'),
    path('delete-product', ProductDetailView.as_view(), name='product-detail-view-delete'),
]