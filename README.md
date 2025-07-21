# Connect - A Django Web Application

This document provides a complete overview of the Connect project, its structure, features, and the key backend and frontend development concepts used in its creation.

## 1. Project Overview

Connect is a web application designed for creating and joining topic-based study groups. Users can browse rooms categorized by topics, participate in discussions by posting messages, manage their own rooms, like rooms and messages, and explore user profiles. The project is built using the Django web framework for the backend, styled with Bootstrap 5, Bootstrap Icons, and custom CSS for a modern, responsive frontend, and incorporates modular template components for maintainability.

## 2. Features

- **User Authentication**: Full user management with registration, login, logout, and profile pages showing hosted rooms, recent activity, and liked content.
- **Room & Message CRUD**: Authenticated users can create, read, update, and delete rooms and messages, with permission checks ensuring only owners can edit or delete their content.
- **Topic Browsing & Filtering**: Rooms are organized by topics, with a sidebar for filtering rooms by topic or viewing all rooms.
- **Live Search**: A dynamic search bar filters rooms by topic, name, or description using Django’s `Q` objects for flexible querying.
- **User Profiles**: Each user has a profile page displaying their username, hosted rooms, recent messages, and a section for liked rooms and messages, with links to related rooms.
- **Likes for Rooms and Messages**: Authenticated users can like/unlike rooms and messages, with like counts displayed and updated instantly via AJAX. 
- **Blur Effect for Non-Authenticated Users**: Non-logged-in users see a blur overlay and login/signup prompt when scrolling past 300px on the homepage, encouraging account creation.
- **Reusable Components**: Modular template components (`feed_component.html`, `topics_component.html`, `activity_component.html`) ensure a clean, reusable frontend.
- **Responsive Design**: Built with Bootstrap 5 and custom CSS, the application is fully responsive, adapting to mobile, tablet, and desktop screens.
- **Styling**: A modern, social media-inspired theme (inspired by Twitter/X) with custom colors (`#1DA1F2`, `#FFD700`, `#E0245E` for likes), hover effects, and a Lottie animation on the homepage.
- **Custom Template Tags**: Smart components (`topics_list`, `recent_activity`) fetch their own data, enhancing modularity and reducing view complexity.

## 3. Project Structure (Multi-App Architecture)

The project follows a modular, multi-app architecture to ensure scalability and maintainability, with clear separation of concerns between user management and core functionality.

- **`connect/` (Project Folder)**: Main project configuration directory.
  - `settings.py`: Configures project-wide settings, including `INSTALLED_APPS` (`users`, `activities`, `widget_tweaks`), SQLite database, static file settings (`STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT`), and custom template tags.
  - `urls.py`: Main URL router, delegating to app-specific `urls.py` files using `include()` and serving static files in development.
  - `templates/main.html`: Base template with Bootstrap 5, Bootstrap Icons, custom CSS, a responsive navbar, a Lottie animation for unauthenticated users, a blur effect, and JavaScript for likes and blur functionality. 
  - `static/styles/style.css`: Custom CSS with a social media-inspired theme, including responsive media queries, animations (e.g., bouncing arrow), and styles for likes and blur effects. 
  - `static/js/likes.js`: JavaScript for handling AJAX like/unlike actions with CSRF token support.

- **`activities/` (App)**: Handles core functionality related to study rooms, topics, messages, and likes.
  - `models.py`: Defines `Topic` (unique names), `Room` (host, topic, participants, timestamps), `Message` (user, room, body), `RoomLike` (user, room, timestamp), and `MessageLike` (user, message, timestamp) models with appropriate relationships and `unique_together` constraints for likes. 
  - `views.py`: Manages room/message CRUD, search, related room suggestions, and AJAX views for liking/unliking rooms and messages, with `login_required` decorators for protected views. 
  - `urls.py`: Defines routes for homepage, room view, room creation/update/deletion, message deletion, and like/unlike actions (`like-room/<int:pk>`, `like-message/<int:pk>`). 
  - `forms.py`: `RoomForm` for creating/editing rooms, with custom validation for selecting or creating topics.
  - `templatetags/activity_tags.py`: Custom tags (`topics_list`, `recent_activity`, `model_name`) for rendering topic lists and recent activity.
  - Templates:
    - `home.html`: Displays search bar, room count, and components for rooms, topics, and activity.
    - `room.html`: Shows room details, messages, participants, related rooms, and like buttons for rooms and messages.
    - `room_form.html`: Form for creating/editing rooms with `widget_tweaks` for styling.
    - `delete.html`: Confirmation page for deleting rooms or messages.
    - Components: `feed_component.html` (room cards with like buttons), `topics_component.html` (topic list), `activity_component.html` (recent messages). 

- **`users/` (App)**: Manages user-related functionality.
  - `models.py`: Defines `UserProfile` with a one-to-one link to `User` and a profile photo.
  - `views.py`: Handles registration, login, logout, and user profile display, including hosted rooms, messages, and liked content. 
  - `urls.py`: Defines routes under the `users/` namespace (e.g., `/users/login/`, `/users/profile/<username>/`).
  - `forms.py`: Custom forms for user registration, profile photo upload, username changes, and password updates.
  - Templates:
    - `login_register.html`: Unified form for login and registration, styled with `widget_tweaks`.
    - `profile.html`: Displays user details, hosted rooms, messages, and a section for liked rooms and messages, using `feed_component.html`.

## 4. Setup and Installation

To run the project locally:

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

2. **Install Dependencies**:
   ```bash
   pip install django django-widget-tweaks
   ```

3. **Configure Static Files**:
   - Ensure `settings.py` includes:
     ```python
     STATIC_URL = '/static/'
     STATICFILES_DIRS = [BASE_DIR / "static"]
     STATIC_ROOT = BASE_DIR / "staticfiles"
     ```
   - Create `static/styles/` and `static/js/` directories for `style.css` and `likes.js`.
   - Run:
     ```bash
     python manage.py collectstatic
     ```

4. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Access the project at `http://127.0.0.1:8000/`.

7. **Optional: Lottie Animation and Bootstrap Icons**:
   - Ensure the following are included in `main.html`:
     ```html
     <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
     <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
     ```
   - Place animation files (e.g., `welcome-animation.json`, `arrow-down.json`) in `static/lottie/`.

## 5. Key Backend and Frontend Concepts

The project emphasizes modern Django best practices and frontend design principles.

### a. URL Routing and Namespacing
- **Main Router (`connect/urls.py`)**: Uses `include()` to delegate routing to `users` and `activities` apps, with `static()` for serving static files in development.
- **App Routers**: `users/urls.py` (with `app_name = 'users'`) and `activities/urls.py` define app-specific routes, using namespacing for collision-free URLs (e.g., `{% url 'users:login' %}`).
- **Dynamic URLs**: Routes like `/room/<int:pk>/`, `/users/profile/<str:username>/`, and `/like-room/<int:pk>/` use path converters for flexibility.

### b. Database Relationships & Lookups
- **ForeignKey**: Links `Message` to `Room`, `Room` to `Topic` and `User` (host), and `RoomLike`/`MessageLike` to `User` and `Room`/`Message`. `on_delete=models.SET_NULL` or `CASCADE` ensures data integrity.
- **ManyToManyField**: `Room.participants` allows multiple users to join rooms, with `related_name='participants'` for reverse lookups.
- **Reverse Lookups**: Access messages (`room.message_set.all()`), participants (`room.participants.all()`), user-hosted rooms (`user.room_set.all()`), and likes (`room.likes.count()`, `user.roomlike_set.all()`).
- **Unique Constraints**: `unique_together` in `RoomLike` and `MessageLike` prevents duplicate likes by the same user. 

### c. Django Forms & Validation
- **GET vs. POST**: Views like `createRoom`, `loginPage`, and `like_room` handle `GET` for display and `POST` for submission (including AJAX POST for likes). 
- **form.is_valid()**: Ensures input validation and security (e.g., CSRF protection).
- **commit=False**: Used in `createRoom` and `registerPage` to modify objects (e.g., set `room.host` or lowercase `user.username`) before saving.
- **Custom Validation**: `RoomForm.clean()` enforces exclusive topic selection.

### d. Template Inheritance and Components
- **Inheritance**: All templates extend `main.html`, which includes Bootstrap 5, Bootstrap Icons, custom CSS, a responsive navbar, a Lottie animation, a blur effect, and JavaScript for likes and blur. 
- **Components**: `feed_component.html` (room cards with like buttons), `topics_component.html` (topic list), and `activity_component.html` (recent messages) are reusable via `{% include %}`. 
- **Custom Inclusion Tags**: `topics_list` and `recent_activity` fetch their own data, keeping views lightweight.
- **Widget Tweaks**: Used in forms (`login_register.html`, `room_form.html`) to apply Bootstrap classes (e.g., `form-control`, `form-select`).

### e. Styling and Frontend Design
- **Bootstrap 5 & Icons**: Provides a responsive grid, cards, forms, buttons, and heart icons for likes, ensuring cross-device compatibility. 
- **Custom CSS (`style.css`)**:
  - Uses Poppins font and a Twitter/X-inspired color scheme (`#1DA1F2` for primary, `#FFD700` for highlights, `#E0245E` for liked state).
  - Defines styles for cards (`.room-card`, `.card`), messages (`.message`), lists (`.list-group-item`), like buttons (`.like-btn`, `.liked`), blur effects (`.blur-overlay`, `.blur-prompt`), and profile likes (`.likes-section`).
  - Includes hover effects (e.g., `room-card:hover` translates upward) and a bouncing arrow animation (`.animated-arrow`).
  - Responsive design with media queries for mobile (`@media (max-width: 768px)`) and smaller screens (`@media (max-width: 576px)`).
- **Lottie Animation**: A dynamic character animation on the homepage for unauthenticated users, with a blur effect on scroll.
- **Form Styling**: `widget_tweaks` applies Bootstrap classes to form fields, with error messages styled in red (`.errorlist`).

### f. Security and Permissions
- **Authentication**: Uses Django’s built-in auth system with `UserCreationForm` and custom lowercase username handling.
- **Permission Checks**: `login_required` decorators and `PermissionDenied` exceptions ensure only authorized users can perform CRUD operations or like content. 
- **CSRF Protection**: All forms and AJAX requests include CSRF tokens for security (e.g., `getCookie('csrftoken')` in `likes.js`). 
- **Search Safety**: Uses `Q` objects for safe, flexible search queries without SQL injection risks.

### g. AJAX for Dynamic Interactions
- **Likes Feature**: Uses AJAX (`fetch` API in `likes.js`) to toggle likes on rooms and messages without page reloads, returning JSON responses with like status and counts. 
- **CSRF Handling**: JavaScript retrieves CSRF tokens from cookies for secure POST requests. 

## 6. Future Improvements
- **Pagination**: Add Django’s `Paginator` to `home` and `profile` views to handle large room/message lists.
- **Custom Error Pages**: Implement `handler403` for `PermissionDenied` exceptions with a custom 403 template.
- **Production Settings**: Move `SECRET_KEY` to environment variables, set `DEBUG = False`, and configure `ALLOWED_HOSTS`.
- **Real-Time Features**: Integrate Django Channels for live messaging or notifications.
- **Testing**: Add unit tests for views, forms, and models using Django’s `TestCase`.