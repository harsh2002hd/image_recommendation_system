from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.URLField()
    labels = models.TextField(help_text="Comma-separated labels for the image")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_label_list(self):
        """Return labels as a list"""
        return [label.strip() for label in self.labels.split(',')]

class Collection(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, through='CollectionImage')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"

class CollectionImage(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    # 1 for liked, 3 for starred
    interaction_type = models.IntegerField(choices=[(1, 'Liked'), (3, 'Starred')])
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('collection', 'image')
    
    def __str__(self):
        return f"{self.collection.name} - {self.image.title}"

class RecommendationSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference_images = models.ManyToManyField(Image, related_name='reference_for_sessions')
    recommended_images = models.ManyToManyField(Image, through='Recommendation', related_name='recommended_in_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Recommendation for {self.user.username} at {self.created_at}"

class Recommendation(models.Model):
    session = models.ForeignKey(RecommendationSession, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    similarity_score = models.FloatField()
    position = models.IntegerField(help_text="Position in the recommendation list (1 is most similar)")
    added_to_collection = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['position']
    
    def __str__(self):
        return f"Recommendation: {self.image.title} (Score: {self.similarity_score})"