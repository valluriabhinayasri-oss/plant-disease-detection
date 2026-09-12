# """
# =============================================================
#   Plant Disease Detection - Prediction & Disease Database
# =============================================================
#   This module handles:
#   - Loading the trained model
#   - Preprocessing uploaded images
#   - Predicting disease and confidence
#   - Returning treatment advice
# """

# import os
# import numpy as np
# import json
# from PIL import Image
# import io

# # ─── Constants ────────────────────────────────────────────────────────────────
# IMG_SIZE = 224
# MODEL_PATH = "model/plant_disease_model.h5"
# LABELS_PATH = "model/class_labels.json"

# # ─── Disease Information Database ─────────────────────────────────────────────
# # Each entry: treatment tips, severity, and farmer advice
# DISEASE_INFO = {
#     # ── Apple Diseases ─────────────────────────────────────────────────────────
#     "Apple___Apple_scab": {
#         "display_name": "Apple Scab",
#         "type": "Fungal",
#         "severity": "Moderate",
#         "description": "A fungal disease causing dark, scabby lesions on leaves and fruit.",
#         "symptoms": ["Dark olive-green spots on leaves", "Scabby corky lesions on fruit", "Premature leaf drop"],
#         "treatment": [
#             "Apply fungicides (captan, mancozeb) at bud break",
#             "Remove and destroy infected leaves",
#             "Improve air circulation by pruning",
#             "Use resistant apple varieties"
#         ],
#         "prevention": "Apply preventive sprays before rain events in spring.",
#         "farmer_tip": "🌱 Scout trees weekly in spring. Early detection saves up to 80% of crop.",
#         "emoji": "🍎"
#     },
#     "Apple___Black_rot": {
#         "display_name": "Apple Black Rot",
#         "type": "Fungal",
#         "severity": "High",
#         "description": "Causes fruit rot, leaf spots, and cankers on branches.",
#         "symptoms": ["Brown circular leaf spots with purple borders", "Rotting fruit with black mummified remains", "Sunken cankers on bark"],
#         "treatment": [
#             "Remove mummified fruit and dead wood",
#             "Apply copper-based fungicides",
#             "Prune out infected branches 15cm below visible cankers",
#             "Avoid overhead irrigation"
#         ],
#         "prevention": "Clean up all fallen fruit and leaves at end of season.",
#         "farmer_tip": "🧹 Sanitation is key — remove all mummified fruits before winter.",
#         "emoji": "🍎"
#     },
#     "Apple___Cedar_apple_rust": {
#         "display_name": "Cedar Apple Rust",
#         "type": "Fungal",
#         "severity": "Moderate",
#         "description": "Requires both cedar and apple trees to complete its lifecycle.",
#         "symptoms": ["Bright orange-yellow spots on upper leaf surface", "Tube-like structures on leaf undersides", "Premature defoliation"],
#         "treatment": [
#             "Apply myclobutanil or propiconazole fungicides",
#             "Remove nearby cedar/juniper trees if possible",
#             "Plant rust-resistant apple varieties"
#         ],
#         "prevention": "Apply fungicides from pink bud stage through summer.",
#         "farmer_tip": "🌲 Check nearby cedar trees for orange galls in late winter — cut them off before they release spores.",
#         "emoji": "🍎"
#     },
#     "Apple___healthy": {
#         "display_name": "Healthy Apple",
#         "type": "Healthy",
#         "severity": "None",
#         "description": "Your apple plant appears healthy! No disease detected.",
#         "symptoms": [],
#         "treatment": ["Continue regular care and monitoring"],
#         "prevention": "Maintain good airflow, proper fertilization, and regular inspection.",
#         "farmer_tip": "✅ Keep up the great work! Regular monitoring prevents disease outbreaks.",
#         "emoji": "✅"
#     },

#     # ── Tomato Diseases ────────────────────────────────────────────────────────
#     "Tomato___Bacterial_spot": {
#         "display_name": "Tomato Bacterial Spot",
#         "type": "Bacterial",
#         "severity": "High",
#         "description": "Bacterial infection causing spots on leaves, stems, and fruit.",
#         "symptoms": ["Small water-soaked spots on leaves", "Dark raised scabs on fruit", "Yellowing around lesions"],
#         "treatment": [
#             "Apply copper-based bactericides (copper hydroxide)",
#             "Remove heavily infected plants",
#             "Avoid overhead watering",
#             "Use disease-free certified seeds"
#         ],
#         "prevention": "Use drip irrigation and stake plants to reduce moisture on foliage.",
#         "farmer_tip": "💧 Switch to drip irrigation — it reduces bacterial spread by up to 60%.",
#         "emoji": "🍅"
#     },
#     "Tomato___Early_blight": {
#         "display_name": "Tomato Early Blight",
#         "type": "Fungal",
#         "severity": "Moderate",
#         "description": "Common fungal disease causing concentric ring patterns on leaves.",
#         "symptoms": ["Dark brown spots with concentric rings (target pattern)", "Yellow halo around spots", "Lower leaves affected first"],
#         "treatment": [
#             "Apply chlorothalonil or mancozeb fungicide",
#             "Remove infected lower leaves",
#             "Mulch around plants to prevent soil splash",
#             "Ensure adequate plant spacing"
#         ],
#         "prevention": "Rotate crops — avoid planting tomatoes in same spot for 3 years.",
#         "farmer_tip": "🔄 Crop rotation is your best long-term defense against early blight.",
#         "emoji": "🍅"
#     },
#     "Tomato___Late_blight": {
#         "display_name": "Tomato Late Blight",
#         "type": "Fungal/Oomycete",
#         "severity": "Critical",
#         "description": "The same pathogen (Phytophthora) that caused the Irish Potato Famine. Very destructive.",
#         "symptoms": ["Large dark water-soaked lesions on leaves", "White fuzzy growth on leaf undersides", "Rapid plant death in humid conditions"],
#         "treatment": [
#             "Apply fungicides immediately (metalaxyl, chlorothalonil)",
#             "Remove and bag all infected plant material",
#             "Avoid composting infected material",
#             "Consider destroying severely affected plants"
#         ],
#         "prevention": "Plant resistant varieties. Monitor weather — disease thrives in cool, wet conditions.",
#         "farmer_tip": "⚠️ Act fast — late blight can destroy an entire crop within a week in wet weather!",
#         "emoji": "🍅"
#     },
#     "Tomato___Leaf_Miner": {
#         "display_name": "Tomato Leaf Miner",
#         "type": "Pest",
#         "severity": "Moderate",
#         "description": "Insect larvae tunnel through leaf tissue causing serpentine trails.",
#         "symptoms": ["Winding white/yellowish trails on leaves", "Tiny flies on plants", "Blistered or distorted leaves"],
#         "treatment": [
#             "Apply spinosad or abamectin insecticides",
#             "Use yellow sticky traps to monitor adult flies",
#             "Release Diglyphus isaea (biological control)",
#             "Remove heavily infested leaves"
#         ],
#         "prevention": "Use row covers early in season. Inspect transplants before planting.",
#         "farmer_tip": "🪤 Yellow sticky traps are cheap and effective for early detection.",
#         "emoji": "🍅"
#     },
#     "Tomato___Septoria_leaf_spot": {
#         "display_name": "Septoria Leaf Spot",
#         "type": "Fungal",
#         "severity": "Moderate",
#         "description": "Fungal disease causing numerous small spots with dark borders.",
#         "symptoms": ["Small circular spots with gray centers and dark borders", "Tiny black dots (fruiting bodies) in centers", "Lower leaves affected first, spreading upward"],
#         "treatment": [
#             "Apply fungicides (chlorothalonil, copper-based)",
#             "Remove and discard infected leaves",
#             "Avoid wetting foliage when watering",
#             "Stake plants to improve air circulation"
#         ],
#         "prevention": "Space plants at least 60cm apart for good airflow.",
#         "farmer_tip": "✂️ Removing the bottom 30cm of leaves when plants are young reduces infection dramatically.",
#         "emoji": "🍅"
#     },
#     "Tomato___Spider_mites Two-spotted_spider_mite": {
#     "display_name": "Tomato Spider Mites (Two-Spotted)",
#     "type": "Pest",
#     "severity": "Moderate",
#     "description": (
#         "Two-spotted spider mites (Tetranychus urticae) are tiny arachnids "
#         "that pierce leaf cells and suck out the contents, causing yellowing, "
#         "stippling, and eventually leaf death. They thrive in hot, dry conditions "
#         "and reproduce extremely fast — a full generation in just 5–7 days. "
#         "Severe infestations can defoliate an entire plant within weeks."
#     ),
#     "symptoms": [
#         "Tiny yellow or white speckles (stippling) on upper leaf surface",
#         "Leaves turn bronze, yellow, or silvery",
#         "Fine silky webbing on undersides of leaves and between stems",
#         "Tiny moving dots (mites) visible on leaf undersides with magnification",
#         "Premature leaf drop in severe infestations",
#         "Stunted plant growth and reduced fruit yield"
#     ],
#     "treatment": [
#         "Spray strong jets of water on leaf undersides to dislodge mites",
#         "Apply neem oil spray (2 tbsp per liter water) every 3–5 days",
#         "Use insecticidal soap solution on affected leaves",
#         "Apply miticides: abamectin, bifenazate, or spiromesifen",
#         "Release predatory mites (Phytoseiulus persimilis) for biological control",
#         "Remove and destroy heavily infested leaves immediately",
#         "Avoid broad-spectrum insecticides that kill natural predators"
#     ],
#     "prevention": (
#         "Keep plants well-watered — drought-stressed plants attract mites. "
#         "Maintain humidity around plants. Avoid dusty conditions. "
#         "Inspect leaf undersides weekly. Introduce predatory mites early in season. "
#         "Use reflective mulch to confuse and repel mites."
#     ),
#     "farmer_tip": (
#         "💦 A strong water spray on leaf undersides daily can control mild "
#         "infestations without any chemicals. Start early — once webbing appears, "
#         "populations are already in the thousands!"
#     ),
#     "emoji": "🍅"
# },

# # Alternate key format (same data, different class name format)
# "Tomato___Spider_mites_Two-spotted_spider_mite": {
#     "display_name": "Tomato Spider Mites (Two-Spotted)",
#     "type": "Pest",
#     "severity": "Moderate",
#     "description": (
#         "Two-spotted spider mites (Tetranychus urticae) are tiny arachnids "
#         "that pierce leaf cells and suck out the contents, causing yellowing, "
#         "stippling, and eventually leaf death. They thrive in hot, dry conditions "
#         "and reproduce extremely fast — a full generation in just 5–7 days."
#     ),
#     "symptoms": [
#         "Tiny yellow or white speckles (stippling) on upper leaf surface",
#         "Leaves turn bronze, yellow, or silvery",
#         "Fine silky webbing on undersides of leaves",
#         "Tiny moving dots visible under magnification",
#         "Premature leaf drop in severe cases"
#     ],
#     "treatment": [
#         "Spray strong jets of water on leaf undersides",
#         "Apply neem oil every 3–5 days",
#         "Use insecticidal soap on affected leaves",
#         "Apply miticides: abamectin or bifenazate",
#         "Release predatory mites (Phytoseiulus persimilis)"
#     ],
#     "prevention": "Keep plants well-watered. Inspect weekly. Maintain humidity.",
#     "farmer_tip": "💦 Daily water spray on leaf undersides controls mild infestations without chemicals!",
#     "emoji": "🍅"
# },
#     "Tomato___Target_Spot": {
#         "display_name": "Tomato Target Spot",
#         "type": "Fungal",
#         "severity": "Moderate",
#         "description": "Fungal disease causing distinctive target-like rings on leaves and fruit.",
#         "symptoms": ["Brown spots with concentric rings on leaves", "Small dark spots on fruit", "Defoliation in severe cases"],
#         "treatment": [
#             "Apply azoxystrobin or chlorothalonil",
#             "Remove infected leaves immediately",
#             "Avoid overhead irrigation"
#         ],
#         "prevention": "Ensure good air circulation and avoid dense planting.",
#         "farmer_tip": "🌿 Thin out dense canopy to improve airflow and reduce humidity inside the plant.",
#         "emoji": "🍅"
#     },
#     "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
#         "display_name": "Tomato Yellow Leaf Curl Virus",
#         "type": "Viral",
#         "severity": "Critical",
#         "description": "Viral disease spread by whiteflies causing severe yield loss.",
#         "symptoms": ["Upward leaf curling and yellowing", "Stunted plant growth", "Flowers drop before fruiting"],
#         "treatment": [
#             "No cure — remove and destroy infected plants immediately",
#             "Control whitefly population with insecticides (imidacloprid)",
#             "Use yellow sticky traps for monitoring"
#         ],
#         "prevention": "Plant TYLCV-resistant varieties. Use reflective mulches to repel whiteflies.",
#         "farmer_tip": "🚫 Remove infected plants immediately — there is no cure, and keeping them spreads the virus to healthy plants.",
#         "emoji": "🍅"
#     },
#     "Tomato___Tomato_mosaic_virus": {
#         "display_name": "Tomato Mosaic Virus",
#         "type": "Viral",
#         "severity": "High",
#         "description": "Highly contagious virus spread by contact and contaminated tools.",
#         "symptoms": ["Mosaic pattern of light/dark green on leaves", "Distorted, fern-like leaf shape", "Reduced fruit size and quality"],
#         "treatment": [
#             "No chemical cure available",
#             "Remove and destroy all infected plants",
#             "Disinfect tools with 10% bleach solution"
#         ],
#         "prevention": "Wash hands thoroughly before handling plants. Disinfect all tools between plants.",
#         "farmer_tip": "🧤 Always wash hands and disinfect tools — this virus spreads through touch!",
#         "emoji": "🍅"
#     },
#     "Tomato___healthy": {
#         "display_name": "Healthy Tomato",
#         "type": "Healthy",
#         "severity": "None",
#         "description": "Your tomato plant appears healthy! No disease detected.",
#         "symptoms": [],
#         "treatment": ["Continue regular care and monitoring"],
#         "prevention": "Maintain consistent watering, fertilization, and weekly inspections.",
#         "farmer_tip": "✅ Healthy plants! Maintain mulching and stake tall plants for best yields.",
#         "emoji": "✅"
#     },

#     # ── Potato Diseases ────────────────────────────────────────────────────────
#     "Potato___Early_blight": {
#         "display_name": "Potato Early Blight",
#         "type": "Fungal",
#         "severity": "Moderate",
#         "description": "Fungal disease causing characteristic target-board spots on potato leaves.",
#         "symptoms": ["Dark brown target-pattern spots", "Yellow halo around lesions", "Lower/older leaves affected first"],
#         "treatment": [
#             "Apply chlorothalonil or mancozeb fungicide",
#             "Hill soil around plants to protect tubers",
#             "Remove infected foliage",
#             "Ensure adequate potassium fertilization"
#         ],
#         "prevention": "Use certified disease-free seed potatoes. Rotate crops every 3 years.",
#         "farmer_tip": "🥔 Strong, well-nourished plants resist early blight better — don't skip fertilization.",
#         "emoji": "🥔"
#     },
#     "Potato___Late_blight": {
#         "display_name": "Potato Late Blight",
#         "type": "Fungal/Oomycete",
#         "severity": "Critical",
#         "description": "Phytophthora infestans — the most devastating potato disease in history.",
#         "symptoms": ["Water-soaked dark lesions on leaves", "White mold on undersides", "Rapid browning and plant collapse"],
#         "treatment": [
#             "Apply metalaxyl + mancozeb fungicide immediately",
#             "Destroy all infected plant tissue",
#             "Hill up soil to protect tubers",
#             "Harvest early if outbreak is severe"
#         ],
#         "prevention": "Plant certified seed. Monitor forecasts — spray before predicted wet weather.",
#         "farmer_tip": "⚠️ Late blight can destroy an entire field in 2 weeks. Act at first sign!",
#         "emoji": "🥔"
#     },
#     "Potato___healthy": {
#         "display_name": "Healthy Potato",
#         "type": "Healthy",
#         "severity": "None",
#         "description": "Your potato plant appears healthy! No disease detected.",
#         "symptoms": [],
#         "treatment": ["Continue regular care and monitoring"],
#         "prevention": "Hill plants, maintain consistent moisture, and monitor weekly.",
#         "farmer_tip": "✅ Looking good! Keep hilling soil around plants for better tuber development.",
#         "emoji": "✅"
#     },

#     # ── Corn Diseases ──────────────────────────────────────────────────────────
#     "Corn_(maize)___Common_rust_": {
#         "display_name": "Corn Common Rust",
#         "type": "Fungal",
#         "severity": "Moderate",
#         "description": "Fungal rust disease causing characteristic orange pustules on corn leaves.",
#         "symptoms": ["Oval-shaped brick-red pustules on both leaf surfaces", "Pustules may darken to brown-black late in season", "Severe infection causes leaf death"],
#         "treatment": [
#             "Apply triazole fungicides (propiconazole, tebuconazole)",
#             "Plant rust-resistant hybrids",
#             "Early season applications give best results"
#         ],
#         "prevention": "Select resistant hybrid varieties. Scout fields from V5 growth stage.",
#         "farmer_tip": "🌽 Resistant hybrids are your best tool — check seed catalog resistance ratings.",
#         "emoji": "🌽"
#     },
#     "Corn_(maize)___Northern_Leaf_Blight": {
#         "display_name": "Northern Corn Leaf Blight",
#         "type": "Fungal",
#         "severity": "High",
#         "description": "Fungal disease causing characteristic long cigar-shaped lesions.",
#         "symptoms": ["Long grayish-green cigar-shaped lesions", "Lesions turn tan/brown with age", "Dark green sooty areas (spores) inside lesions"],
#         "treatment": [
#             "Apply fungicides at tassel emergence (azoxystrobin, propiconazole)",
#             "Plant resistant hybrids",
#             "Rotate crops with non-host crops"
#         ],
#         "prevention": "Bury crop residue by tillage. Plant resistant hybrids in high-risk areas.",
#         "farmer_tip": "📅 Timing is critical — apply fungicide at VT/R1 stage for maximum protection.",
#         "emoji": "🌽"
#     },
#     "Corn_(maize)___healthy": {
#         "display_name": "Healthy Corn",
#         "type": "Healthy",
#         "severity": "None",
#         "description": "Your corn plant appears healthy! No disease detected.",
#         "symptoms": [],
#         "treatment": ["Continue regular care and monitoring"],
#         "prevention": "Scout fields weekly from V5 stage onward for early disease detection.",
#         "farmer_tip": "✅ Corn looks healthy! Scout fields weekly during tasseling for best yields.",
#         "emoji": "✅"
#     },

#     # ── Grape Diseases ─────────────────────────────────────────────────────────
#     "Grape___Black_rot": {
#         "display_name": "Grape Black Rot",
#         "type": "Fungal",
#         "severity": "High",
#         "description": "Serious fungal disease causing fruit loss and leaf spots.",
#         "symptoms": ["Tan circular spots with dark borders on leaves", "Small black fruiting bodies in spots", "Fruit turns brown, shrivels into black mummies"],
#         "treatment": [
#             "Apply myclobutanil or mancozeb from bud break",
#             "Remove all mummified berries and infected leaves",
#             "Prune to improve canopy airflow",
#             "Apply protective sprays before rain events"
#         ],
#         "prevention": "Remove all old infected material before spring. Good sanitation is critical.",
#         "farmer_tip": "🍇 Remove mummified fruit immediately — they are the primary source of infection.",
#         "emoji": "🍇"
#     },
#     "Grape___healthy": {
#         "display_name": "Healthy Grape",
#         "type": "Healthy",
#         "severity": "None",
#         "description": "Your grapevine appears healthy! No disease detected.",
#         "symptoms": [],
#         "treatment": ["Continue regular care and monitoring"],
#         "prevention": "Prune annually for good airflow. Monitor regularly from bud break.",
#         "farmer_tip": "✅ Vines look great! Good canopy management prevents most grape diseases.",
#         "emoji": "✅"
#     },

#     # ── Default fallback ───────────────────────────────────────────────────────
#     "default": {
#         "display_name": "Unknown Disease",
#         "type": "Unknown",
#         "severity": "Unknown",
#         "description": "Disease information not found in database.",
#         "symptoms": ["Consult a local agricultural extension officer"],
#         "treatment": ["Consult with a local agronomist or plant pathologist"],
#         "prevention": "Regular monitoring and good agricultural practices.",
#         "farmer_tip": "📞 Contact your local agricultural extension office for expert advice.",
#         "emoji": "🔍"
#     }
# }


# # ─── Model Loader (singleton pattern) ─────────────────────────────────────────
# _model = None
# _labels = None

# def load_model_and_labels():
#     """Load model and labels once, reuse across requests (singleton)."""
#     global _model, _labels

#     if _model is None:
#         try:
#             import tensorflow as tf
#             print("🔄 Loading model...")
#             _model = tf.keras.models.load_model(MODEL_PATH)
#             print("✅ Model loaded successfully")
#         except Exception as e:
#             print(f"⚠️ Could not load model: {e}")
#             _model = None

#     if _labels is None:
#         try:
#             with open(LABELS_PATH, 'r') as f:
#                 _labels = json.load(f)
#             # Convert string keys to int
#             _labels = {int(k): v for k, v in _labels.items()}
#             print(f"✅ Labels loaded: {len(_labels)} classes")
#         except Exception as e:
#             print(f"⚠️ Could not load labels: {e}")
#             _labels = None

#     return _model, _labels


# def preprocess_image(image_bytes):
#     """
#     Preprocess image for model prediction.

#     Steps:
#       1. Open with PIL
#       2. Convert to RGB (handles PNG with alpha, grayscale, etc.)
#       3. Resize to 224x224
#       4. Normalize to [0, 1]
#       5. Add batch dimension → (1, 224, 224, 3)
#     """
#     img = Image.open(io.BytesIO(image_bytes))
#     img = img.convert('RGB')                          # Ensure 3 channels
#     img = img.resize((IMG_SIZE, IMG_SIZE))             # Resize to model input size
#     img_array = np.array(img, dtype=np.float32)       # Convert to numpy
#     img_array = img_array / 255.0                     # Normalize to [0, 1]
#     img_array = np.expand_dims(img_array, axis=0)     # Add batch dim
#     return img_array


# # def get_disease_info(class_name):
# #     """Look up disease info from database, with fallback."""
# #     if class_name in DISEASE_INFO:
# #         return DISEASE_INFO[class_name]

# #     # Try partial match (e.g., different formatting)
# #     for key in DISEASE_INFO:
# #         if key.lower().replace(" ", "_") in class_name.lower():
# #             return DISEASE_INFO[key]

# #     # Return default with the class name
# #     info = DISEASE_INFO["default"].copy()
# #     info["display_name"] = class_name.replace("___", " - ").replace("_", " ")
# #     return info
# def get_disease_info(class_name):
#     """Look up disease info — tries exact match, then fuzzy match."""

#     # 1. Exact match
#     if class_name in DISEASE_INFO:
#         return DISEASE_INFO[class_name]

#     # 2. Normalize and try again
#     normalized = class_name.lower().replace(" ", "_").replace("-", "_")
#     for key in DISEASE_INFO:
#         key_normalized = key.lower().replace(" ", "_").replace("-", "_")
#         if key_normalized == normalized:
#             return DISEASE_INFO[key]

#     # 3. Partial match (class name contains key or vice versa)
#     for key in DISEASE_INFO:
#         if key.lower() in class_name.lower() or class_name.lower() in key.lower():
#             return DISEASE_INFO[key]

#     # 4. Word overlap match
#     class_words = set(class_name.lower().replace("___", " ").replace("_", " ").split())
#     best_match = None
#     best_score = 0
#     for key in DISEASE_INFO:
#         key_words = set(key.lower().replace("___", " ").replace("_", " ").split())
#         overlap = len(class_words & key_words)
#         if overlap > best_score:
#             best_score = overlap
#             best_match = key
#     if best_score >= 2 and best_match:
#         return DISEASE_INFO[best_match]

#     # 5. Final fallback
#     info = DISEASE_INFO["default"].copy()
#     info["display_name"] = class_name.replace("___", " - ").replace("_", " ")
#     return info

# def predict(image_bytes):
#     """
#     Main prediction function.

#     Returns dict with:
#       - class_name: raw model output class
#       - display_name: human-readable name
#       - confidence: float (0–1)
#       - confidence_pct: string percentage
#       - is_healthy: bool
#       - disease_info: full disease info dict
#       - top3: list of top 3 predictions
#     """
#     model, labels = load_model_and_labels()

#     # ── Demo Mode (no model loaded) ──────────────────────────────────────────
#     if model is None or labels is None:
#         return _demo_prediction()

#     # ── Real Prediction ──────────────────────────────────────────────────────
#     img_array = preprocess_image(image_bytes)
#     predictions = model.predict(img_array)[0]          # Shape: (num_classes,)

#     top_idx = int(np.argmax(predictions))
#     confidence = float(predictions[top_idx])
#     class_name = labels.get(top_idx, "Unknown")

#     # Top 3 predictions
#     top3_indices = np.argsort(predictions)[::-1][:3]
#     top3 = []
#     for idx in top3_indices:
#         cn = labels.get(int(idx), "Unknown")
#         info = get_disease_info(cn)
#         top3.append({
#             "class": cn,
#             "name": info["display_name"],
#             "confidence": float(predictions[idx]),
#             "confidence_pct": f"{float(predictions[idx])*100:.1f}%"
#         })

#     disease_info = get_disease_info(class_name)

#     return {
#         "class_name": class_name,
#         "display_name": disease_info["display_name"],
#         "confidence": confidence,
#         "confidence_pct": f"{confidence*100:.1f}%",
#         "is_healthy": disease_info["type"] == "Healthy",
#         "disease_info": disease_info,
#         "top3": top3,
#         "model_loaded": True
#     }


# def _demo_prediction():
#     """Return a realistic demo result when no model is available."""
#     import random
#     demo_classes = [
#         "Tomato___Early_blight",
#         "Tomato___Late_blight",
#         "Potato___Late_blight",
#         "Apple___Apple_scab",
#         "Tomato___healthy",
#         "Corn_(maize)___Common_rust_"
#     ]
#     class_name = random.choice(demo_classes)
#     confidence = random.uniform(0.72, 0.97)
#     disease_info = get_disease_info(class_name)

#     top3 = []
#     other_classes = [c for c in demo_classes if c != class_name][:2]
#     confs = sorted([random.uniform(0.01, 0.15) for _ in range(2)], reverse=True)
#     for cn, cf in zip(other_classes, confs):
#         info = get_disease_info(cn)
#         top3.append({"class": cn, "name": info["display_name"],
#                      "confidence": cf, "confidence_pct": f"{cf*100:.1f}%"})

#     top3.insert(0, {
#         "class": class_name,
#         "name": disease_info["display_name"],
#         "confidence": confidence,
#         "confidence_pct": f"{confidence*100:.1f}%"
#     })

#     return {
#         "class_name": class_name,
#         "display_name": disease_info["display_name"],
#         "confidence": confidence,
#         "confidence_pct": f"{confidence*100:.1f}%",
#         "is_healthy": disease_info["type"] == "Healthy",
#         "disease_info": disease_info,
#         "top3": top3,
#         "model_loaded": False,
#         "demo_mode": True
#     }
"""
=============================================================
  Plant Disease Detection - Prediction & Disease Database
=============================================================
"""

import os
import numpy as np
import json
from PIL import Image
import io

IMG_SIZE    = 224      # ← Must match train_model.py IMG_SIZE
MODEL_PATH  = "model/plant_disease_model.h5"
LABELS_PATH = "model/class_labels.json"

# =============================================================
#   COMPLETE DISEASE DATABASE — Full details for every class
# =============================================================
DISEASE_INFO = {

    # ──────────────────────────────────────────────────────────
    #  APPLE DISEASES
    # ──────────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "display_name": "Apple Scab",
        "type": "Fungal",
        "severity": "Moderate",
        "emoji": "🍎",
        "description": (
            "Apple Scab is one of the most common and damaging fungal diseases of apple trees worldwide. "
            "Caused by the fungus Venturia inaequalis, it thrives in cool, moist spring weather. "
            "The disease overwinters in fallen infected leaves and releases spores in spring that infect "
            "new growth. Left untreated, it can cause significant fruit and leaf loss, reducing both "
            "yield and marketability of the crop."
        ),
        "symptoms": [
            "Dark olive-green to black velvety spots on upper leaf surfaces",
            "Spots may turn brown and corky as they age",
            "Scabby, rough, corky lesions on fruit surface",
            "Severely infected leaves curl, yellow, and drop prematurely",
            "Infected fruit may crack or become misshapen",
            "Lesions also appear on young green twigs and flower petals"
        ],
        "treatment": [
            "Apply fungicides (captan, mancozeb, myclobutanil) starting at bud break",
            "Spray every 7–10 days during wet spring weather",
            "Remove and destroy all fallen infected leaves in autumn",
            "Prune trees to improve air circulation and light penetration",
            "Use resistant apple varieties (Liberty, Freedom, Redfree)",
            "Apply urea to fallen leaves to speed decomposition of fungal spores"
        ],
        "prevention": (
            "Rake and destroy fallen leaves every autumn — this removes 90% of overwintering spores. "
            "Apply preventive fungicide sprays before rain events in spring. "
            "Plant resistant varieties in new orchards. Ensure good airflow by proper pruning."
        ),
        "farmer_tip": "🌱 Scout trees weekly from bud break through early summer. Early detection and spray timing saves up to 80% of crop value.",
    },

    "Apple___Black_rot": {
        "display_name": "Apple Black Rot",
        "type": "Fungal",
        "severity": "High",
        "emoji": "🍎",
        "description": (
            "Apple Black Rot, caused by the fungus Botryosphaeria obtusa, is a destructive disease "
            "affecting leaves, fruit, and woody parts of the tree. It causes fruit rot, leaf spots "
            "called 'frog-eye leaf spot', and cankers on branches. Infected fruit eventually shrivels "
            "into hard, black, mummified remains that cling to the tree and serve as sources of "
            "re-infection the following season."
        ),
        "symptoms": [
            "Circular brown leaf spots with purple or reddish-purple borders (frog-eye spots)",
            "Small black dots (pycnidia) visible in the center of leaf spots",
            "Fruit rot starting as small brown spots that enlarge rapidly",
            "Infected fruit turns completely black and mummifies on the tree",
            "Sunken, reddish-brown to black cankers on bark and branches",
            "Cankers may girdle and kill entire limbs"
        ],
        "treatment": [
            "Remove and destroy all mummified fruit from trees and ground immediately",
            "Prune out dead or cankered wood at least 15cm below visible infection",
            "Apply copper-based fungicides or captan during growing season",
            "Disinfect pruning tools with 10% bleach between cuts",
            "Avoid wounding trees — wounds are entry points for the fungus",
            "Improve tree vigor through proper fertilization and irrigation"
        ],
        "prevention": (
            "Thorough sanitation is the most important control measure. "
            "Remove all mummified fruit and prune dead wood before bud break. "
            "Avoid leaving pruning wounds — seal large cuts. "
            "Clean up all fallen fruit and leaves at end of every season."
        ),
        "farmer_tip": "🧹 Sanitation is everything for black rot. Remove every mummified fruit you can see — each one contains millions of spores for next season.",
    },

    "Apple___Cedar_apple_rust": {
        "display_name": "Cedar Apple Rust",
        "type": "Fungal",
        "severity": "Moderate",
        "emoji": "🍎",
        "description": (
            "Cedar Apple Rust is a unique fungal disease caused by Gymnosporangium juniperi-virginianae "
            "that requires TWO different host plants to complete its lifecycle — apple/crabapple trees "
            "and eastern red cedar or juniper trees. In spring, orange gelatinous galls on cedars release "
            "spores that infect apples. The disease cannot spread apple-to-apple; it must cycle through "
            "a cedar host each year."
        ),
        "symptoms": [
            "Bright orange-yellow circular spots on upper surface of apple leaves",
            "Spots develop tube-like or hair-like orange structures on leaf undersides",
            "Infected leaves may drop prematurely causing defoliation",
            "Orange lesions may also appear on fruit and green twigs",
            "On cedar trees: orange gelatinous star-shaped galls in spring after rain",
            "Galls on cedar turn brown and woody by summer"
        ],
        "treatment": [
            "Apply fungicides (myclobutanil, propiconazole, or trifloxystrobin) from pink bud stage",
            "Spray every 7–10 days through petal fall and 2 more times after",
            "Remove nearby eastern red cedar or juniper trees if feasible",
            "Cut off orange galls from cedar trees before they release spores",
            "Plant rust-resistant apple varieties in new plantings"
        ],
        "prevention": (
            "Plant rust-resistant apple varieties (Enterprise, Liberty, Redfree). "
            "Apply fungicides preventively from pink bud stage through early June. "
            "Remove eastern red cedar trees within 300 meters of orchard if possible. "
            "Monitor cedar trees in late winter for developing galls."
        ),
        "farmer_tip": "🌲 Check nearby cedar trees in February/March for orange galls. Cut them off BEFORE spring rains — once they release spores, infection has already started.",
    },

    "Apple___healthy": {
        "display_name": "Healthy Apple",
        "type": "Healthy",
        "severity": "None",
        "emoji": "✅",
        "description": (
            "Great news! Your apple plant appears completely healthy with no signs of disease. "
            "The leaves show normal green color, proper shape, and no spots, lesions, or discoloration. "
            "Continue your current care practices to maintain plant health and prevent future disease outbreaks."
        ),
        "symptoms": [],
        "treatment": [
            "Continue regular watering and fertilization schedule",
            "Monitor plants weekly for any early signs of disease",
            "Maintain proper pruning for good airflow",
            "Apply preventive fungicide sprays in early spring as precaution"
        ],
        "prevention": (
            "Maintain good airflow through annual pruning. Apply balanced fertilizer in spring. "
            "Use mulch around base to retain moisture. Remove fallen leaves and fruit promptly."
        ),
        "farmer_tip": "✅ Keep up the great work! Regular weekly monitoring and good sanitation prevents most apple diseases before they start.",
    },

    # ──────────────────────────────────────────────────────────
    #  TOMATO DISEASES
    # ──────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "display_name": "Tomato Bacterial Spot",
        "type": "Bacterial",
        "severity": "High",
        "emoji": "🍅",
        "description": (
            "Tomato Bacterial Spot is caused by four species of Xanthomonas bacteria and is one of "
            "the most damaging tomato diseases in warm, wet climates. It affects leaves, stems, and "
            "fruit, reducing both yield and quality. The bacteria spread rapidly through rain splash, "
            "wind-driven rain, and contaminated tools or hands. Infected fruit cannot be sold fresh "
            "due to unsightly scabs and is highly susceptible to secondary rots."
        ),
        "symptoms": [
            "Small, water-soaked, greasy-looking spots on leaves (1–3mm)",
            "Spots enlarge and turn brown with yellow halos around them",
            "Centers of spots may fall out giving a shot-hole appearance",
            "Raised, dark brown, scab-like spots on green fruit surface",
            "Fruit spots have rough, warty texture and remain as permanent scars",
            "Severe leaf infection causes yellowing and complete defoliation",
            "Dark, water-soaked streaks on stems and leaf petioles"
        ],
        "treatment": [
            "Apply copper-based bactericides (copper hydroxide, copper sulfate) immediately",
            "Add mancozeb to copper sprays to improve effectiveness",
            "Spray every 5–7 days during warm, wet weather",
            "Remove and destroy heavily infected plants and leaves",
            "Avoid overhead irrigation — switch to drip watering at soil level",
            "Use disease-free certified seeds or treat seeds with hot water (50°C for 25 min)",
            "Disinfect all tools and equipment with 10% bleach solution after use"
        ],
        "prevention": (
            "Use certified disease-free seeds and transplants. "
            "Avoid working in fields when plants are wet. "
            "Use drip irrigation instead of overhead sprinklers. "
            "Stake and cage plants to improve airflow. "
            "Rotate crops — do not plant tomatoes in same location for 2–3 years."
        ),
        "farmer_tip": "💧 Switching from overhead sprinklers to drip irrigation alone reduces bacterial spot spread by up to 60%. Wet foliage is the #1 enabler of this disease.",
    },

    "Tomato___Early_blight": {
        "display_name": "Tomato Early Blight",
        "type": "Fungal",
        "severity": "Moderate",
        "emoji": "🍅",
        "description": (
            "Tomato Early Blight, caused by Alternaria solani, is one of the most common tomato diseases "
            "worldwide. Despite its name, it typically appears mid-season on older, lower leaves first. "
            "The fungus survives in soil and infected plant debris and spreads through rain splash and wind. "
            "While rarely killing plants outright, severe infection causes significant defoliation, "
            "reducing photosynthesis and fruit size. Stressed or under-fertilized plants are most susceptible."
        ),
        "symptoms": [
            "Dark brown to black circular spots with distinctive concentric rings (target/bull's-eye pattern)",
            "Yellow chlorotic halo surrounding each lesion",
            "Older, lower leaves affected first — disease progresses upward through plant",
            "Stems develop dark, sunken, elongated lesions (collar rot on seedlings)",
            "Fruit develops dark, leathery, sunken lesions near stem end",
            "Severe infection causes complete defoliation of lower plant sections"
        ],
        "treatment": [
            "Apply fungicides: chlorothalonil, mancozeb, or azoxystrobin",
            "Begin sprays when first symptoms appear or when conditions favor disease",
            "Spray every 7–10 days, more frequently in wet weather",
            "Remove and dispose of infected leaves (do not compost them)",
            "Mulch soil to prevent spore splash from soil to lower leaves",
            "Improve plant nutrition — especially calcium and potassium levels",
            "Stake or cage plants to keep foliage off ground"
        ],
        "prevention": (
            "Rotate crops — avoid planting tomatoes or potatoes in same spot for 3 years. "
            "Use certified disease-free transplants. Remove plant debris at end of season. "
            "Maintain adequate plant nutrition throughout season. Water at base, not overhead."
        ),
        "farmer_tip": "🔄 Crop rotation is your single best long-term defense. Also, remove the bottom 30cm of leaves on young plants — this dramatically slows disease spread all season.",
    },

    "Tomato___Late_blight": {
        "display_name": "Tomato Late Blight",
        "type": "Fungal/Oomycete",
        "severity": "Critical",
        "emoji": "🍅",
        "description": (
            "Tomato Late Blight, caused by Phytophthora infestans, is the most destructive tomato and "
            "potato disease in the world — the same pathogen that caused the Irish Potato Famine. "
            "Under ideal conditions (cool temperatures 10–25°C, high humidity), it can destroy "
            "an entire crop within 7–10 days. The disease spreads with terrifying speed through airborne "
            "spores and infected water. There is NO cure once infection is established — prevention and "
            "immediate action are absolutely critical."
        ),
        "symptoms": [
            "Large, irregular, dark water-soaked lesions on leaves — often at leaf tips or edges",
            "White, fuzzy mold growth on undersides of infected leaves in humid conditions",
            "Infected areas turn brown-black and collapse rapidly within days",
            "Dark brown to black greasy lesions appear on stems",
            "Fruit develops firm, brown, corky lesions that can penetrate deep into flesh",
            "Entire plant can collapse and die within 1–2 weeks of first symptoms",
            "Distinctive musty, rotting odor emanates from infected plants and fields"
        ],
        "treatment": [
            "Apply fungicides IMMEDIATELY at first sign: metalaxyl+mancozeb (Ridomil Gold), chlorothalonil",
            "Spray every 5–7 days — do not skip applications under any circumstances",
            "Remove ALL infected plant material and seal in plastic bags before disposal",
            "Do NOT compost infected material — it spreads disease to next season",
            "Destroy severely affected plants completely — do not leave in field",
            "Warn neighboring farmers immediately — disease spreads for kilometers by wind",
            "Consider prophylactic spraying of all nearby tomato and potato plants"
        ],
        "prevention": (
            "Plant resistant varieties (Mountain Magic, Defiant, Plum Regal). "
            "Monitor weather forecasts — late blight thrives when temps stay below 25°C with rain. "
            "Apply preventive fungicide before predicted wet/cool weather events. "
            "Avoid overhead irrigation. Ensure excellent airflow through plant spacing and staking."
        ),
        "farmer_tip": "⚠️ URGENT: Late blight can destroy your ENTIRE crop in one week. If you see even 3–4 infected leaves, act THAT DAY. Call your local agricultural extension officer immediately.",
    },

    "Tomato___Leaf_Miner": {
        "display_name": "Tomato Leaf Miner",
        "type": "Pest",
        "severity": "Moderate",
        "emoji": "🍅",
        "description": (
            "Tomato Leaf Miners (Liriomyza spp.) are tiny flies whose larvae tunnel between the upper and "
            "lower surfaces of leaves, creating characteristic serpentine (winding) white trails called mines. "
            "The adult flies also cause damage by puncturing leaves to feed on plant sap. While the mines "
            "themselves rarely kill plants, severe infestations reduce photosynthesis, weaken plants, and "
            "can introduce secondary fungal infections through the feeding wounds."
        ),
        "symptoms": [
            "Winding, serpentine white or yellowish trails (mines) visible on leaf surfaces",
            "Mines are narrow at start and widen as larva grows inside",
            "Tiny round puncture marks on leaves from adult feeding and egg-laying",
            "Blistered, distorted, or papery patches on heavily mined leaves",
            "Presence of tiny yellowish flies (2mm) hovering on plants",
            "Heavily infested leaves turn yellow and drop prematurely",
            "Small white or yellowish maggots visible inside mines when leaf is held to light"
        ],
        "treatment": [
            "Apply spinosad (organic-approved) as first-choice insecticide",
            "Use abamectin — translaminar action works inside leaf tissue where larvae hide",
            "Apply cyromazine which specifically targets young larvae inside mines",
            "Use yellow sticky traps to monitor and reduce adult fly populations",
            "Release biological control agents: Diglyphus isaea or Dacnusa sibirica (parasitic wasps)",
            "Remove and destroy heavily infested leaves immediately to reduce population",
            "Avoid pyrethroid insecticides — they kill beneficial insects that naturally control miners"
        ],
        "prevention": (
            "Use insect-proof mesh row covers on seedlings and young transplants. "
            "Inspect all transplants carefully before planting — reject any with mines. "
            "Install yellow sticky traps at planting time for early detection. "
            "Maintain populations of natural enemies by avoiding broad-spectrum insecticides. "
            "Remove crop debris promptly after harvest."
        ),
        "farmer_tip": "🪤 Install yellow sticky traps at transplanting time — they're cheap, chemical-free, and give early warning before populations explode. One trap per 100 square meters is ideal.",
    },

    "Tomato___Septoria_leaf_spot": {
        "display_name": "Septoria Leaf Spot",
        "type": "Fungal",
        "severity": "Moderate",
        "emoji": "🍅",
        "description": (
            "Septoria Leaf Spot, caused by Septoria lycopersici, is one of the most common and destructive "
            "foliage diseases of tomato worldwide. It appears as numerous small, circular spots on leaves "
            "and is recognized by the tiny black dots (pycnidia — fungal fruiting bodies) visible in the "
            "center of each spot. Like early blight, it starts on lower leaves and progresses upward. "
            "Severe infection causes complete defoliation, exposing fruit to sunscald and reducing yields significantly."
        ),
        "symptoms": [
            "Numerous small (3–6mm) circular spots with dark brown borders and grayish-white centers",
            "Tiny black dots (pycnidia) visible in center of spots — the key identifying feature",
            "Yellow halo may surround spots on susceptible varieties",
            "Lower and older leaves affected first — disease progresses steadily upward",
            "Heavily infected leaves turn completely yellow and drop",
            "Stems and flower stalks may also become infected",
            "Fruit is rarely directly infected but sunscalds when leaves drop exposing it"
        ],
        "treatment": [
            "Apply fungicides: chlorothalonil, mancozeb, copper-based fungicides, or azoxystrobin",
            "Begin treatment at first symptom appearance — do not delay",
            "Spray every 7–10 days, more frequently during wet weather periods",
            "Remove infected leaves immediately and dispose of (do not compost)",
            "Avoid wetting foliage when watering — use drip irrigation or water at base",
            "Stake or cage plants to improve air circulation through canopy",
            "Remove lower leaves proactively to 30cm height to slow spread"
        ],
        "prevention": (
            "Space plants at least 60cm apart for excellent airflow. "
            "Use mulch to prevent soil splash onto lower leaves. "
            "Rotate crops — fungus survives in soil and debris for 1+ years. "
            "Use certified disease-free seeds and transplants. "
            "Clean up all plant debris at end of season without fail."
        ),
        "farmer_tip": "✂️ Proactively remove all leaves below 30cm height when plants are young — this one simple step dramatically slows Septoria spread throughout the entire season.",
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "display_name": "Tomato Spider Mites (Two-Spotted)",
        "type": "Pest",
        "severity": "Moderate",
        "emoji": "🍅",
        "description": (
            "Two-spotted spider mites (Tetranychus urticae) are among the most economically damaging "
            "pests of tomatoes and hundreds of other crops worldwide. Despite being called spider mites, "
            "they are arachnids — closely related to spiders and ticks. They pierce individual plant cells "
            "and suck out the contents, causing the characteristic stippled, bronzed appearance. "
            "They thrive in hot, dry, dusty conditions (above 27°C) and reproduce explosively — "
            "a single female can lay 100+ eggs, and a full generation completes in just 5–7 days. "
            "Severe infestations can fully defoliate and kill plants within 2–3 weeks if untreated."
        ),
        "symptoms": [
            "Tiny yellow or white speckles/stippling on upper leaf surface (each speck = one feeding puncture)",
            "Leaves develop a bronze, silvery, or bleached appearance overall",
            "Fine silky webbing on undersides of leaves, between stems, and at growing tips",
            "Tiny moving dots (the mites — 0.3–0.5mm) visible on leaf undersides under magnification",
            "Leaves curl, dry out, and drop prematurely in severe infestations",
            "Severely affected plants look dusty and bleached when viewed from a distance",
            "Stunted plant growth and significantly reduced fruit yield and quality"
        ],
        "treatment": [
            "Spray strong jets of water forcefully on leaf undersides daily to dislodge and kill mites",
            "Apply neem oil spray (2 tbsp per liter of water + few drops dish soap) every 3–5 days",
            "Use insecticidal soap solution — spray thoroughly covering all leaf surfaces especially undersides",
            "Apply miticides: abamectin (Agri-Mek), bifenazate (Acramite), or spiromesifen (Oberon)",
            "Release predatory mites: Phytoseiulus persimilis — the most effective biological control",
            "Remove and destroy heavily webbed or infested leaves immediately",
            "Avoid broad-spectrum insecticides (pyrethroids) — they kill natural predators causing mite outbreaks",
            "Rotate chemical classes to prevent resistance development in mite populations"
        ],
        "prevention": (
            "Keep plants consistently well-watered — drought-stressed plants are 3x more attractive to mites. "
            "Maintain adequate humidity around plants when possible. "
            "Avoid dusty conditions — dust suppresses natural predators of mites. "
            "Inspect leaf undersides weekly from early in the season. "
            "Introduce predatory mites early as preventive biological control. "
            "Use reflective silver mulch — it disorients and repels adult mites. "
            "Avoid excessive nitrogen fertilization which produces succulent growth that mites prefer."
        ),
        "farmer_tip": "💦 A strong water spray on leaf undersides EVERY DAY controls mild and moderate infestations completely without chemicals. Start early — once you see webbing, populations are already in the thousands. Act immediately!",
    },

    "Tomato___Spider_mites_Two-spotted_spider_mite": {
        "display_name": "Tomato Spider Mites (Two-Spotted)",
        "type": "Pest",
        "severity": "Moderate",
        "emoji": "🍅",
        "description": (
            "Two-spotted spider mites (Tetranychus urticae) pierce plant cells and suck out contents, "
            "causing yellowing, stippling, and leaf death. They thrive in hot, dry conditions and "
            "reproduce extremely fast — a full generation in just 5–7 days. "
            "Severe infestations can defoliate an entire plant within 2–3 weeks if untreated."
        ),
        "symptoms": [
            "Tiny yellow or white speckles (stippling) on upper leaf surface",
            "Leaves turn bronze, yellow, or silvery overall",
            "Fine silky webbing on undersides of leaves and between stems",
            "Tiny moving dots (mites) visible on leaf undersides with magnification",
            "Premature leaf drop in severe infestations",
            "Stunted plant growth and reduced fruit yield"
        ],
        "treatment": [
            "Spray strong jets of water on leaf undersides to dislodge mites",
            "Apply neem oil spray (2 tbsp per liter water) every 3–5 days",
            "Use insecticidal soap solution on all leaf surfaces",
            "Apply miticides: abamectin, bifenazate, or spiromesifen",
            "Release predatory mites (Phytoseiulus persimilis) for biological control",
            "Remove and destroy heavily infested leaves immediately"
        ],
        "prevention": (
            "Keep plants well-watered — drought-stressed plants attract mites. "
            "Maintain humidity. Inspect leaf undersides weekly. "
            "Use reflective mulch to repel adult mites."
        ),
        "farmer_tip": "💦 Daily water spray on leaf undersides controls mild infestations without any chemicals. Start early before webbing appears!",
    },

    "Tomato___Target_Spot": {
        "display_name": "Tomato Target Spot",
        "type": "Fungal",
        "severity": "Moderate",
        "emoji": "🍅",
        "description": (
            "Tomato Target Spot, caused by the fungus Corynespora cassiicola, produces distinctive "
            "circular lesions with concentric rings resembling a target or bullseye on leaves, stems, "
            "and fruit. It is common in warm, humid tropical and subtropical regions. "
            "The disease causes defoliation, reducing photosynthesis and yield. "
            "Fruit infections cause direct crop loss and make tomatoes completely unmarketable."
        ),
        "symptoms": [
            "Brown circular spots with concentric target-like rings on leaves (5–10mm diameter)",
            "Yellow halo surrounding lesions on leaves",
            "Spots on fruit start small and dark, enlarging into sunken, water-soaked lesions",
            "Leaf defoliation in severe cases — lower leaves first, spreading upward",
            "Dark brown lesions may also appear on stems and petioles",
            "In humid conditions, olive-colored fungal growth visible in lesion centers"
        ],
        "treatment": [
            "Apply fungicides: azoxystrobin, chlorothalonil, or difenoconazole",
            "Begin treatment immediately at first symptom appearance",
            "Spray every 7–14 days depending on weather conditions",
            "Remove and destroy infected leaves immediately upon detection",
            "Avoid overhead irrigation — water at base of plants only",
            "Improve airflow by pruning lower leaves and staking all plants"
        ],
        "prevention": (
            "Ensure good air circulation — space plants properly and stake or cage all plants. "
            "Use drip irrigation instead of overhead watering. "
            "Rotate crops with non-solanaceous plants for 2+ years. "
            "Remove and destroy all crop debris at end of season."
        ),
        "farmer_tip": "🌿 Thin out dense canopy by removing overlapping branches — improved airflow reduces humidity inside the plant by 30–40%, making conditions far less favorable for this fungus.",
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "display_name": "Tomato Yellow Leaf Curl Virus",
        "type": "Viral",
        "severity": "Critical",
        "emoji": "🍅",
        "description": (
            "Tomato Yellow Leaf Curl Virus (TYLCV) is one of the most devastating viral diseases of "
            "tomato globally, causing crop losses of 20–100% in affected fields. It is spread "
            "exclusively by the silverleaf whitefly (Bemisia tabaci) — a tiny insect that acquires "
            "the virus in just 15–30 minutes of feeding on infected plants and can transmit it for weeks. "
            "There is absolutely NO cure for infected plants. Once a plant shows symptoms, "
            "it will NEVER recover and serves only as a continuous source of virus for healthy plants nearby."
        ),
        "symptoms": [
            "Upward and inward curling of leaf margins — leaves form distinctive cup or bowl shapes",
            "Severe yellowing (chlorosis) of leaf margins and between veins",
            "Stunted, bushy plant growth — internodes shorten dramatically",
            "Leaves become small, thick, leathery, and crinkled",
            "Flowers drop before fruit sets, or fruit fails to develop at all",
            "Plants infected early in season produce virtually no fruit",
            "Presence of tiny white whiteflies on undersides of leaves throughout"
        ],
        "treatment": [
            "NO CURE EXISTS — remove and destroy ALL infected plants immediately",
            "Bag infected plants in plastic before removing to prevent releasing virus-carrying whiteflies",
            "Control whitefly population aggressively with imidacloprid or thiamethoxam insecticides",
            "Apply insecticidal soap or neem oil for organic whitefly control",
            "Install yellow sticky traps throughout field to monitor and reduce whitefly populations",
            "Do NOT handle infected plants then move to healthy areas without disinfecting"
        ],
        "prevention": (
            "Plant TYLCV-resistant or tolerant varieties — many exist, check with local seed suppliers. "
            "Use reflective silver mulch at planting — reduces whitefly landing by 50–80%. "
            "Install fine mesh (50 mesh) row covers on young transplants to exclude whiteflies. "
            "Control weeds around field — many serve as virus and whitefly reservoirs. "
            "Apply imidacloprid soil drench at transplanting for systemic whitefly control. "
            "Scout weekly for whiteflies — control must start BEFORE virus spreads."
        ),
        "farmer_tip": "🚫 Remove infected plants THE SAME DAY you find them — wrap in plastic bag first to trap whiteflies. Every infected plant left in field spreads TYLCV to 10–20 new plants per week.",
    },

    "Tomato___Tomato_mosaic_virus": {
        "display_name": "Tomato Mosaic Virus",
        "type": "Viral",
        "severity": "High",
        "emoji": "🍅",
        "description": (
            "Tomato Mosaic Virus (ToMV) is one of the most stable and persistent plant viruses known — "
            "it can survive for years in dried plant debris, in soil, and on contaminated surfaces and tools. "
            "Unlike most plant viruses, it does NOT require an insect vector to spread. "
            "It spreads primarily through direct contact during handling, through contaminated tools, "
            "stakes, and even through cigarette smoke (since tobacco is also a host). "
            "A single infected plant can contaminate hundreds of others during normal cultivation activities."
        ),
        "symptoms": [
            "Mosaic pattern of alternating light green and dark green patches on leaves",
            "Leaves may develop fernlike or oak-leaf distortion with narrow, elongated leaflets",
            "Stunted, bushy plant growth overall",
            "Fruit may show yellow blotchy or streaked discoloration",
            "Internal browning of fruit wall visible when cut (especially in cool conditions)",
            "Blossom drop and significantly reduced fruit set",
            "Mottled, distorted, twisted growth at growing shoot tips"
        ],
        "treatment": [
            "NO chemical cure is available for any plant virus — this is true for all viruses",
            "Remove and destroy ALL infected plants immediately to prevent further spread",
            "Disinfect ALL tools with 10% bleach (sodium hypochlorite) solution between every plant",
            "Wash hands thoroughly with soap and water before handling any plants",
            "Do not handle plants after touching potentially infected material without washing",
            "Milk solution (10% skim milk) sprayed on plants can help prevent spread during pruning operations"
        ],
        "prevention": (
            "Use certified virus-free seeds — seed can carry this virus internally. "
            "Treat seeds with 10% trisodium phosphate for 15 minutes before planting. "
            "Always disinfect tools between every plant during pruning — use bleach dip. "
            "Wash hands before entering greenhouse or touching any plants. "
            "Do not smoke near plants — tobacco products carry related viruses. "
            "Plant resistant varieties with the Tm-2 resistance gene where available."
        ),
        "farmer_tip": "🧤 This virus spreads through TOUCH alone. Always wash hands before handling plants and disinfect pruning tools between every single plant. Inconvenient but prevents devastating crop losses.",
    },

    "Tomato___healthy": {
        "display_name": "Healthy Tomato",
        "type": "Healthy",
        "severity": "None",
        "emoji": "✅",
        "description": (
            "Excellent! Your tomato plant appears completely healthy with no signs of disease or pest damage. "
            "The leaves show uniform green color, normal shape, and no spots, lesions, or discoloration. "
            "Healthy tomatoes are vigorous growers — continue your current management practices to maintain this."
        ),
        "symptoms": [],
        "treatment": [
            "Continue consistent watering — tomatoes need 25–50mm of water per week",
            "Maintain regular fertilization (balanced NPK early, then phosphorus and potassium at fruiting)",
            "Continue weekly scouting for early disease or pest signs on all plant surfaces",
            "Stake or cage plants for support as they grow taller"
        ],
        "prevention": (
            "Maintain consistent soil moisture — fluctuations cause blossom end rot. "
            "Apply mulch to retain moisture and suppress disease splash from soil. "
            "Stake or cage all plants for airflow and to keep fruit off ground. "
            "Perform weekly inspections of leaves (both surfaces) for early pest and disease detection."
        ),
        "farmer_tip": "✅ Healthy plants! Consistent watering, good staking, and weekly inspections are your three best tools to keep tomatoes productive all season long.",
    },

    # ──────────────────────────────────────────────────────────
    #  POTATO DISEASES
    # ──────────────────────────────────────────────────────────
    "Potato___Early_blight": {
        "display_name": "Potato Early Blight",
        "type": "Fungal",
        "severity": "Moderate",
        "emoji": "🥔",
        "description": (
            "Potato Early Blight, caused by Alternaria solani, is a common fungal disease affecting "
            "potato crops worldwide. The fungus is soil-borne and survives in infected plant debris. "
            "It typically appears on older, lower leaves first and progresses upward during the season. "
            "While primarily a foliar disease, severe infections reduce the photosynthetic capacity of "
            "the plant, leading to smaller tubers and reduced yields. Plants under nutritional stress, "
            "particularly those deficient in nitrogen or potassium, are most severely affected."
        ),
        "symptoms": [
            "Dark brown to black circular spots with characteristic concentric rings (target-board pattern)",
            "Yellow chlorotic area surrounds each lesion clearly",
            "Older, lower leaves affected first — progresses up the plant as season advances",
            "Severely infected leaves turn yellow and die off",
            "Stem lesions appear as dark, elongated, sunken areas on stems",
            "Tuber infections: dark, sunken, corky lesions with distinct margins visible on skin"
        ],
        "treatment": [
            "Apply fungicides: chlorothalonil, mancozeb, or azoxystrobin",
            "Begin spraying when plants reach 15–20cm height or at very first symptoms",
            "Spray every 7–14 days depending on disease pressure and rainfall frequency",
            "Remove and destroy infected foliage from field",
            "Hill soil around plants regularly — protects tubers from infection via soil splash",
            "Ensure adequate potassium and nitrogen fertilization — strengthens plant resistance",
            "Irrigate in morning so foliage has time to dry before evening"
        ],
        "prevention": (
            "Use certified disease-free seed potatoes without exception. "
            "Rotate crops — do not plant potatoes or tomatoes in same ground for 3 years. "
            "Plant resistant varieties where available locally. "
            "Avoid excessive vine damage at harvest which allows tuber infection. "
            "Ensure proper plant nutrition is maintained throughout entire season."
        ),
        "farmer_tip": "🥔 Well-fed, well-watered potato plants resist early blight far better than stressed ones. Never skip fertilization — a strong plant fights off fungal attack much more effectively.",
    },

    "Potato___Late_blight": {
        "display_name": "Potato Late Blight",
        "type": "Fungal/Oomycete",
        "severity": "Critical",
        "emoji": "🥔",
        "description": (
            "Potato Late Blight, caused by Phytophthora infestans, is the single most devastating plant "
            "disease in human history — it caused the Irish Potato Famine (1845–1849), killing over one "
            "million people and causing two million more to emigrate from Ireland. Today it remains a major "
            "threat to global food security, causing billions of dollars in crop losses annually worldwide. "
            "Under favorable conditions (cool, wet weather 10–25°C), it can destroy an entire field in "
            "less than 2 weeks. The pathogen is not a true fungus but an oomycete (water mold), which "
            "means many traditional fungicides are ineffective — specific oomycete-targeting products are essential."
        ),
        "symptoms": [
            "Water-soaked, dark green to brown-black irregular lesions on leaves — often starting at tips or edges",
            "White cottony or fuzzy sporulation on undersides of leaves in humid conditions — highly diagnostic",
            "Lesions spread rapidly, killing entire leaves within just 2–3 days",
            "Dark brown to black lesions on stems, often causing complete stem collapse",
            "Tubers: reddish-brown, granular dry rot just below skin, extends deep into flesh",
            "Entire field takes on a burnt, blackened, collapsed appearance in severe outbreaks",
            "Distinctive musty, unpleasant rotting odor emanates from infected plants"
        ],
        "treatment": [
            "Apply oomycete-specific fungicides IMMEDIATELY: metalaxyl+mancozeb (Ridomil Gold MZ), cymoxanil",
            "Spray every 5–7 days without fail — do not extend intervals even slightly during active outbreak",
            "Remove and destroy ALL infected foliage — bag before removing to contain and trap spores",
            "Do NOT compost infected material — dispose by burning or deep burial away from fields",
            "Hill up soil aggressively around plants to protect tubers from spore contamination",
            "Consider emergency harvest if outbreak is severe — sacrifice vine to save tuber",
            "Warn neighboring farmers immediately — disease spreads for many kilometers by wind"
        ],
        "prevention": (
            "Plant certified disease-free seed tubers without exception. "
            "Use resistant varieties (Sarpo Mira, Cara, Stirling — check local recommendations). "
            "Apply preventive fungicide sprays before predicted cool, wet weather events. "
            "Use forecasting systems (BlightWatch, BLITECAST) to time spray applications. "
            "Destroy all volunteer potato plants which harbor disease between seasons. "
            "Ensure hills do not erode — exposed tubers are highly susceptible. "
            "Harvest in dry conditions and cure tubers properly before storage."
        ),
        "farmer_tip": "⚠️ CRITICAL: Late blight can destroy your ENTIRE field within 10 days. If you see even ONE infected plant, call your agricultural extension officer TODAY and start spraying immediately. Do not wait.",
    },

    "Potato___healthy": {
        "display_name": "Healthy Potato",
        "type": "Healthy",
        "severity": "None",
        "emoji": "✅",
        "description": (
            "Your potato plant appears completely healthy! No signs of disease or pest damage are visible. "
            "The foliage shows uniform green color with normal leaf shape and texture. "
            "Continue your current management practices to maintain plant health through the growing season and into harvest."
        ),
        "symptoms": [],
        "treatment": [
            "Continue consistent watering — especially critical during tuber bulking stage",
            "Maintain regular hilling to cover tubers and prevent greening",
            "Monitor weekly for any early signs of late blight, especially after cool, wet weather",
            "Apply balanced fertilizer as needed based on plant visual appearance"
        ],
        "prevention": (
            "Hill plants regularly to keep tubers covered (prevents greening and reduces late blight tuber infection). "
            "Maintain consistent moisture — irregular watering causes hollow heart in tubers. "
            "Scout fields weekly, especially monitoring lower leaves for early blight symptoms. "
            "Avoid overhead irrigation in late afternoon or evening — wet foliage overnight invites disease."
        ),
        "farmer_tip": "✅ Potato looks great! Remember: regular hilling is your best investment — it protects tubers, improves yield, and reduces late blight tuber infection all at once.",
    },

    # ──────────────────────────────────────────────────────────
    #  CORN DISEASES
    # ──────────────────────────────────────────────────────────
    "Corn_(maize)___Common_rust_": {
        "display_name": "Corn Common Rust",
        "type": "Fungal",
        "severity": "Moderate",
        "emoji": "🌽",
        "description": (
            "Corn Common Rust, caused by Puccinia sorghi, is a widespread fungal disease that produces "
            "characteristic brick-red to cinnamon-brown pustules on corn leaves. Unlike other rusts, "
            "common rust spores are airborne and can travel hundreds of miles on wind currents from "
            "overwintering populations in tropical regions. The disease develops most rapidly in cool "
            "to moderate temperatures (16–23°C) with high humidity or extended leaf wetness. "
            "While usually manageable in field corn with resistant hybrids, it can cause significant "
            "yield losses in sweet corn and susceptible field corn hybrids when infection occurs before tasseling."
        ),
        "symptoms": [
            "Oval to elongated brick-red to cinnamon-brown pustules (uredia) on both leaf surfaces",
            "Pustules are raised, powdery, and rupture through the leaf epidermis naturally",
            "Reddish-brown spore powder easily rubs off on fingers when touched",
            "Pustules may darken to black-brown (telia) late in the growing season",
            "Severe infection causes leaves to yellow and die prematurely",
            "Heavy infections on both leaf surfaces give leaves a rusty, dusty appearance overall",
            "Pustules may also appear on leaf sheaths, husks, and occasionally tassels"
        ],
        "treatment": [
            "Apply triazole fungicides: propiconazole (Tilt), tebuconazole, or prothioconazole",
            "Strobilurin fungicides (azoxystrobin, pyraclostrobin) are also very effective",
            "Apply at early disease onset — before 5% leaf area infected for best results",
            "Single application often sufficient in field corn if timing is correct",
            "Sweet corn may require 2 applications 10–14 days apart",
            "Application at VT (tasseling) or R1 (silking) gives best yield protection"
        ],
        "prevention": (
            "Plant resistant or tolerant hybrid varieties — this is the most economical control method. "
            "Check seed catalog resistance ratings (scale 1–9, lower = more resistant). "
            "Scout fields from V5 (5-leaf) stage onward, paying attention to lower leaves first. "
            "Early planting may allow crop to mature before severe rust pressure develops in some regions."
        ),
        "farmer_tip": "🌽 Choosing a rust-resistant hybrid is your most cost-effective tool. Check the seed catalog resistance rating before buying — it costs nothing extra and can save significant spray costs.",
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "display_name": "Northern Corn Leaf Blight",
        "type": "Fungal",
        "severity": "High",
        "emoji": "🌽",
        "description": (
            "Northern Corn Leaf Blight (NCLB), caused by Exserohilum turcicum, is one of the most "
            "economically important foliar diseases of corn in temperate regions worldwide. "
            "It is immediately recognizable by its distinctive long, cigar-shaped or elliptical gray-green "
            "lesions. The disease is favored by moderate temperatures (18–27°C) and periods of heavy dew "
            "or rain. Losses are most severe when disease develops before tasseling — infection at this "
            "stage can reduce yields by 30–50% in susceptible hybrids. The fungus survives in infected "
            "crop residue and spores are dispersed by wind and rain splash."
        ),
        "symptoms": [
            "Long (2.5–15cm), cigar-shaped or elliptical lesions on leaves — the key diagnostic feature",
            "Lesions initially appear grayish-green to tan, turning tan-brown as they age",
            "Dark olive-green to black sooty areas within older lesions from fungal sporulation",
            "Lower leaves typically infected first — disease progresses steadily upward",
            "Lesions may coalesce in severe infections, killing entire leaves rapidly",
            "Infected husks show tan-brown discoloration on outer layers",
            "Under humid conditions, dark olive sporulation clearly visible in lesion centers"
        ],
        "treatment": [
            "Apply fungicides at VT/R1 growth stage (tasseling/silking) for maximum economic benefit",
            "Effective fungicides: azoxystrobin, propiconazole, pyraclostrobin+metconazole",
            "Application before tasseling is typically not cost-effective in field corn situations",
            "Plant resistant hybrids — most economical long-term solution available",
            "Rotate crops with non-grass crops (soybeans, legumes) to reduce residue inoculum levels",
            "Tillage to bury residue reduces primary inoculum for following season significantly"
        ],
        "prevention": (
            "Plant resistant or tolerant hybrids — consult agronomist for local recommendations. "
            "Rotate corn with soybeans or other non-grass crops on a 1–2 year cycle. "
            "Consider tillage to bury infected residue in high-risk fields. "
            "Scout fields from V5 stage, monitoring lower leaves consistently. "
            "Early planting reduces exposure during critical silking period in some regions."
        ),
        "farmer_tip": "📅 Timing is CRITICAL for fungicide applications. Applying at VT (tassel emergence) through R1 (silk) gives maximum yield protection. Applications before VT or after R2 typically don't provide economic returns.",
    },

    "Corn_(maize)___healthy": {
        "display_name": "Healthy Corn",
        "type": "Healthy",
        "severity": "None",
        "emoji": "✅",
        "description": (
            "Your corn plant looks completely healthy! No disease or pest damage is visible. "
            "The leaves show good uniform green color without lesions, spots, or abnormal discoloration. "
            "Continue scouting regularly and maintain good agronomic practices through the rest of the season."
        ),
        "symptoms": [],
        "treatment": [
            "Continue current fertilization and irrigation program",
            "Scout fields weekly from V5 through grain fill stage",
            "Monitor for both disease and insect pests (corn borer, rootworm, aphids)",
            "Apply side-dress nitrogen if plant color indicates possible deficiency"
        ],
        "prevention": (
            "Scout fields every 5–7 days from V5 stage through R4 (dough) stage. "
            "Pay close attention to lower leaves for early rust or blight development. "
            "Check silk and ear area for insect pests during pollination period. "
            "Ensure adequate potassium and phosphorus for stalk strength and disease resistance."
        ),
        "farmer_tip": "✅ Corn looks great! Keep scouting weekly through tasseling — that critical period sees the most disease and insect pressure that affects final grain yield.",
    },

    # ──────────────────────────────────────────────────────────
    #  GRAPE DISEASES
    # ──────────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "display_name": "Grape Black Rot",
        "type": "Fungal",
        "severity": "High",
        "emoji": "🍇",
        "description": (
            "Grape Black Rot, caused by Guignardia bidwellii, is the most destructive fungal disease of "
            "grapes in warm, humid regions and can destroy 80–100% of the fruit crop in a severe year. "
            "The fungus overwinters in infected mummified berries and cane lesions. In spring, it "
            "releases spores during rain events that infect new growth. All green parts of the vine "
            "are susceptible — leaves, shoots, tendrils, and especially developing berries. "
            "Once a berry is infected, there is no treatment — it will inevitably mummify into a "
            "black, shriveled, spore-filled mass that infects the next season's crop."
        ),
        "symptoms": [
            "Tan to brown circular leaf spots with dark brown to black borders (2–10mm diameter)",
            "Small black flask-shaped fruiting bodies (pycnidia) visible as black dots in tan centers",
            "Young infected berries turn brown, shrivel, and mummify into hard black raisin-like masses",
            "Mummified berries cling stubbornly to clusters long after healthy berries would drop",
            "Dark brown lesions on green shoots — elongated, sunken into the tissue",
            "Tendrils develop dark lesions and die back completely",
            "Infected flower clusters dry up and fail to set fruit entirely"
        ],
        "treatment": [
            "Apply fungicides from bud break through 4–5 weeks after bloom — this is the critical protection window",
            "Effective fungicides: myclobutanil (Rally), mancozeb, captan, azoxystrobin",
            "Spray every 7–10 days — more frequently during wet weather periods",
            "Remove ALL mummified berries from vines and ground before bud break each spring",
            "Prune out and destroy infected canes showing lesions during dormant pruning",
            "Improve canopy airflow through leaf removal and proper shoot positioning",
            "Apply protective sprays BEFORE rain events during susceptible growth period"
        ],
        "prevention": (
            "Thorough sanitation before bud break is the single most important control step. "
            "Remove every mummified berry from vines and ground — each contains millions of spores. "
            "Apply dormant-season lime sulfur spray to reduce overwintering inoculum levels. "
            "Train vines to open canopy system for airflow and spray penetration. "
            "Plant resistant varieties in high-disease-pressure regions."
        ),
        "farmer_tip": "🍇 Spend time in winter removing every mummified berry you can find — tedious but removes your primary infection source for next season. One hour of sanitation saves 10 hours of spraying later.",
    },

    "Grape___healthy": {
        "display_name": "Healthy Grape",
        "type": "Healthy",
        "severity": "None",
        "emoji": "✅",
        "description": (
            "Your grapevine appears completely healthy! Leaves are a good green color with no spots, "
            "lesions, or abnormal symptoms visible anywhere. Clusters (if present) look clean and well-formed. "
            "Continue your current vineyard management practices to maintain this excellent plant health."
        ),
        "symptoms": [],
        "treatment": [
            "Continue regular canopy management — shoot positioning and leaf removal for optimal airflow",
            "Maintain fertilization and irrigation schedule appropriate to current growth stage",
            "Scout weekly through entire growing season for early disease symptoms",
            "Apply preventive fungicide program from bud break as standard annual practice"
        ],
        "prevention": (
            "Prune annually to maintain open canopy for good airflow and spray penetration. "
            "Remove all crop residue (mummies, infected canes) during dormant pruning. "
            "Apply a standard preventive spray program from bud break through veraison. "
            "Monitor weather — apply extra sprays before and after rain events during bloom and berry development."
        ),
        "farmer_tip": "✅ Vines look great! Good canopy management — keeping shoots positioned and removing excess leaves — is the foundation of all disease prevention in grapes.",
    },

    # ──────────────────────────────────────────────────────────
    #  DEFAULT FALLBACK
    # ──────────────────────────────────────────────────────────
    "default": {
        "display_name": "Unknown Disease",
        "type": "Unknown",
        "severity": "Unknown",
        "emoji": "🔍",
        "description": (
            "This plant condition was not found in our database, or the model predicted a class "
            "that doesn't match our current disease records. This could be a disease variant, "
            "a nutrient deficiency, environmental stress, or a condition outside our current "
            "38-class dataset. Please consult a qualified agronomist or plant pathologist "
            "for a professional diagnosis with a physical inspection."
        ),
        "symptoms": [
            "Refer to the predicted class name above for identification clues",
            "Consult a local agricultural extension officer for in-person visual diagnosis",
            "Take multiple clear photos (top and bottom of leaves, stem, fruit) for expert review"
        ],
        "treatment": [
            "Consult with a local agronomist or plant pathologist immediately",
            "Do not apply any chemical treatment without a confirmed diagnosis",
            "Isolate affected plants from healthy ones as a precautionary measure",
            "Contact your nearest agricultural university or extension service for help"
        ],
        "prevention": (
            "Regular monitoring and good agricultural practices prevent most plant diseases. "
            "Maintain proper plant nutrition, irrigation, and airflow at all times. "
            "Scout crops weekly and document any unusual symptoms with photos for records."
        ),
        "farmer_tip": "📞 When in doubt, contact your local agricultural extension office — they offer free or low-cost plant disease diagnosis services and expert advice that can save your crop.",
    }
}


# =============================================================
#   MODEL LOADER (Singleton pattern — loads once, reuses)
# =============================================================
_model  = None
_labels = None

def load_model_and_labels():
    global _model, _labels
    if _model is None:
        try:
            import tensorflow as tf
            print("🔄 Loading model...")
            _model = tf.keras.models.load_model(MODEL_PATH)
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"⚠️ Model not loaded: {e}")
            _model = None

    if _labels is None:
        try:
            with open(LABELS_PATH, 'r') as f:
                raw = json.load(f)
            _labels = {int(k): v for k, v in raw.items()}
            print(f"✅ Labels loaded: {len(_labels)} classes")
        except Exception as e:
            print(f"⚠️ Labels not loaded: {e}")
            _labels = None

    return _model, _labels


# =============================================================
#   IMAGE PREPROCESSING
# =============================================================
def preprocess_image(image_bytes):
    """Resize, normalize, and batch-expand image for model input."""
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert('RGB')                         # Ensure 3 channels
    img = img.resize((IMG_SIZE, IMG_SIZE))            # Resize to model input
    img_array = np.array(img, dtype=np.float32) / 255.0  # Normalize [0,1]
    img_array = np.expand_dims(img_array, axis=0)    # Add batch dimension
    return img_array


# =============================================================
#   FUZZY DISEASE LOOKUP — never falls back to Unknown for known diseases
# =============================================================
def get_disease_info(class_name):
    """Smart lookup — tries 4 matching strategies before giving up."""

    # 1. Exact match
    if class_name in DISEASE_INFO:
        return DISEASE_INFO[class_name]

    # 2. Normalized exact match
    def normalize(s):
        return s.lower().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")

    cn = normalize(class_name)
    for key in DISEASE_INFO:
        if normalize(key) == cn:
            return DISEASE_INFO[key]

    # 3. Partial containment match
    for key in DISEASE_INFO:
        if normalize(key) in cn or cn in normalize(key):
            return DISEASE_INFO[key]

    # 4. Word overlap score (best match with ≥2 shared words)
    def words(s):
        return set(normalize(s).replace("_", " ").split())

    cn_words = words(class_name)
    best_key, best_score = None, 0
    for key in DISEASE_INFO:
        if key == "default":
            continue
        overlap = len(cn_words & words(key))
        if overlap > best_score:
            best_score, best_key = overlap, key

    if best_score >= 2 and best_key:
        return DISEASE_INFO[best_key]

    # 5. Final fallback with readable name
    info = DISEASE_INFO["default"].copy()
    info["display_name"] = class_name.replace("___", " — ").replace("_", " ").title()
    return info


# =============================================================
#   MAIN PREDICTION FUNCTION
# =============================================================
def predict(image_bytes):
    model, labels = load_model_and_labels()

    if model is None or labels is None:
        return _demo_prediction()

    img_array   = preprocess_image(image_bytes)
    predictions = model.predict(img_array)[0]

    top_idx    = int(np.argmax(predictions))
    confidence = float(predictions[top_idx])
    class_name = labels.get(top_idx, "Unknown")

    top3_indices = np.argsort(predictions)[::-1][:3]
    top3 = []
    for idx in top3_indices:
        cn   = labels.get(int(idx), "Unknown")
        info = get_disease_info(cn)
        top3.append({
            "class": cn,
            "name": info["display_name"],
            "confidence": float(predictions[idx]),
            "confidence_pct": f"{float(predictions[idx])*100:.1f}%"
        })

    disease_info = get_disease_info(class_name)

    return {
        "class_name": class_name,
        "display_name": disease_info["display_name"],
        "confidence": confidence,
        "confidence_pct": f"{confidence*100:.1f}%",
        "is_healthy": disease_info["type"] == "Healthy",
        "disease_info": disease_info,
        "top3": top3,
        "model_loaded": True
    }


def _demo_prediction():
    """Realistic demo when no model file is present."""
    import random
    demo_classes = [
        "Tomato___Early_blight", "Tomato___Late_blight",
        "Potato___Late_blight",  "Apple___Apple_scab",
        "Tomato___healthy",      "Corn_(maize)___Common_rust_"
    ]
    class_name   = random.choice(demo_classes)
    confidence   = random.uniform(0.72, 0.97)
    disease_info = get_disease_info(class_name)

    others = [c for c in demo_classes if c != class_name][:2]
    confs  = sorted([random.uniform(0.01, 0.15) for _ in range(2)], reverse=True)
    top3   = [{
        "class": class_name, "name": disease_info["display_name"],
        "confidence": confidence, "confidence_pct": f"{confidence*100:.1f}%"
    }]
    for cn, cf in zip(others, confs):
        info = get_disease_info(cn)
        top3.append({"class": cn, "name": info["display_name"],
                     "confidence": cf, "confidence_pct": f"{cf*100:.1f}%"})

    return {
        "class_name": class_name,
        "display_name": disease_info["display_name"],
        "confidence": confidence,
        "confidence_pct": f"{confidence*100:.1f}%",
        "is_healthy": disease_info["type"] == "Healthy",
        "disease_info": disease_info,
        "top3": top3,
        "model_loaded": False,
        "demo_mode": True
    }
