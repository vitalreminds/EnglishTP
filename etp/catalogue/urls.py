from django.urls import path, include
from .views import CatalogueListView, BookDetailView,BookCreate, BookUpdate, BookDelete, BookOrder


# Urls

catalogue_patterns = ([ 
    path('', CatalogueListView.as_view(), name='books'),
    path('create/', BookCreate.as_view(), name='create'),
    path('update/P<pk>/', BookUpdate.as_view(), name='update'),
    path('delete/P<pk>/', BookDelete.as_view(), name='delete'),
    path('order/P<id>/', BookOrder, name='order'),   
       
],'catalogue')