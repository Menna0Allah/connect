# Connect - A Django Web Application

This document provides a complete overview of the Connect project, its structure, features, and the key backend development concepts used in its creation.


## 1. Project Overview

Connect is a web application for finding and creating study groups. Users can browse rooms based on different topics, join discussions by posting messages, and manage the rooms they create. The project is built using the Django web framework and follows modern backend development best practices.


## 2. Features

* **User Authentication:** Full user management including registration, login, and logout functionality.

* **Room & Message CRUD:** Users can Create, Read, Update, and Delete study rooms and messages.

* **Topic Browsing & Filtering:** Rooms are categorized by topics, and users can filter the room list by selecting a topic.

* **Live Search:** A search bar allows users to dynamically search for rooms by name, topic, or description.

* **User Profiles:** Each user has a profile page displaying the rooms they host and their recent activity.

* **Reusable Components:** The application uses a component-based template structure for a clean and maintainable frontend.


## 3. Project Structure (Multi-App Architecture)

A key architectural decision was to separate the project into distinct Django "apps," each with a single, clear responsibility. This is a core principle of building scalable and maintainable Django projects.

* **`connection/` (Project Folder):** This is the main project configuration directory.
    * `settings.py`: Contains all project-wide settings, including `INSTALLED_APPS`, database configuration, and template directories.
    * `urls.py`: The main URL router. It doesn't handle specific page URLs but instead directs URL prefixes to the appropriate app's `urls.py` file.

* **`activities/` (App):** This app handles the core functionality of the website—everything related to study rooms, topics, and messages.
    * `models.py`: Defines the `Room`, `Topic`, and `Message` database models.
    * `views.py`: Contains the logic for displaying and managing rooms and messages.
    * `urls.py`: Defines the URL patterns specific to the activities (e.g., `/`, `/room/5/`, `/create-room/`).
    * `templatetags/`: Contains custom template tags for creating reusable components.

* **`users/` (App):** This app is responsible for all user-related functionality.
    * `views.py`: Contains the logic for user registration, login, logout, and profile pages.
    * `urls.py`: Defines the URL patterns for user management (e.g., `/accounts/login/`, `/accounts/profile/2/`). The `accounts/` prefix is set in the main `connection/urls.py`.


## 4. Setup and Installation

To run this project on a local machine, follow these steps:

1.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    ```

2.  **Install Dependencies:**
    ```bash
    pip install Django
    ```

3.  **Apply Database Migrations:** This creates the necessary tables in the database.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Create a Superuser:** This gives you access to the admin panel.
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    The project will be available at `http://127.0.0.1:8000/`.

## 5. Key Backend Concepts Explained

This project was built with a focus on understanding the "why" behind the code. Here are the key concepts we implemented.

### a. URL Routing and Namespacing

* **Main Router (`connection/urls.py`):** Uses `include()` to delegate URL routing to the apps. This keeps the main router clean and makes the apps "pluggable."

* **App Routers (`activities/urls.py`, `users/urls.py`):** Define the specific URL patterns for each app.

* **Namespacing:** We use `app_name = 'users'` in `users/urls.py`. This is crucial for avoiding URL name collisions. In templates, we can now reliably create links using `{% url 'users:login' %}`, which tells Django to find the URL named `login` specifically inside the `users` app.


### b. Database Relationships & Lookups

* **`ForeignKey` (Many-to-One):** Used in the `Message` model to link to a `Room`. Many messages can belong to one room.

* **`ManyToManyField` (Many-to-Many):** Used in the `Room` model to link to `User` (as `participants`). One room can have many participants, and one user can participate in many rooms.

* **Reverse Lookups:**
    * For a `ForeignKey`, if `related_name` is not set, the reverse lookup from the "one" side (e.g., a `room` object) to the "many" side (`Message`) uses the default `_set` syntax: `room.message_set.all()`.
    * For a `ManyToManyField` defined on a model (e.g., `participants` on `Room`), you access it directly: `room.participants.all()`. The `related_name` is for the *reverse* lookup (from `User` back to `Room`).


### c. Django Forms & Validation

* **`GET` vs. `POST`:** Views like `createRoom` handle both request methods. `GET` displays an empty form, while `POST` processes the submitted data.

* **`form.is_valid()`:** This is the most important step in form processing. It validates user input against model constraints and custom rules, cleans the data, and protects against common security vulnerabilities.

* **`commit=False`:** Used when creating an object from a form, this allows us to modify the object in memory (e.g., to assign `room.host = request.user`) before saving it to the database.

* **Custom Validation:** The `clean()` method in `RoomForm` provides custom logic to ensure a user either selects an existing topic or enters a new one, but not both.


### d. Template Inheritance and Components

* **`{% extends 'main.html' %}`:** All pages inherit from a base template, `main.html`, which contains the main HTML structure, Bootstrap links, and the navbar. This avoids repeating the same boilerplate code on every page.

* **`{% include 'navbar.html' %}`:** Used for simple, reusable pieces of HTML. The included template has access to the same context as the parent template.

* **Custom Inclusion Tags (`templatetags`):** Used for "smart" components that need to fetch their own data. Our `{% topics_list %}` and `{% recent_activity %}` tags are perfect examples. They can be placed on any page, and they will always work because they contain their own database query logic, keeping the views clean and focused.
