from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_view, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    path('subcategories/', views.subcategory_view, name='subcategory-list'),
    path('subcategories/<int:pk>/', views.subcategory_detail, name='subcategory-detail'),
    path('contents/<int:pk>/', views.content_detail, name='content-detail'),  
    path('contents/', views.content_create_by_subcategory, name='content-create-by-subcategory'),  
    path('contents/all/', views.content_get_all, name='content_get_all'),
    path('comments/content/<int:content_id>/', views.add_comment, name='add-comment'),
    path('comments/<int:id>/', views.comment_detail, name='comment_detail'),
]
