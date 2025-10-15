import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'img_recommendation_system.settings')
django.setup()

from recommendation.models import Image
from django.contrib.auth.models import User

# Create sample images with labels
sample_images = [
    {
        'title': 'Mountain Landscape at Sunset',
        'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'mountain, sunset, landscape, nature, peak, outdoors, scenic, golden hour'
    },
    {
        'title': 'Forest Path with Sunlight',
        'image_url': 'https://images.unsplash.com/photo-1448375240586-882707db888b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'forest, trees, path, sunlight, nature, green, woodland, peaceful, natural light'
    },
    {
        'title': 'Starry Night Sky with Milky Way',
        'image_url': 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'stars, night sky, milky way, galaxy, cosmos, dark, astronomy, celestial'
    },
    {
        'title': 'Ocean Waves at Golden Hour',
        'image_url': 'https://images.unsplash.com/photo-1505228395891-9a51e781003f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'ocean, waves, water, beach, golden hour, sunset, coastal, blue, sea'
    },
    {
        'title': 'Desert Dunes at Sunrise',
        'image_url': 'https://images.unsplash.com/photo-1509316785289-025f5b8b4c06?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'desert, dunes, sand, sunrise, landscape, arid, golden, vast, natural'
    },
    {
        'title': 'Snowy Mountain Peak',
        'image_url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'snow, mountain, peak, winter, cold, landscape, white, alpine, scenic'
    },
    {
        'title': 'Autumn Forest with Colored Leaves',
        'image_url': 'https://images.unsplash.com/photo-1503418700-2b0e4d7a5b6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'forest, autumn, leaves, trees, colorful, nature, fall, orange, red, seasonal'
    },
    {
        'title': 'City Skyline at Night',
        'image_url': 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'city, skyline, night, buildings, urban, lights, modern, architecture, metropolitan'
    },
    {
        'title': 'Tropical Beach with Palm Trees',
        'image_url': 'https://images.unsplash.com/photo-1505228395891-9a51e781003f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'beach, ocean, palm trees, tropical, sand, vacation, paradise, blue, seaside'
    },
    {
        'title': 'Northern Lights in the Sky',
        'image_url': 'https://images.unsplash.com/photo-1476820865390-c52aeebb9891?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'northern lights, aurora, night sky, green, nature, phenomenon, arctic, colorful, natural'
    },
    {
        'title': 'Wildlife Photography - Lion',
        'image_url': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'lion, wildlife, animal, safari, africa, predator, mammal, big cat, nature'
    },
    {
        'title': 'Abstract Art Painting',
        'image_url': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'abstract, art, painting, colorful, creative, modern, artistic, expression, design'
    },
    {
        'title': 'Coffee and Croissant on Table',
        'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'coffee, croissant, breakfast, food, cafe, morning, pastry, french, bakery'
    },
    {
        'title': 'Vintage Camera on Table',
        'image_url': 'https://images.unsplash.com/photo-1516035733009-6923a180903a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'camera, vintage, photography, equipment, retro, analog, classic, technology, hobby'
    },
    {
        'title': 'Yoga Practice in Nature',
        'image_url': 'https://images.unsplash.com/photo-1549272620-5c9d1d6b1a0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'yoga, meditation, nature, wellness, exercise, mindfulness, outdoor, healthy, lifestyle'
    },
    {
        'title': 'Modern Architecture Building',
        'image_url': 'https://images.unsplash.com/photo-1494972308805-463bc619d34e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'architecture, building, modern, design, structure, urban, contemporary, skyscraper, city'
    },
    {
        'title': 'Delicious Pizza with Toppings',
        'image_url': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'pizza, food, italian, cheese, tomato, meal, delicious, restaurant, cuisine'
    },
    {
        'title': 'Cute Cat Sleeping',
        'image_url': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'cat, pet, animal, cute, sleeping, furry, domestic, mammal, adorable'
    },
    {
        'title': 'Colorful Flower Garden',
        'image_url': 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'flowers, garden, colorful, nature, bloom, petals, plants, spring, botanical'
    },
    {
        'title': 'Vintage Car on Road',
        'image_url': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
        'labels': 'car, vintage, automobile, classic, road, vehicle, retro, transportation, luxury'
    }
]

# Create the images in the database
for img_data in sample_images:
    image, created = Image.objects.get_or_create(
        title=img_data['title'],
        defaults={
            'image_url': img_data['image_url'],
            'labels': img_data['labels']
        }
    )
    if created:
        print(f"Created image: {image.title}")
    else:
        print(f"Image already exists: {image.title}")

print("Sample data creation completed!")