# automated-essay-scoring

# 📝 AES - Automated Essay Scoring System

## 🌟 **Overview**

**AES (Automated Essay Scoring)** dengan brand name **"Eduvate"** adalah platform penilaian esai otomatis yang menggunakan teknologi Machine Learning dan Natural Language Processing untuk memberikan evaluasi esai secara real-time. Sistem ini dirancang untuk membantu pendidik dan siswa dalam proses pembelajaran yang lebih efektif dan objektif.

**Live Demo**: [https://eduvate-web-327602290437.asia-southeast2.run.app](https://eduvate-web-327602290437.asia-southeast2.run.app)

## 🎯 **Problem Statement**

### Masalah yang Diatasi:
- **Keterbatasan Waktu**: Dosen/guru membutuhkan waktu lama untuk menilai esai secara manual
- **Subjektivitas Penilaian**: Perbedaan standar penilaian antar penilai
- **Delayed Feedback**: Siswa tidak mendapat feedback cepat untuk perbaikan
- **Workload Overflow**: Beban kerja berlebihan dalam mengevaluasi banyak esai
- **Inkonsistensi**: Sulit mempertahankan konsistensi penilaian dalam skala besar
- **Lack of Detailed Analysis**: Kurangnya analisis mendalam terhadap aspek-aspek specific esai

## 🛠️ **Technology Stack**

### **Backend AI/ML Engine**
- **Framework**: Python Flask
- **ML Model**: BERT (Bidirectional Encoder Representations from Transformers)
- **Tokenizer**: IndoBERT untuk pemrosesan bahasa Indonesia
- **ML Framework**: TensorFlow 2.x dengan Keras
- **Model Storage**: TensorFlow SavedModel format

### **Frontend Web Application**
- **Framework**: Next.js 15 with TypeScript
- **UI Library**: Radix UI components
- **Styling**: Tailwind CSS + CSS Modules
- **Authentication**: NextAuth.js
- **State Management**: React Hooks + Context API
- **HTTP Client**: Fetch API
- **Animations**: Framer Motion

### **Database & Storage**
- **Primary Database**: MongoDB
- **ODM**: Mongoose
- **Schema Design**: Document-based with relationships

### **DevOps & Deployment**
- **Containerization**: Docker
- **Cloud Platform**: Google Cloud Run
- **CI/CD**: Docker + Google Cloud Build
- **Monitoring**: Built-in cloud monitoring

## 📊 **Scoring Methodology**

### **Scoring Components**
Sistem mengevaluasi esai berdasarkan 4 aspek dengan bobot yang dapat disesuaikan:

1. **Relevancy Score (25% default)**
   - Mengukur kesesuaian jawaban dengan pertanyaan
   - Menggunakan semantic similarity analysis

2. **Correlation Score (45% default)**
   - Menilai koherensi dan alur logika dalam esai
   - Menganalisis hubungan antar paragraf dan kalimat

3. **Length Score (15% default)**
   - Evaluasi panjang esai optimal (100-200 kata recommended)
   - Formula: Exponential scoring function

4. **Vocabulary Score (15% default)**
   - Mengukur keragaman kosakata menggunakan Type-Token Ratio (TTR)
   - Adjusted TTR untuk esai pendek

### **Scoring Algorithm**
```python
def calculate_total_score(relevancy, correlation, length, vocabulary, multipliers):
    total_score = (
        relevancy * multipliers.relevancy +
        correlation * multipliers.correlation + 
        length * multipliers.length +
        vocabulary * multipliers.vocabulary
    )
    return total_score
```

## 🏗️ **System Architecture**

### **High-Level Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   AI/ML Model   │
│   (Next.js)     │◄──►│   (Flask)       │◄──►│   (BERT)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Session  │    │   Business      │    │   TensorFlow    │
│   Management    │    │   Logic & API   │    │   SavedModel    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────────┐
│            MongoDB Database                 │
│   ┌─────────┐ ┌─────────┐ ┌─────────────┐  │
│   │ Users   │ │ Courses │ │ Submissions │  │
│   │ Quizzes │ │ Results │ │   ...       │  │
│   └─────────┘ └─────────┘ └─────────────┘  │
└─────────────────────────────────────────────┘
```

### **Request Flow Diagram**
```
User Input (Essay) 
    │
    ▼
Frontend Validation
    │
    ▼
API Request to Flask Backend
    │
    ▼
Text Preprocessing & Cleaning
    │
    ▼
BERT Tokenization (IndoBERT)
    │
    ▼
Model Inference (TensorFlow)
    │
    ▼
Score Calculation & Aggregation
    │
    ▼
Feedback Generation
    │
    ▼
Database Storage (MongoDB)
    │
    ▼
Response to Frontend
    │
    ▼
Results Display to User
```

## 🔄 **Data Flow & Business Logic**

### **1. Authentication Flow**
```typescript
// User Authentication Process
1. User accesses /auth?q=login
2. NextAuth.js handles authentication
3. Session created with user role (student/lecturer/admin)  
4. Role-based routing to appropriate dashboard
5. Protected routes validate session and role
```

### **2. Quiz Management Flow (Lecturer/Admin)**
```typescript
// Quiz Creation Process
POST /api/quizzes
{
  title: "Quiz Title",
  description: "Optional description",
  questions: ["Question 1", "Question 2"],
  courseId: ObjectId,
  multipliers: {
    relevancy: 0.25,
    correlation: 0.45,
    length: 0.15,
    vocabulary: 0.15
  }
}
```

### **3. Quiz Taking Flow (Student)**
```typescript
// Student Quiz Process
1. GET /api/quizzes/[id] - Load quiz data
2. Auto-save answers to localStorage (draft mode)
3. Real-time word counting and validation
4. Timer tracking for completion time
5. Final submission triggers AI scoring process
```

### **4. AI Scoring Pipeline**
```python
def generate_feedback(prompt, essay, multipliers):
    # Step 1: Text Preprocessing
    cleaned_essay = clean_essay(essay)
    combined_text = f"{prompt} [SEP] {cleaned_essay}"
    
    # Step 2: Tokenization
    inputs = tokenizer(
        combined_text,
        truncation=True,
        padding='max_length', 
        max_length=512,
        return_tensors='tf'
    )
    
    # Step 3: Model Inference
    predict_fn = model.signatures['serving_default']
    predictions = predict_fn(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask']
    )
    
    # Step 4: Score Extraction
    relevancy_score = predictions['dense_2'][0][0].numpy() * 100
    correlation_score = predictions['dense_2'][0][1].numpy() * 100
    
    # Step 5: Additional Metrics
    length_score = calculate_length_score(essay)
    vocabulary_score = calculate_vocabulary_score(essay)
    
    # Step 6: Weighted Aggregation
    total_score = (
        relevancy_score * multipliers['relevancy'] +
        correlation_score * multipliers['correlation'] +
        length_score * multipliers['length'] +
        vocabulary_score * multipliers['vocabulary']
    )
    
    return {
        "relevancy_score": relevancy_score,
        "correlation_score": correlation_score,
        "length_score": length_score, 
        "vocabulary_score": vocabulary_score,
        "total_score": total_score,
        "feedback": generate_contextual_feedback(scores)
    }
```

## 📁 **Project Structure**

```
AES/
├── api/                          # Python Flask Backend
│   ├── app.py                   # Main Flask application
│   ├── saved_model/             # TensorFlow SavedModel
│   ├── dockerfile               # Docker configuration
│   └── myenv/                   # Python virtual environment
│
├── interface/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/                 # App Router (Next.js 13+)
│   │   │   ├── api/            # API Routes
│   │   │   ├── auth/           # Authentication pages
│   │   │   ├── dashboard/      # Dashboard pages
│   │   │   └── quiz/           # Quiz-related pages
│   │   ├── components/         # Reusable UI components
│   │   ├── models/             # MongoDB Models (Mongoose)
│   │   ├── types/              # TypeScript type definitions
│   │   └── lib/                # Utility functions
│   ├── package.json
│   ├── next.config.ts
│   └── tailwind.config.ts
│
└── README.md                    # This documentation
```

## 📊 **Database Schema**

### **User Collection**
```typescript
interface IUser {
    _id: ObjectId;
    email: string;                // Unique email address
    password: string;             // Hashed password (bcrypt)
    name: string;                 // Full name
    role: 'student' | 'lecturer' | 'admin';  // User role
    createdAt: Date;
    updatedAt: Date;
}
```

### **Course Collection**
```typescript
interface ICourse {
    _id: ObjectId;
    title: string;                // Course title
    description?: string;         // Optional course description
    quizzez: ObjectId[];         // References to Quiz documents
    createdAt: Date;
    updatedAt: Date;
}
```

### **Quiz Collection**
```typescript
interface IQuiz {
    _id: ObjectId;
    title: string;                // Quiz title
    description?: string;         // Optional quiz description
    course: ObjectId;             // Reference to Course document
    questions: string[];          // Array of essay questions
    multipliers: {                // Scoring weights (customizable)
        relevancy: number;        // Default: 0.25
        correlation: number;      // Default: 0.45  
        length: number;           // Default: 0.15
        vocabulary: number;       // Default: 0.15
    };
    createdAt: Date;
    updatedAt: Date;
}
```

### **Submission Collection**
```typescript
interface ISubmission {
    _id: ObjectId;
    student: ObjectId;            // Reference to User document
    quiz: ObjectId;               // Reference to Quiz document
    answers: IAnswer[];           // Array of essay answers with scores
    totalScore: number;           // Aggregated total score
    duration: number;             // Time taken in seconds
    isCompleted: boolean;         // Completion status
    submittedAt: Date;            // Submission timestamp
    createdAt: Date;
    updatedAt: Date;
}

interface IAnswer {
    question: string;             // The essay question
    answer: string;               // Student's essay answer
    feedback: string;             // AI-generated feedback text
    scores: {                     // Detailed scoring breakdown
        relevancy: number;        // Relevancy score (0-100)
        correlation: number;      // Correlation score (0-100)
        length: number;           // Length score (0-100)
        vocabulary: number;       // Vocabulary score (0-100)
    };
    overallScore: number;         // Weighted total score
}
```

## 🔗 **API Documentation**

### **Authentication Endpoints**

#### `POST /api/auth/register`
Register a new user account.

**Request Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com", 
    "password": "securepassword",
    "role": "student"
}
```

**Response:**
```json
{
    "success": true,
    "message": "User registered successfully",
    "data": {
        "_id": "user_id",
        "name": "John Doe",
        "email": "john@example.com",
        "role": "student"
    }
}
```

### **Quiz Management Endpoints**

#### `GET /api/quizzes`
Get all available quizzes.

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "_id": "quiz_id",
            "title": "Essay Quiz 1",
            "description": "Quiz description",
            "questions": ["Question 1", "Question 2"],
            "course": {
                "_id": "course_id", 
                "title": "Course Name"
            },
            "multipliers": {
                "relevancy": 0.25,
                "correlation": 0.45,
                "length": 0.15,
                "vocabulary": 0.15
            }
        }
    ]
}
```

#### `POST /api/quizzes`
Create a new quiz (Lecturer/Admin only).

**Request Body:**
```json
{
    "title": "New Quiz",
    "description": "Optional description",
    "questions": ["Essay question 1", "Essay question 2"],
    "courseId": "course_object_id",
    "multipliers": {
        "relevancy": 0.3,
        "correlation": 0.4,
        "length": 0.2,
        "vocabulary": 0.1
    }
}
```

#### `GET /api/quizzes/[id]`
Get specific quiz details.

### **AI Scoring Endpoints**

#### `POST /generate_feedback` (Flask Backend)
Generate AI-powered essay scores and feedback.

**Request Body:**
```json
{
    "relevancy_multiplier": 0.25,
    "correlation_multiplier": 0.45,
    "length_multiplier": 0.15,
    "vocabulary_multiplier": 0.15,
    "answers": [
        {
            "prompt": "Discuss the importance of environmental conservation.",
            "essay": "Environmental conservation is crucial for sustainable development..."
        }
    ]
}
```

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "relevancy_score": 85,
            "correlation_score": 78,
            "length_score": 92,
            "vocabulary_score": 88,
            "total_score": 82,
            "feedback": "Kualitas esai sangat baik dengan sedikit aspek yang perlu disempurnakan."
        }
    ]
}
```

#### `POST /api/quizResult`
Save quiz submission and results.

**Request Body:**
```json
{
    "userId": "user_object_id",
    "quizId": "quiz_object_id",
    "courseId": "course_object_id",
    "courseName": "Course Title",
    "userName": "Student Name",
    "totalScore": 82.5,
    "totalQuestions": 3,
    "duration": 1800,
    "answers": [
        {
            "question": "Essay question text",
            "answer": "Student essay answer",
            "feedback": "AI feedback text",
            "overallScore": 85,
            "scores": {
                "relevancy": 88,
                "correlation": 82,
                "length": 90,
                "vocabulary": 85
            }
        }
    ]
}
```

## 🚀 **Installation & Deployment**

### **Prerequisites**
- **Node.js** 18+ and npm/yarn
- **Python** 3.9+ with pip
- **MongoDB** database (local or Atlas)
- **Git** for version control

### **Local Development Setup**

#### **1. Clone Repository**
```bash
git clone <repository-url>
cd AES/program
```

#### **2. Backend Setup (Flask API)**
```bash
cd api/

# Create and activate virtual environment
python -m venv myenv
# Windows
myenv\Scripts\activate
# macOS/Linux  
source myenv/bin/activate

# Install dependencies
pip install flask flask-cors numpy tensorflow transformers

# Start Flask server
python app.py
# Server runs on http://localhost:5288
```

#### **3. Frontend Setup (Next.js)**
```bash
cd interface/

# Install dependencies
npm install
# or
yarn install

# Set environment variables
cp .env.example .env.local
# Edit .env.local with your MongoDB URI and NextAuth secrets

# Start development server
npm run dev
# or
yarn dev
# Server runs on http://localhost:3000
```

#### **4. Environment Configuration**

Create `.env.local` in the interface directory:
```bash
# Database
MONGODB_URI=mongodb://localhost:27017/aes_database
# or MongoDB Atlas URI
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/aes_database

# NextAuth
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000

# API URLs
MODEL_BASEURL=http://localhost:5288
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### **Production Deployment**

#### **Docker Deployment**

**Backend Dockerfile:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5288
CMD ["python", "app.py"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

#### **Google Cloud Run Deployment**
```bash
# Build and deploy backend
gcloud builds submit --tag gcr.io/PROJECT_ID/aes-backend ./api
gcloud run deploy aes-backend --image gcr.io/PROJECT_ID/aes-backend --platform managed

# Build and deploy frontend  
gcloud builds submit --tag gcr.io/PROJECT_ID/aes-frontend ./interface
gcloud run deploy aes-frontend --image gcr.io/PROJECT_ID/aes-frontend --platform managed
```

## 🧪 **Testing**

### **Backend Testing**
```bash
cd api/
python -m pytest tests/
```

### **Frontend Testing**
```bash
cd interface/
npm run test
# or
yarn test
```

### **API Testing Examples**
```bash
# Test AI scoring endpoint
curl -X POST http://localhost:5288/generate_feedback \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {
        "prompt": "Test question",
        "essay": "Test essay answer with sufficient length to demonstrate scoring capabilities."
      }
    ]
  }'
```

## 🔧 **Configuration Options**

### **Scoring Multipliers**
Customize the weight of each scoring component:

```json
{
    "multipliers": {
        "relevancy": 0.25,      // Relevance to question (0-1)
        "correlation": 0.45,    // Content coherence (0-1) 
        "length": 0.15,         // Essay length score (0-1)
        "vocabulary": 0.15      // Vocabulary diversity (0-1)
    }
}
```

### **Length Scoring Formula**
```python
def calculate_length_score(essay):
    word_count = len(essay.split())
    if word_count >= 200:
        return 100
    elif word_count >= 100:
        return round(50 + 40 * (1 - exp(-0.02 * (word_count - 100))))
    else:
        return round(25 + 25 * (1 - exp(-0.04 * word_count)))
```

### **Vocabulary Scoring Formula**
```python
def calculate_vocabulary_score(essay):
    words = essay.split()
    unique_words = set(words)
    ttr = len(unique_words) / len(words) if len(words) > 0 else 0
    adjusted_ttr = ttr * (len(words) / 50) if len(words) < 50 else ttr
    return round(adjusted_ttr * 100)
```

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Backend Issues:**
- **Model Loading Error**: Ensure TensorFlow SavedModel is in correct directory
- **Memory Error**: Increase container memory allocation for model inference
- **CORS Issues**: Verify Flask-CORS configuration for frontend domain

#### **Frontend Issues:**
- **Authentication Error**: Check NextAuth configuration and session handling
- **API Connection Error**: Verify backend URL in environment variables
- **Build Errors**: Clear `.next` cache and `node_modules`, reinstall dependencies

#### **Database Issues:**
- **Connection Error**: Verify MongoDB URI and network connectivity
- **Schema Validation Error**: Check Mongoose model definitions match data structure

### **Debug Commands**
```bash
# Check backend logs
docker logs <backend-container-id>

# Check frontend logs  
npm run build 2>&1 | tee build.log

# Test database connection
mongosh "mongodb://localhost:27017/aes_database"
```

## 📈 **Performance Considerations**

### **AI Model Optimization**
- **Model Quantization**: Consider using TensorFlow Lite for reduced model size
- **Batch Processing**: Process multiple essays in single inference call
- **Caching**: Implement Redis caching for frequently accessed results

### **Database Optimization**
- **Indexing**: Create indexes on frequently queried fields
- **Connection Pooling**: Configure MongoDB connection pooling
- **Data Pagination**: Implement pagination for large result sets

### **Frontend Optimization**  
- **Code Splitting**: Utilize Next.js automatic code splitting
- **Image Optimization**: Use Next.js Image component
- **Caching**: Implement SWR or React Query for data fetching

## 🔒 **Security Considerations**

### **Authentication & Authorization**
- **JWT Security**: Secure token generation and validation
- **Role-Based Access**: Implement granular permission system
- **Session Management**: Secure session storage and invalidation

### **Data Protection**
- **Input Validation**: Sanitize all user inputs
- **SQL Injection Prevention**: Use parameterized queries
- **XSS Protection**: Implement Content Security Policy

### **API Security**
- **Rate Limiting**: Implement API rate limiting
- **CORS Configuration**: Restrict allowed origins
- **HTTPS**: Enforce HTTPS in production

## 📝 **Contributing Guidelines**

### **Development Workflow**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### **Code Style**
- **TypeScript**: Follow strict TypeScript configuration
- **Python**: Follow PEP 8 style guidelines  
- **Formatting**: Use Prettier for frontend, Black for Python

### **Commit Convention**
```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting changes
refactor: code refactoring
test: adding tests
chore: maintenance tasks
```

## 📊 **Monitoring & Analytics**

### **Application Metrics**
- **Response Time**: API endpoint performance monitoring
- **Error Rate**: Track application errors and exceptions
- **User Engagement**: Quiz completion rates and user activity

### **AI Model Metrics**
- **Inference Time**: Model prediction latency
- **Score Distribution**: Analysis of scoring patterns
- **Feedback Quality**: User satisfaction with AI feedback

## 🗺️ **Roadmap & Future Enhancements**

### **Short Term (Next 3 months)**
- [ ] **Multi-language Support**: Extend beyond Indonesian language
- [ ] **Advanced Analytics Dashboard**: Comprehensive reporting for educators
- [ ] **Mobile App**: React Native mobile application
- [ ] **Plagiarism Detection**: Integrate plagiarism checking capabilities

### **Medium Term (3-6 months)**  
- [ ] **Real-time Collaboration**: Multi-user essay editing
- [ ] **Advanced AI Models**: Integration with GPT-based models
- [ ] **Accessibility Features**: Screen reader and keyboard navigation support
- [ ] **Integration APIs**: LMS integration (Moodle, Canvas, etc.)

### **Long Term (6+ months)**
- [ ] **Adaptive Learning**: Personalized learning recommendations
- [ ] **Voice-to-Text**: Audio essay submissions
- [ ] **Blockchain Certificates**: Verifiable achievement certificates
- [ ] **AI Writing Assistant**: Real-time writing suggestions

## 📞 **Support & Contact**

### **Technical Support**
- **Documentation**: Refer to this README and inline code comments
- **Issues**: Create GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for general questions

### **Development Team**
- **Project Lead**: [Your Name]
- **Backend Developer**: [Backend Dev Name]  
- **Frontend Developer**: [Frontend Dev Name]
- **ML Engineer**: [ML Engineer Name]

### **Resources**
- **Live Demo**: [https://eduvate-web-327602290437.asia-southeast2.run.app](https://eduvate-web-327602290437.asia-southeast2.run.app)
- **API Documentation**: `/api/docs` (when available)
- **User Guide**: See `/docs/user-guide.md` (if created)

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 **Acknowledgments**

- **BERT Model**: Hugging Face Transformers library
- **IndoBERT**: Indonesian BERT model for Indonesian language processing
- **UI Components**: Radix UI component library
- **Icons**: Lucide React and Radix Icons
- **Styling**: Tailwind CSS framework

---

**Built with ❤️ for improving education through AI technology**

*Last updated: January 30, 2026*
