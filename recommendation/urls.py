from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('browse/', views.browse_images, name='browse_images'),
    path('star-image/', views.star_image, name='star_image'),
    path('like-image/', views.like_image, name='like_image'),
    path('recommendations/', views.generate_recommendations, name='generate_recommendations'),
    path('next/<int:session_id>/<int:current_position>/', views.next_recommendation, name='next_recommendation'),
    path('similar/<int:image_id>/', views.get_similar_image, name='get_similar_image'),
    path('add-to-collection/', views.add_to_collection, name='add_to_collection'),
    path('create-collection/', views.create_collection, name='create_collection'),
    path('remove-all-starred-liked/', views.remove_all_starred_liked, name='remove_all_starred_liked'),
]