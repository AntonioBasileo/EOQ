from django.urls import path, include

from app.view.order_view import OrderView, OrderAllListView, OrderByUserView

urlpatterns = [
    path('<int:pk>', OrderView.as_view(), name='order-view'),
    path('create-order', OrderView.as_view(), name='orders-view-create-order'),
    path('get-all', OrderAllListView.as_view(), name='orders-view-get-all'),
    path('my-orders', OrderByUserView.as_view(), name='orders-view-my-orders'),
    path('delete-order/<int:pk>', OrderView.as_view(), name='orders-view-delete-order')
]