# Automated Essay Scoring (AES) System

A Django-based web application that automatically scores essays using machine learning algorithms. The system compares student essays against reference answers using TF-IDF vectorization and cosine similarity to provide instant scoring and feedback.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-6.0.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

- **Automated Essay Scoring**: Uses TF-IDF vectorization and cosine similarity algorithms
- **Teacher Dashboard**: Create and manage essay questions with reference answers
- **Student Portal**: Submit essays and receive instant scores
- **Score Range Customization**: Set custom min/max score ranges for each question
- **Real-time Feedback**: Immediate scoring upon essay submission
- **Responsive Design**: Bootstrap-powered UI for all devices
- **Admin Panel**: Django admin interface for advanced management

## 📋 System Architecture

### Core Components

1. **Scoring Engine** (`scoring/logic.py`)
   - TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
   - Cosine similarity calculation
   - Score mapping to custom ranges

2. **Data Models** (`scoring/models.py`)
   - `Question`: Essay prompts with reference answers
   - `Essay`: Student submissions with calculated scores

3. **Web Interface** 
   - Teacher dashboard for question management
   - Student portal for essay submission
   - Result display with scoring feedback

## 🛠️ Technology Stack

- **Backend**: Django 6.0.1
- **Machine Learning**: scikit-learn
- **Database**: SQLite (default), PostgreSQL/MySQL supported
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.0
- **Python Libraries**: NumPy, scikit-learn

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/daisukifh/automated-essay-scoring.git
   cd automated-essay-scoring
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv aes_env
   source aes_env/bin/activate  # On Windows: aes_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 🚀 Usage Guide

### For Teachers

1. **Create Questions**
   - Navigate to "Teacher Dashboard"
   - Fill in question title, prompt, and reference answer
   - Set minimum and maximum score ranges
   - Save the question

2. **Manage Questions**
   - View all created questions on the homepage
   - Access Django admin panel for advanced management

### For Students

1. **Select Question**
   - Choose from available questions on the homepage
   - Click "Start Writing" to begin

2. **Submit Essay**
   - Enter your name
   - Write your essay in the provided text area
   - Submit for automatic scoring

3. **View Results**
   - Receive instant score based on similarity to reference answer
   - Score is calculated using advanced NLP algorithms

## 🧠 How the Scoring Works

The AES system uses the following algorithm:

1. **Text Preprocessing**: Both the reference answer and student essay are processed
2. **TF-IDF Vectorization**: Converts text into numerical vectors representing word importance
3. **Cosine Similarity**: Measures the similarity between reference and student vectors
4. **Score Mapping**: Maps similarity (0-1) to the custom score range (min_score to max_score)

```python
def calculate_score(essay_text, reference_text, min_score=0, max_score=100):
    # Create TF-IDF vectors
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([reference_text, essay_text])
    
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Map to score range
    score_range = max_score - min_score
    final_score = min_score + (cosine_sim * score_range)
    
    return round(final_score, 2)
```

## 📊 Testing

Run the verification script to test the complete workflow:

```bash
python verify_aes.py
```

This script will:
- Create a test question
- Test the scoring algorithm with sample essays
- Display scoring results for verification

## 🗂️ Project Structure

```
automated-essay-scoring/
├── aes_project/          # Django project settings
│   ├── __init__.py
│   ├── settings.py       # Project configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── scoring/              # Main application
│   ├── migrations/      # Database migrations
│   ├── templates/       # HTML templates
│   ├── __init__.py
│   ├── admin.py         # Admin configuration
│   ├── apps.py          # App configuration
│   ├── forms.py         # Django forms
│   ├── logic.py         # Scoring algorithm
│   ├── models.py        # Data models
│   ├── urls.py          # App URL routing
│   └── views.py         # View controllers
├── db.sqlite3           # SQLite database
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── verify_aes.py        # Testing script
└── README.md           # This file
```

## ⚙️ Configuration

### Database Configuration
The system uses SQLite by default. To use PostgreSQL or MySQL, update `DATABASES` in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aes_database',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Security Settings
For production deployment:
- Set `DEBUG = False` in settings.py
- Configure `ALLOWED_HOSTS`
- Use environment variables for sensitive data
- Change the `SECRET_KEY`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📋 Future Enhancements

- [ ] Advanced NLP models (BERT, GPT)
- [ ] Detailed feedback generation
- [ ] Plagiarism detection
- [ ] Essay length and structure analysis
- [ ] Multi-language support
- [ ] Statistical reporting dashboard
- [ ] Export functionality (PDF reports)
- [ ] Batch processing for multiple essays

## ⚠️ Limitations

- Basic similarity-based scoring (considers content similarity, not grammar or style)
- Requires representative reference answers
- Performance depends on text quality and length
- No advanced linguistic analysis

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Daisuki FH**
- GitHub: [@daisukifh](https://github.com/daisukifh)

## 🙏 Acknowledgments

- Django framework for rapid web development
- scikit-learn for machine learning capabilities
- Bootstrap for responsive UI components

---

*Built with ❤️ for educational purposes*