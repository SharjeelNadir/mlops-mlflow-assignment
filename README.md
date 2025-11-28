
# MLOps MLflow Assignment

## 1. Project Overview

This project demonstrates a comprehensive **MLOps pipeline** using industry-standard tools and practices. The assignment showcases the complete machine learning lifecycle, from data versioning to model training, evaluation, and continuous integration.

**Project Name:** mlops-mlflow-assignment  
**Dataset:** Boston Housing Dataset  
**Objective:** Build an end-to-end ML pipeline with version control, experiment tracking, and CI/CD automation.

---

## 2. Repository Structure

```
mlops-mlflow-assignment/
├── data/
│   ├── raw/
│   │   └── boston_housing.csv
│   └── processed/
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessor.py
│   ├── trainer.py
│   └── evaluator.py
├── components/
│   ├── __init__.py
│   └── (modular pipeline components)
├── artifacts/
│   ├── models/
│   ├── metrics/
│   └── logs/
├── pipeline.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── .dvc/
├── .gitignore
├── dvc.yaml
└── README.md
```

---

## 3. Setup Instructions

### 3.1 Clone the Repository

```bash
git clone https://github.com/yourusername/mlops-mlflow-assignment.git
cd mlops-mlflow-assignment
```

### 3.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Data Versioning with DVC

### 4.1 Initialize DVC

```bash
dvc init
git add .dvc/.gitignore .dvc/config
git commit -m "Initialize DVC"
```

### 4.2 Add Dataset to DVC

```bash
dvc add data/raw/boston_housing.csv
git add data/raw/boston_housing.csv.dvc .gitignore
git commit -m "Add Boston Housing dataset to DVC"
```

### 4.3 Configure Remote Storage (Optional)

```bash
dvc remote add -d myremote s3://your-bucket-name/mlops-assignment
dvc push
```

### 4.4 Pull Data

```bash
dvc pull
```

---

## 5. Pipeline Walkthrough with MLflow

The ML pipeline is orchestrated using **MLflow** and consists of four stages:

1. **Data Loading:** Load raw Boston Housing dataset
2. **Preprocessing:** Clean, normalize, and prepare features
3. **Model Training:** Train regression model (Linear Regression/XGBoost)
4. **Evaluation:** Compute metrics (RMSE, MAE, R²)

### 5.1 Run the Pipeline

```bash
python pipeline.py
```

### 5.2 Start MLflow UI

```bash
mlflow ui --host 0.0.0.0 --port 5000
```

Visit `http://localhost:5000` in your browser to view:
- Experiment tracking
- Run parameters and metrics
- Model artifacts
- Comparison between runs

### 5.3 Pipeline Code Structure

The `pipeline.py` file orchestrates the workflow:

```python
import mlflow
from src.data_loader import load_data
from src.preprocessor import preprocess_data
from src.trainer import train_model
from src.evaluator import evaluate_model

mlflow.set_experiment("boston_housing_experiment")

with mlflow.start_run():
    data = load_data("data/raw/boston_housing.csv")
    X_train, X_test, y_train, y_test = preprocess_data(data)
    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    mlflow.log_metrics(metrics)
    mlflow.sklearn.log_model(model, "model")
```

---

## 6. Continuous Integration with Jenkins

### 6.1 Jenkinsfile Overview

The `Jenkinsfile` defines the CI/CD pipeline with multiple stages:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        
        stage('Data Preparation') {
            steps {
                sh 'dvc pull'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t mlops-assignment:latest .'
            }
        }
        
        stage('Run Pipeline') {
            steps {
                sh '. venv/bin/activate && python pipeline.py'
            }
        }
        
        stage('Model Evaluation') {
            steps {
                sh '. venv/bin/activate && python -m pytest tests/'
            }
        }
        
        stage('Artifacts') {
            steps {
                archiveArtifacts artifacts: 'artifacts/**', allowEmptyArchive: true
            }
        }
    }
}
```

### 6.2 Pipeline Stages

| Stage | Purpose |
|-------|---------|
| **Checkout** | Fetch code from GitHub repository |
| **Setup** | Create virtual environment and install dependencies |
| **Data Preparation** | Pull versioned dataset using DVC |
| **Build Docker Image** | Create containerized application |
| **Run Pipeline** | Execute ML pipeline with MLflow tracking |
| **Model Evaluation** | Run tests and validate model performance |
| **Artifacts** | Archive outputs for downstream use |

---

## 7. How to Run Jenkins Pipeline

### 7.1 Prerequisites

- Jenkins server installed and running
- GitHub repository connected to Jenkins
- Docker installed on Jenkins agent
- Python 3.8+ available

### 7.2 Create Jenkins Job

1. Open Jenkins dashboard: `http://localhost:8080`
2. Click **New Item** → Enter job name → Select **Pipeline**
3. Configure:
   - **Definition:** Pipeline script from SCM
   - **SCM:** Git
   - **Repository URL:** `https://github.com/yourusername/mlops-mlflow-assignment.git`
   - **Script Path:** `Jenkinsfile`
4. Click **Save** and **Build Now**

### 7.3 Monitor Pipeline

- View **Console Output** for logs
- Check **Build Artifacts** for artifacts/
- View **Stage View** for pipeline visualization

---

## 8. Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Programming language |
| **MLflow** | Experiment tracking and model registry |
| **DVC** | Data versioning and pipeline management |
| **Jenkins** | Continuous integration and deployment |
| **Docker** | Containerization |
| **GitHub** | Version control and repository hosting |
| **scikit-learn** | Machine learning library |
| **pandas** | Data manipulation |
| **numpy** | Numerical computing |

---

## 9. Screenshots List (for PDF Submission)

- ✅ DVC initialization and data versioning
- ✅ MLflow UI showing experiment runs and metrics
- ✅ Model performance comparison across runs
- ✅ Jenkins pipeline build stages and success
- ✅ Docker image build output
- ✅ Artifacts archived in Jenkins
- ✅ GitHub repository commits and history
- ✅ Final model metrics and predictions

---

## 10. Final Remarks

This assignment demonstrates:
- **Data Management:** Reproducible versioning with DVC
- **Experiment Tracking:** Comprehensive MLflow logging
- **Automation:** CI/CD pipeline with Jenkins
- **Containerization:** Docker deployment readiness
- **Best Practices:** Modular code structure and documentation

For questions or improvements, refer to the project wiki or submit an issue on GitHub.

---

