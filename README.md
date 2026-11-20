<div align="center">

# 🧠 ML API Service

### Production-ready machine learning API with model versioning, A/B testing, and monitoring

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [API Docs](#-api-documentation) • [Monitoring](#-monitoring)

</div>

---

## ✨ Features

- 🚀 **High-Performance API** - Sub-100ms inference latency
- 📦 **Model Versioning** - Manage multiple model versions
- 🔄 **A/B Testing** - Test different models in production
- 📊 **Real-Time Monitoring** - Track model performance and drift
- 🔄 **Auto-Retraining** - Automated model updates
- 🎯 **Multi-Model Support** - Serve multiple ML models
- 📈 **Scalable** - Horizontal scaling with Kubernetes
- 🔒 **Secure** - API key authentication and rate limiting
- 📝 **Comprehensive Logging** - Detailed request/response logging
- 🧪 **Easy Testing** - Built-in testing framework

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
   ┌────▼────┐                   ┌────▼────┐
   │ API Pod │                   │ API Pod │
   │   1     │                   │   2     │
   └────┬────┘                   └────┬────┘
        │                             │
        └──────────────┬──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │      Model Registry         │
        │  (MLflow / Custom)          │
        └──────────────┬──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │    Monitoring & Logging     │
        │  (Prometheus + Grafana)     │
        └─────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Core
- **Framework:** FastAPI
- **ML Library:** TensorFlow / PyTorch / scikit-learn
- **Model Registry:** MLflow
- **Database:** PostgreSQL
- **Cache:** Redis
- **Queue:** Celery

### DevOps
- **Containerization:** Docker
- **Orchestration:** Kubernetes
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana
- **Logging:** ELK Stack

### Testing
- **Unit Tests:** pytest
- **Load Testing:** Locust
- **Integration Tests:** pytest-asyncio

---

## 🚀 Installation

### Using Docker

```bash
# Clone repository
git clone https://github.com/bag864471-ux/ml-api-service.git
cd ml-api-service

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start services
docker-compose up -d

# Access API documentation
open http://localhost:8000/docs
```

### Kubernetes Deployment

```bash
# Build and push Docker image
docker build -t your-registry/ml-api-service:latest .
docker push your-registry/ml-api-service:latest

# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment
kubectl get pods
```

---

## 📚 API Documentation

### Health Check

```bash
GET /health
```

### Model Inference

```bash
POST /api/v1/predict
Content-Type: application/json
X-API-Key: your-api-key

{
  "model_name": "image_classifier",
  "version": "v1.0.0",
  "data": {
    "image": "base64_encoded_image"
  }
}
```

Response:

```json
{
  "prediction": "cat",
  "confidence": 0.95,
  "model_version": "v1.0.0",
  "inference_time_ms": 45,
  "request_id": "req_123abc"
}
```

### Batch Prediction

```bash
POST /api/v1/predict/batch
{
  "model_name": "sentiment_analyzer",
  "data": [
    {"text": "I love this product!"},
    {"text": "Not worth the money."}
  ]
}
```

### Model Management

```bash
# List models
GET /api/v1/models

# Get model info
GET /api/v1/models/{model_name}

# Upload new model
POST /api/v1/models/upload
Content-Type: multipart/form-data

# Set active version
PUT /api/v1/models/{model_name}/activate
{
  "version": "v1.1.0"
}
```

---

## 📁 Project Structure

```
ml-api-service/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration
│   ├── api/
│   │   └── v1/
│   │       ├── predict.py         # Prediction endpoints
│   │       ├── models.py          # Model management
│   │       └── monitoring.py      # Monitoring endpoints
│   ├── core/
│   │   ├── model_manager.py       # Model loading & versioning
│   │   ├── predictor.py           # Inference logic
│   │   └── preprocessor.py        # Data preprocessing
│   ├── models/                    # ML model implementations
│   │   ├── base_model.py
│   │   ├── image_classifier.py
│   │   └── text_classifier.py
│   ├── services/
│   │   ├── mlflow_service.py      # MLflow integration
│   │   ├── monitoring_service.py  # Metrics collection
│   │   └── cache_service.py       # Redis caching
│   └── utils/
│       ├── helpers.py
│       └── validators.py
├── models/                        # Saved model files
├── notebooks/                     # Jupyter notebooks
├── tests/
│   ├── test_api.py
│   ├── test_models.py
│   └── test_integration.py
├── k8s/                          # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── hpa.yaml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔧 Configuration

`.env` file:

```env
# Application
DEBUG=False
API_V1_PREFIX=/api/v1
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/mlapi
REDIS_URL=redis://localhost:6379/0

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000

# Model Storage
MODEL_STORAGE_PATH=./models
DEFAULT_MODEL_VERSION=v1.0.0

# Monitoring
ENABLE_METRICS=True
PROMETHEUS_PORT=9090

# Security
API_KEY_HEADER=X-API-Key
RATE_LIMIT_PER_MINUTE=100
```

---

## 📊 Monitoring

### Metrics Tracked

- **Request Metrics:** Count, latency, error rate
- **Model Metrics:** Accuracy, drift, prediction distribution
- **System Metrics:** CPU, memory, disk usage
- **Business Metrics:** Predictions by category, confidence scores

### Grafana Dashboard

Access Grafana at `http://localhost:3000`

### Alerts

- High error rate (>5%)
- Model drift detected
- High latency (>500ms)
- Low disk space

---

## 🧪 Testing

```bash
# Unit tests
pytest tests/ -v

# Integration tests
pytest tests/test_integration.py

# Load testing
locust -f tests/load_test.py

# Test coverage
pytest --cov=app --cov-report=html
```

---

## 🔄 CI/CD Pipeline

GitHub Actions workflow:

1. **Lint & Format:** Check code quality
2. **Test:** Run unit and integration tests
3. **Build:** Build Docker image
4. **Push:** Push to container registry
5. **Deploy:** Deploy to Kubernetes
6. **Monitor:** Run smoke tests

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 📝 License

MIT License - see [LICENSE](./LICENSE)

---

<div align="center">

**Built with ❤️ by [bag864471-ux](https://github.com/bag864471-ux)**

⭐ Star this repo if you find it helpful!

</div>
