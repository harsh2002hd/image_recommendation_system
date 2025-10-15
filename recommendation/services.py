import requests
from typing import List, Optional
from django.conf import settings

class PollinationsAIService:
    """
    Service class for interacting with Pollinations.AI API
    """
    
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt"
        self.timeout = 30  # seconds
    
    def generate_image(self, prompt: str, width: int = 512, height: int = 512, 
                      model: str = "flux") -> Optional[str]:
        """
        Generate an image using Pollinations.AI API
        
        Args:
            prompt (str): Text prompt for image generation
            width (int): Width of the generated image
            height (int): Height of the generated image
            model (str): Model to use for generation
            
        Returns:
            str: URL of the generated image, or None if failed
        """
        try:
            # Construct the URL with parameters
            url = f"{self.base_url}/{prompt}?width={width}&height={height}&model={model}"
            
            # Make the request
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                # Return the image URL
                return response.url
            else:
                print(f"Failed to generate image. Status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return None
    
    def generate_recommendation_prompt(self, labels: List[str]) -> str:
        """
        Generate a prompt for image generation based on labels
        
        Args:
            labels (List[str]): Labels from reference images
            
        Returns:
            str: Generated prompt for image generation
        """
        # Combine labels into a descriptive prompt
        label_description = ", ".join(labels[:10])  # Limit to 10 labels
        
        # Base prompt structure
        prompt = f"high quality image featuring {label_description}"
        
        # Add style modifiers
        prompt += ", professional photography, detailed, vibrant colors, high resolution"
        
        return prompt

def calculate_cosine_similarity(labels1: List[str], labels2: List[str]) -> float:
    """
    Calculate cosine similarity between two sets of labels
    
    Args:
        labels1 (List[str]): First set of labels
        labels2 (List[str]): Second set of labels
        
    Returns:
        float: Cosine similarity score between 0 and 1
    """
    # Convert to sets for easier computation
    set1 = set(labels1)
    set2 = set(labels2)
    
    # If either set is empty, return 0
    if not set1 or not set2:
        return 0.0
    
    # Calculate intersection and union
    intersection = len(set1.intersection(set2))
    magnitude1 = len(set1) ** 0.5
    magnitude2 = len(set2) ** 0.5
    
    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # Calculate cosine similarity
    similarity = intersection / (magnitude1 * magnitude2)
    return similarity