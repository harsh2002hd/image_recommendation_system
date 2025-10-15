from django.contrib import admin
from .models import Image, Collection, CollectionImage, RecommendationSession, Recommendation

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'labels')
    list_filter = ('created_at',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at', 'user')

@admin.register(CollectionImage)
class CollectionImageAdmin(admin.ModelAdmin):
    list_display = ('collection', 'image', 'interaction_type', 'added_at')
    list_filter = ('interaction_type', 'added_at')

@admin.register(RecommendationSession)
class RecommendationSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active', 'user')

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('session', 'image', 'similarity_score', 'position', 'added_to_collection')
    list_filter = ('added_to_collection', 'position')