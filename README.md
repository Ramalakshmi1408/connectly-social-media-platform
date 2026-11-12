# Connectly — Social Media Platform

Connectly is a Django-based social media web application where users can create accounts, share posts, interact with other users, and build connections.

## Features

- User registration, login and logout
- User profiles with profile pictures, bios and locations
- Create posts with captions and images
- Edit and delete your own posts
- Like and unlike posts
- Comment on posts
- Follow and unfollow users
- Search for users and posts
- Responsive interface for desktop and mobile screens

## Technology Stack

- **Frontend:** HTML, CSS
- **Backend:** Python, Django
- **Database:** SQLite
- **Image Handling:** Pillow

## Project Structure

```text
social_media_platform/
├── config/
├── social/
│   ├── migrations/
│   ├── templates/
│   │   └── social/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd social_media_platform
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the following address in your browser:

http://127.0.0.1:8000/

## Future Improvements

- Notifications and messaging
- User discovery and advanced search
- Post sharing and bookmarking
- Improved interface and additional customization

## Project Status

Core social media functionality implemented and locally tested.

## License

This project is created for educational purposes.