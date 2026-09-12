# 🌿 LeafScan AI — Plant Disease Detection App

A full-stack plant disease detection application using **MobileNetV2 Transfer Learning**, 
**Flask**, and a beautiful web UI. Upload a leaf photo and get instant disease diagnosis, 
confidence scores, and treatment advice.

---

## 📁 Project Structure

```
plant_disease_app/
│
├── app.py                    # Flask web app & API endpoints
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── model/
│   ├── train_model.py        # Model training script (MobileNetV2)
│   ├── plant_disease_model.h5 # Trained model (generated after training)
│   └── class_labels.json     # Class index → name mapping
│
├── utils/
│   └── predictor.py          # Image preprocessing + prediction + disease DB
│
├── templates/
│   └── index.html            # Beautiful single-page web UI
│
├── static/
│   ├── uploads/              # Temporary uploaded images
│   └── css/ js/              # (Optional) extra assets
│
└── data/
    └── PlantVillage/         # Dataset folder (you download this)
        ├── Apple___Apple_scab/
        ├── Tomato___Early_blight/
        └── ... (38 folders)
```

---

## ⚡ Quick Start (5 minutes)

### Step 1 — Clone / Download the project
```bash
cd plant_disease_app
```

### Step 2 — Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app (Demo Mode)
```bash
python app.py
```
Open **http://localhost:5000** in your browser. 
The app runs in **Demo Mode** (simulated predictions) until you train a model.

---

## 🧠 Training Your Own Model

### Step 1 — Download the PlantVillage Dataset
- Go to: https://www.kaggle.com/datasets/emmarex/plantdisease
- Download and extract to: `data/PlantVillage/`
- Structure should be: `data/PlantVillage/Apple___Apple_scab/image001.jpg` etc.

### Step 2 — Train the model
```bash
python model/train_model.py
```

This will:
1. ✅ Load and augment the PlantVillage dataset
2. ✅ Build MobileNetV2 transfer learning model
3. ✅ Phase 1: Train new top layers (base frozen)
4. ✅ Phase 2: Fine-tune top 30 layers
5. ✅ Save best model to `model/plant_disease_model.h5`
6. ✅ Save class labels to `model/class_labels.json`
7. ✅ Plot training accuracy/loss curves

Training time: ~30–60 min on GPU, ~2–4 hours on CPU

### Step 3 — Restart the Flask app
```bash
python app.py
```
The badge in the header will change to **"Model Ready · 38 Classes"**

---

## 🔌 API Reference

### `POST /api/predict`
Upload a leaf image and get disease prediction.

**File upload:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -F "image=@leaf.jpg"
```

**Base64:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "data:image/jpeg;base64,/9j/4AAQ..."}'
```

**Response:**
```json
{
  "success": true,
  "result": {
    "display_name": "Tomato Early Blight",
    "confidence": 0.9234,
    "confidence_pct": "92.3%",
    "is_healthy": false,
    "disease_info": {
      "type": "Fungal",
      "severity": "Moderate",
      "description": "...",
      "symptoms": ["..."],
      "treatment": ["..."],
      "prevention": "...",
      "farmer_tip": "..."
    },
    "top3": [...]
  }
}
```

### `GET /api/diseases`
List all 38+ supported disease classes.

### `GET /api/health`
Check server and model status.

---

## 🌱 Supported Plants & Diseases

| Plant   | Diseases Supported |
|---------|--------------------|
| 🍎 Apple | Apple Scab, Black Rot, Cedar Apple Rust, Healthy |
| 🍅 Tomato | Early Blight, Late Blight, Bacterial Spot, Septoria, Spider Mites, Target Spot, Leaf Miner, Yellow Leaf Curl Virus, Mosaic Virus, Healthy |
| 🥔 Potato | Early Blight, Late Blight, Healthy |
| 🌽 Corn | Common Rust, Northern Leaf Blight, Healthy |
| 🍇 Grape | Black Rot, Healthy |
| + more  | 38 classes total from PlantVillage |

---

## 🚀 Deploying to Production

### Using Gunicorn (Linux/Mac)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
```

---

## 🎯 Model Architecture

```
Input (224×224×3)
    ↓
MobileNetV2 (pretrained ImageNet, ~2.2M params)
    ↓
GlobalAveragePooling2D
    ↓
Dense(256, ReLU)
    ↓
Dropout(0.5)
    ↓
Dense(38, Softmax)  ← Number of disease classes
```

**Transfer Learning Strategy:**
- Phase 1: Freeze MobileNetV2, train only top layers (10 epochs)
- Phase 2: Unfreeze last 30 layers of MobileNetV2, fine-tune with low LR (20 epochs)

---

## 📊 Expected Performance

| Metric              | Value      |
|---------------------|------------|
| PlantVillage Dataset | ~54,000 images |
| Classes             | 38          |
| Validation Accuracy | ~96%        |
| Inference Time      | < 100ms     |
| Model Size          | ~14 MB      |

---

## 💡 Tips for Better Results

1. **Image quality**: Use clear, well-lit photos
2. **Leaf focus**: Zoom in on the affected leaf area
3. **Single leaf**: One leaf per photo works best
4. **Natural light**: Avoid flash or harsh shadows
5. **Both surfaces**: Try photographing leaf underside if top looks healthy

---

## 📝 License

For educational and agricultural research use. 
PlantVillage dataset: CC BY 4.0 License.
# Plant-Disease-Detection
