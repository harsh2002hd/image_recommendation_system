# Image-Based Recommendation System

A Django-based web application that recommends images based on user preferences using metadata labels and similarity algorithms.

## Features

- User collections management (liked/starred images)
- Image recommendation engine based on reference images
- Modern UI with responsive design
- "Next" button to browse through recommendations
- Ability to add recommended images to collections
- User authentication via Django admin

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **Database**: SQLite (default Django database)

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
5. Load sample data (optional):
   ```
   python create_sample_data.py
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

1. Access the admin panel at `http://127.0.0.1:8000/admin/` to manage images and users
2. Visit the main application at `http://127.0.0.1:8000/`
3. Log in using your superuser credentials
4. Create collections and add reference images (liked/starred)
5. Generate recommendations based on your reference images
6. Browse recommendations and add them to your collections

## Models

- **Image**: Represents an image with metadata labels
- **Collection**: User-created collections to organize images
- **CollectionImage**: Through model linking images to collections with interaction type (liked/starred)
- **RecommendationSession**: Tracks recommendation sessions for users
- **Recommendation**: Individual recommendations with similarity scores

## Recommendation Algorithm

The system uses a text-based similarity algorithm comparing metadata labels:
1. Calculates Jaccard similarity between reference image labels and candidate image labels
2. Weights similarities based on interaction type (liked=1, starred=3)
3. Ranks candidates by weighted average similarity score

## Authentication

The application uses Django's built-in authentication system:
- Users must log in to access the dashboard and recommendations
- Authentication is handled through the Django admin login
- Login redirects are configured in settings.py

## Future Enhancements

- Implement image-based similarity using computer vision
- Add cosine similarity for text-based recommendations
- Integrate with cloud storage services
- Add user rating feedback loop
- Implement collaborative filtering
- Create a custom user registration and login system

## License

This project is licensed under the MIT License.