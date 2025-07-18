# Connect - A Django Web Application

This document provides a complete overview of the Connect project, its structure, features, and the key backend and frontend development concepts used in its creation.


## 1. Project Overview

Connect is a web application designed for creating and joining topic-based study groups. Users can browse rooms categorized by topics, participate in discussions by posting messages, manage their own rooms, and explore user profiles. The project is built using the Django web framework for the backend, styled with Bootstrap and custom CSS for a modern, responsive frontend, and incorporates modular template components for maintainability.


## 2. Features

- **User Authentication**: Full user management with registration, login, logout, and profile pages showing hosted rooms and recent activity.

- **Room & Message CRUD**: Authenticated users can create, read, update, and delete rooms and messages, with permission checks ensuring only owners can edit or delete their content.

- **Topic Browsing & Filtering**: Rooms are organized by topics, with a sidebar for filtering rooms by topic or viewing all rooms.

- **Live Search**: A dynamic search bar filters rooms by topic, name, or description using Django’s `Q` objects for flexible querying.

- **User Profiles**: Each user has a profile page displaying their username, hosted rooms, and recent activity, with links to related rooms.

- **Reusable Components**: Modular template components (`feed_component.html`, `topics_component.html`, `activity_component.html`) ensure a clean, reusable frontend.

- **Responsive Design**: Built with Bootstrap 5 and custom CSS, the application is fully responsive, adapting to mobile, tablet, and desktop screens.

- **Styling**: A modern, social media-inspired theme (inspired by Twitter) with custom colors (`#1DA1F2`, `#FFD700`), hover effects, and a Lottie animation on the homepage.

- **Custom Template Tags**: Smart components (`topics_list`, `recent_activity`) fetch their own data, enhancing modularity and reducing view complexity.


## 3. Project Structure (Multi-App Architecture)

The project follows a modular, multi-app architecture to ensure scalability and maintainability, with clear separation of concerns between user management and core functionality.

- **`connection/` (Project Folder)**: Main project configuration directory.
  - `settings.py`: Configures project-wide settings, including `INSTALLED_APPS` (`users`, `activities`, `widget_tweaks`), SQLite database, and custom template tags.
  - `urls.py`: Main URL router, delegating to app-specific `urls.py` files using `include()`.
  - `templates/main.html`: Base template with Bootstrap 5, custom CSS, a responsive navbar, and a Lottie animation for unauthenticated users on the homepage.
  - `static/style.css`: Custom CSS with a social media-inspired theme, including responsive media queries and animations (e.g., bouncing arrow).

- **`activities/` (App)**: Handles core functionality related to study rooms, topics, and messages.
  - `models.py`: Defines `Topic` (unique names), `Room` (host, topic, participants, timestamps), and `Message` (user, room, body) models with appropriate relationships.
  - `views.py`: Manages room/message CRUD, search, and related room suggestions, with `login_required` decorators for protected views.
  - `urls.py`: Defines routes for homepage, room view, room creation/update/deletion, and message deletion.
  - `forms.py`: `RoomForm` for creating/editing rooms, with custom validation for selecting or creating topics.
  - `templatetags/activity_tags.py`: Custom tags (`topics_list`, `recent_activity`, `model_name`) for rendering topic lists and recent activity.
  - Templates:
    - `home.html`: Displays search bar, room count, and components for rooms, topics, and activity.
    - `room.html`: Shows room details, messages, participants, and related rooms.
    - `room_form.html`: Form for creating/editing rooms with `widget_tweaks` for styling.
    - `delete.html`: Confirmation page for deleting rooms or messages.
    - Components: `feed_component.html` (room cards), `topics_component.html` (topic list), `activity_component.html` (recent messages).

- **`users/` (App)**: Manages user-related functionality.
  - `views.py`: Handles registration, login, logout, and user profile display.
  - `urls.py`: Defines routes under the `accounts/` prefix (e.g., `/accounts/login/`, `/accounts/profile/<username>/`).
  - Templates:
    - `login_register.html`: Unified form for login and registration, styled with `widget_tweaks`.
    - `profile.html`: Displays user details and hosted rooms, using `feed_component.html`.


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

3. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Access the project at `http://127.0.0.1:8000/`.

6. **Optional: Lottie Animation**:
   - Ensure the Lottie player library is included:
     ```html
     <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
     ```
   - Place the animation file (e.g., `character.json`) in `static/animations/` and reference it in `main.html`.


## 5. Key Backend and Frontend Concepts

The project emphasizes modern Django best practices and frontend design principles.

### a. URL Routing and Namespacing
- **Main Router (`connection/urls.py`)**: Uses `include()` to delegate routing to `users` and `activities` apps, keeping the main router clean and apps pluggable.
- **App Routers**: `users/urls.py` (with `app_name = 'users'`) and `activities/urls.py` define app-specific routes, using namespacing for collision-free URLs (e.g., `{% url 'users:login' %}`).
- **Dynamic URLs**: Routes like `/room/<int:pk>/` and `/profile/<str:username>/` use path converters for flexibility.

### b. Database Relationships & Lookups
- **ForeignKey**: Links `Message` to `Room` (many messages per room) and `Room` to `Topic` and `User` (host). `on_delete=models.SET_NULL` ensures data integrity.
- **ManyToManyField**: `Room.participants` allows multiple users to join rooms, with `related_name='participants'` for reverse lookups.
- **Reverse Lookups**: Access messages via `room.message_set.all()` and participants via `room.participants.all()`. User-hosted rooms are accessed via `user.room_set.all()`.

### c. Django Forms & Validation
- **GET vs. POST**: Views like `createRoom` and `loginPage` handle `GET` for form display and `POST` for submission.
- **form.is_valid()**: Ensures input validation and security (e.g., CSRF protection).
- **commit=False**: Used in `createRoom` and `registerPage` to modify objects (e.g., set `room.host` or lowercase `user.username`) before saving.
- **Custom Validation**: `RoomForm.clean()` enforces exclusive topic selection (existing or new topic).

### d. Template Inheritance and Components
- **Inheritance**: All templates extend `main.html`, which includes Bootstrap 5, custom CSS, a responsive navbar, and a Lottie animation for unauthenticated users.
- **Components**: `feed_component.html`, `topics_component.html`, and `activity_component.html` are reusable, included via `{% include %}` for modularity.
- **Custom Inclusion Tags**: `topics_list` and `recent_activity` fetch their own data (e.g., `Topic.objects.all()`, `Message.objects.all()[:5]`), keeping views lightweight.
- **Widget Tweaks**: Used in forms (`login_register.html`, `room_form.html`) to apply Bootstrap classes (e.g., `form-control`, `form-select`).

### e. Styling and Frontend Design
- **Bootstrap 5**: Provides a responsive grid, cards, forms, and buttons, ensuring cross-device compatibility.
- **Custom CSS (`style.css`)**:
  - Uses Poppins font and a Twitter-inspired color scheme (`#1DA1F2` for primary, `#FFD700` for highlights).
  - Defines styles for cards (`.room-card`, `.card`), messages (`.message`), and lists (`.list-group-item`).
  - Includes hover effects (e.g., `room-card:hover` translates upward) and a bouncing arrow animation (`.animated-arrow`).
  - Responsive design with media queries for mobile (`@media (max-width: 768px)`) and smaller screens (`@media (max-width: 576px)`), adjusting font sizes, padding, and layout.
- **Lottie Animation**: A dynamic character animation on the homepage for unauthenticated users, enhancing visual appeal.
- **Form Styling**: `widget_tweaks` applies Bootstrap classes to form fields, with error messages styled in red (`.errorlist`).

### f. Security and Permissions
- **Authentication**: Uses Django’s built-in auth system with `UserCreationForm` and custom lowercase username handling.
- **Permission Checks**: `login_required` decorators and `PermissionDenied` exceptions ensure only authorized users can perform CRUD operations.
- **CSRF Protection**: All forms include `{% csrf_token %}` for security.
- **Search Safety**: Uses `Q` objects for safe, flexible search queries without SQL injection risks.

## 6. Future Improvements
- **Pagination**: Add Django’s `Paginator` to `home` and `profile` views to handle large room/message lists.
- **Custom Error Pages**: Implement `handler403` for `PermissionDenied` exceptions with a custom 403 template.
- **Production Settings**: Move `SECRET_KEY` to environment variables, set `DEBUG = False`, and configure `ALLOWED_HOSTS`.
- **Real-Time Features**: Integrate Django Channels for live messaging or notifications.
- **Testing**: Add unit tests for views, forms, and models using Django’s `TestCase`.