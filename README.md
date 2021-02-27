API for social network Yatube (https://github.com/volhadounar/hw05_final.git)
=================================

A service, API to create personal posts and comments on others' records.

Tools: Python3, Django Rest Framework, SQLite3, Authtoken, ModelViewSet, ModelSerializer, BasePermission, DefaultRouter, Cross-Origin Resource Sharing(CORS)

Getting Started
===============

1. You can build it in steps:
    1. ``cd ...wherever...``
    2. ``git clone https://github.com/volhadounar/api_yatube.git``
    3. ``cd api_yatube``
    4. ``pip install -r requirements.txt``  -- Should install everything you need
    5. ``python3 manage.py migrate`` -- Reads all the migrations folders in the application folders and creates / evolves the tables in the database
    6. ``python3 manage.py createsuperuser`` 
    7. ``python3 manage.py runserver`` -- Running localy
    8. And visit http://127.0.0.1:8000
2. Using:
    1. POST api/v1/api-token-auth/ to get token
       or use cmd ``python manage.py drf_create_token user_name``
    2. Put token value un headers using Postman
    3. Get posts or create post: http://127.0.0.1:8000/api/v1/posts/
    4. Get, update, delete post: http://127.0.0.1:8000/api/v1/posts/{post_id}/
    5. Get all post's comments, create comment for post: http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
    6. Get, update, delete particular comment: http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{comment_id}/
