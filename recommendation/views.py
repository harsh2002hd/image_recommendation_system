from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Image, Collection, CollectionImage, RecommendationSession, Recommendation
import json

# Import our new services
from .services import PollinationsAIService, calculate_cosine_similarity

def dashboard(request):
    """Main dashboard view"""
    # If user is not authenticated, redirect to admin login
    if not request.user.is_authenticated:
        return redirect('/admin/login/?next=/')
    
    # Get user's collections
    collections = Collection.objects.filter(user=request.user)
    
    # Get reference images (starred and liked)
    reference_images = []
    collection_images = CollectionImage.objects.filter(
        collection__user=request.user
    ).select_related('image')
    
    for ci in collection_images:
        reference_images.append({
            'image': ci.image,
            'weight': ci.interaction_type  # 1 for liked, 3 for starred
        })
    
    context = {
        'collections': collections,
        'reference_images': reference_images
    }
    return render(request, 'recommendation/dashboard.html', context)

def browse_images(request):
    """Browse all available images and interact with them"""
    # If user is not authenticated, redirect to admin login
    if not request.user.is_authenticated:
        return redirect('/admin/login/?next=/browse/')
    
    # Get all images
    images = Image.objects.all().order_by('-created_at')
    
    # Get user's collections for the add to collection dropdown
    collections = Collection.objects.filter(user=request.user)
    
    # Check which images the user has already interacted with
    user_collection_images = CollectionImage.objects.filter(
        collection__user=request.user
    ).values_list('image_id', flat=True)
    
    context = {
        'images': images,
        'collections': collections,
        'user_collection_images': list(user_collection_images)
    }
    return render(request, 'recommendation/browse.html', context)

@csrf_exempt
@login_required
def star_image(request):
    """Star an image (add to 'Starred Images' collection)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        image_id = data.get('image_id')
        
        try:
            image = Image.objects.get(id=image_id)
            user = request.user
            
            # Get or create the 'Starred Images' collection
            collection, created = Collection.objects.get_or_create(
                user=user,
                name='Starred Images'
            )
            
            # Add image to collection with interaction type 3 (starred)
            collection_image, created = CollectionImage.objects.get_or_create(
                collection=collection,
                image=image,
                defaults={'interaction_type': 3}
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Image starred successfully'
            })
        except Image.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Image not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@csrf_exempt
@login_required
def like_image(request):
    """Like an image (add to 'Liked Images' collection)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        image_id = data.get('image_id')
        
        try:
            image = Image.objects.get(id=image_id)
            user = request.user
            
            # Get or create the 'Liked Images' collection
            collection, created = Collection.objects.get_or_create(
                user=user,
                name='Liked Images'
            )
            
            # Add image to collection with interaction type 1 (liked)
            collection_image, created = CollectionImage.objects.get_or_create(
                collection=collection,
                image=image,
                defaults={'interaction_type': 1}
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Image liked successfully'
            })
        except Image.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Image not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@login_required
def generate_recommendations(request):
    """Generate recommendations based on reference images"""
    # Get all reference images with their weights
    collection_images = CollectionImage.objects.filter(
        collection__user=request.user
    ).select_related('image')
    
    if not collection_images:
        # No reference images, return empty recommendations
        return render(request, 'recommendation/recommendations.html', {
            'recommendations': [],
            'session_id': None
        })
    
    # Create a new recommendation session
    session = RecommendationSession.objects.create(user=request.user)
    
    # Get all images that are not in the user's collections
    user_image_ids = CollectionImage.objects.filter(
        collection__user=request.user
    ).values_list('image_id', flat=True)
    
    # Get candidate images (not in user's collections)
    candidate_images = Image.objects.exclude(id__in=user_image_ids)
    
    # Calculate similarity scores for each candidate
    scored_images = []
    reference_labels = []
    
    # Collect all reference labels
    for ci in collection_images:
        reference_labels.extend(ci.image.get_label_list())
    
    # Remove duplicates while preserving order
    reference_labels = list(dict.fromkeys(reference_labels))
    
    for image in candidate_images:
        total_score = 0
        total_weight = 0
        
        # Compare with each reference image
        for ci in collection_images:
            similarity = calculate_cosine_similarity(
                ci.image.get_label_list(),
                image.get_label_list()
            )
            total_score += similarity * ci.interaction_type
            total_weight += ci.interaction_type
        
        if total_weight > 0:
            avg_score = total_score / total_weight
            scored_images.append((image, avg_score))
    
    # Sort by similarity score (descending)
    scored_images.sort(key=lambda x: x[1], reverse=True)
    
    # Take top 10 existing images
    top_existing_images = scored_images[:10]
    
    # Generate new images using Pollinations.AI
    pollinations_service = PollinationsAIService()
    generated_images = []
    
    # Generate 10 new images based on reference labels
    for i in range(10):
        # Create a prompt based on reference labels
        prompt = pollinations_service.generate_recommendation_prompt(reference_labels)
        
        # Generate image
        image_url = pollinations_service.generate_image(prompt)
        
        if image_url:
            # Create a temporary image object for the recommendation
            temp_image = Image(
                title=f"AI Generated Recommendation #{i+1}",
                image_url=image_url,
                labels=", ".join(reference_labels[:5])  # Use top 5 labels
            )
            generated_images.append((temp_image, 0.8))  # High similarity score for generated images
    
    # Combine existing and generated images
    all_recommendations = top_existing_images + generated_images
    
    # Sort all recommendations by similarity score
    all_recommendations.sort(key=lambda x: x[1], reverse=True)
    
    # Take top 20
    top_recommendations = all_recommendations[:20]
    
    # Save recommendations to database
    recommendations = []
    for i, (image, score) in enumerate(top_recommendations):
        # For generated images, we need to save them to the database first
        if hasattr(image, 'id') and image.id:
            # Existing image
            rec = Recommendation.objects.create(
                session=session,
                image=image,
                similarity_score=score,
                position=i+1
            )
        else:
            # Generated image - save it first
            image.save()
            rec = Recommendation.objects.create(
                session=session,
                image=image,
                similarity_score=score,
                position=i+1
            )
        recommendations.append(rec)
    
    return render(request, 'recommendation/recommendations.html', {
        'recommendations': recommendations,
        'session_id': session.id
    })

@login_required
def next_recommendation(request, session_id, current_position):
    """Get the next recommendation in the sequence"""
    try:
        recommendation = Recommendation.objects.get(
            session_id=session_id,
            position=current_position + 1
        )
        return JsonResponse({
            'success': True,
            'image_id': recommendation.image.id,
            'image_title': recommendation.image.title,
            'image_url': recommendation.image.image_url,
            'position': recommendation.position,
            'similarity_score': recommendation.similarity_score
        })
    except Recommendation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No more recommendations'
        })

@login_required
def get_similar_image(request, image_id):
    """Get a similar image for a specific reference image"""
    try:
        # Get the reference image
        reference_image = Image.objects.get(id=image_id)
        
        # Get user's collections to exclude their images
        user_image_ids = CollectionImage.objects.filter(
            collection__user=request.user
        ).values_list('image_id', flat=True)
        
        # Get candidate images (not in user's collections)
        candidate_images = Image.objects.exclude(id__in=user_image_ids).exclude(id=image_id)
        
        if not candidate_images.exists():
            return JsonResponse({
                'success': False,
                'message': 'No similar images found'
            })
        
        # Calculate similarity scores for each candidate
        scored_images = []
        reference_labels = reference_image.get_label_list()
        
        for image in candidate_images:
            similarity = calculate_cosine_similarity(
                reference_labels,
                image.get_label_list()
            )
            scored_images.append((image, similarity))
        
        # Sort by similarity score (descending) and get the most similar
        scored_images.sort(key=lambda x: x[1], reverse=True)
        
        if not scored_images:
            return JsonResponse({
                'success': False,
                'message': 'No similar images found'
            })
        
        # Get the most similar image
        most_similar_image, similarity_score = scored_images[0]
        
        return JsonResponse({
            'success': True,
            'image_id': most_similar_image.id,
            'image_title': most_similar_image.title,
            'image_url': most_similar_image.image_url,
            'similarity_score': similarity_score
        })
    except Image.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Reference image not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@csrf_exempt
@login_required
def add_to_collection(request):
    """Add a recommended image to user's collection"""
    if request.method == 'POST':
        data = json.loads(request.body)
        image_id = data.get('image_id')
        collection_id = data.get('collection_id')
        
        try:
            image = Image.objects.get(id=image_id)
            collection = Collection.objects.get(id=collection_id, user=request.user)
            
            # Add image to collection
            CollectionImage.objects.get_or_create(
                collection=collection,
                image=image,
                defaults={'interaction_type': 1}  # Default to liked
            )
            
            # Mark as added in recommendation
            Recommendation.objects.filter(
                image=image,
                session__user=request.user,
                session__is_active=True
            ).update(added_to_collection=True)
            
            return JsonResponse({
                'success': True,
                'message': 'Image added to collection successfully'
            })
        except (Image.DoesNotExist, Collection.DoesNotExist):
            return JsonResponse({
                'success': False,
                'message': 'Image or collection not found'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@csrf_exempt
@login_required
def remove_all_starred_liked(request):
    """Remove all starred and liked images by deleting the respective collections"""
    if request.method == 'POST':
        try:
            # Delete all "Starred Images" collections
            Collection.objects.filter(
                user=request.user,
                name='Starred Images'
            ).delete()
            
            # Delete all "Liked Images" collections
            Collection.objects.filter(
                user=request.user,
                name='Liked Images'
            ).delete()
            
            return JsonResponse({
                'success': True,
                'message': 'All starred and liked images removed successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@login_required
def create_collection(request):
    """Create a new collection"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            collection = Collection.objects.create(
                name=name,
                user=request.user
            )
            return JsonResponse({
                'success': True,
                'collection_id': collection.id,
                'collection_name': collection.name
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request'
    })