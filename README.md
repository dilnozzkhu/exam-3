Exam - Django Backend Application
Overview
Exam is a Django backend application providing comprehensive management of blog content, comments, and essential site policies. The application is designed with best practices and DRY (Don't Repeat Yourself) principles to ensure clean, maintainable code, and all data is dynamically managed through the database.

Features
Blog List: Display all blog posts with pagination for optimized load times.
Blog Detail: View detailed content of each blog post along with associated comments.
Blog Comment: Add, edit, and delete comments for blog posts, supporting multiple levels of replies.
Contact: Handle contact form submissions and send queries to the database.
Terms and Conditions: Display the terms and conditions page, dynamically managed from the database.
Privacy Policy: Display the privacy policy page, managed via the database.
Setup and Installation
Clone the Repository:

bash

git clone <repository-link>
cd exam
Install Requirements:

bash

pip install -r requirements.txt
Database Setup: Run migrations to set up the database schema.

bash

python manage.py migrate
Run the Server:

bash

python manage.py runserver
Project Structure
models.py: Contains models for Blog, Comment, Contact, TermsAndConditions, and PrivacyPolicy.
views.py: Modularized views for handling blog listings, blog details, comments, and policy pages.
urls.py: URL patterns for accessing various endpoints.
serializers.py: Serializers to convert model instances to JSON format.
admin.py: Customizable admin panel to manage content directly from the Django admin interface.