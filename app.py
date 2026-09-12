"""LeafScan AI v4 — Flask App with Chatbot, Database, PDF Reports, Multilingual"""
import os, sys, json, uuid, base64
from pathlib import Path
from flask import (Flask, request, jsonify, render_template,
                   send_from_directory, session, send_file)
from werkzeug.utils import secure_filename

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import (init_db, save_scan, get_scan_history, get_scan_by_id,
                          get_stats, save_message, get_chat_history, clear_chat,
                          get_or_create_user, update_user_language)
from utils.chatbot import get_bot_response, get_greeting, LANGUAGES
from utils.pdf_report import generate_pdf_report

# ── Try to import predictor (optional - demo mode if not available) ────────────
try:
    from utils.predictor import predict, load_model_and_labels, get_disease_info, DISEASE_INFO
    HAS_PREDICTOR = True
except ImportError:
    HAS_PREDICTOR = False
    def predict(img_bytes): return _demo_result()
    def load_model_and_labels(): return None, None
    DISEASE_INFO = {}
    def get_disease_info(cn): return {"display_name":cn,"type":"Unknown","severity":"Unknown","emoji":"🔍","description":"","symptoms":[],"treatment":[],"prevention":"","farmer_tip":""}

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'leafscan-secret-2024-agri')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED = {'png','jpg','jpeg','gif','bmp','webp'}

init_db()

def allowed_file(f): return '.' in f and f.rsplit('.',1)[1].lower() in ALLOWED

def get_session_id():
    if 'sid' not in session:
        session['sid'] = str(uuid.uuid4())
    return session['sid']

# ── PAGES ──────────────────────────────────────────────────────
@app.route('/')
def index():
    sid = get_session_id()
    get_or_create_user(sid)
    return render_template('index.html')

# ── PREDICT ────────────────────────────────────────────────────
@app.route('/api/predict', methods=['POST'])
def predict_disease():
    sid = get_session_id()
    lang = request.form.get('language', session.get('lang','en'))
    try:
        image_bytes = None
        filename = ''
        if 'image' in request.files:
            f = request.files['image']
            if not allowed_file(f.filename):
                return jsonify({"success":False,"error":"Invalid file type"}), 400
            image_bytes = f.read()
            filename = secure_filename(f.filename)
        elif request.is_json and 'image_base64' in request.json:
            b64 = request.json['image_base64']
            if ',' in b64: b64 = b64.split(',')[1]
            image_bytes = base64.b64decode(b64)
        else:
            return jsonify({"success":False,"error":"No image provided"}), 400

        result = predict(image_bytes)
        scan_id = save_scan(sid, result, filename, lang)
        result['scan_id'] = scan_id
        return jsonify({"success":True,"result":result})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}), 500

# ── PDF REPORT ─────────────────────────────────────────────────
@app.route('/api/report/pdf/<int:scan_id>', methods=['GET'])
def download_pdf(scan_id):
    """Generate and download PDF report for a scan."""
    lang = request.args.get('lang', 'en')
    scan = get_scan_by_id(scan_id)
    if not scan:
        # If no DB record, generate demo PDF
        scan = None
    try:
        if scan:
            # Reconstruct result dict from DB row
            result = {
                'display_name': scan['disease_name'],
                'class_name':   scan['class_name'],
                'confidence':   scan['confidence'],
                'confidence_pct': f"{round(scan['confidence']*100,1)}%",
                'is_healthy':   bool(scan['is_healthy']),
                'top3': json.loads(scan['top3']) if scan['top3'] else [],
                'demo_mode': bool(scan['demo_mode']),
                'disease_info': {
                    'type':        scan['disease_type'],
                    'severity':    scan['severity'],
                    'emoji':       scan['emoji'],
                    'description': scan['description'],
                    'symptoms':    json.loads(scan['symptoms']) if scan['symptoms'] else [],
                    'treatment':   json.loads(scan['treatment']) if scan['treatment'] else [],
                    'prevention':  scan['prevention'],
                    'farmer_tip':  scan['farmer_tip'],
                }
            }
        else:
            result = _demo_result()

        pdf_buf = generate_pdf_report(result, scan_id=scan_id, language=lang)
        fname = f"leafscan-report-{scan_id}.pdf"
        return send_file(pdf_buf, mimetype='application/pdf',
                         as_attachment=True, download_name=fname)
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}), 500

@app.route('/api/report/pdf/latest', methods=['GET'])
def download_latest_pdf():
    """Download PDF for most recent scan in session."""
    sid = get_session_id()
    lang = request.args.get('lang','en')
    history = get_scan_history(sid, limit=1)
    if history:
        return download_pdf(history[0]['id'])
    return jsonify({"success":False,"error":"No scans found"}), 404

# ── CHATBOT ────────────────────────────────────────────────────
@app.route('/api/chat', methods=['POST'])
def chat():
    sid  = get_session_id()
    data = request.get_json() or {}
    msg  = data.get('message','').strip()
    lang = data.get('language', session.get('lang','en'))
    if not msg:
        return jsonify({"success":False,"error":"Empty message"}), 400
    save_message(sid, 'user', msg, lang)
    bot_reply = get_bot_response(msg, lang)
    save_message(sid, 'assistant', bot_reply, lang)
    return jsonify({"success":True,"reply":bot_reply,"language":lang})

@app.route('/api/chat/history', methods=['GET'])
def chat_history():
    sid = get_session_id()
    return jsonify({"success":True,"history":get_chat_history(sid)})

@app.route('/api/chat/clear', methods=['POST'])
def chat_clear():
    sid = get_session_id()
    clear_chat(sid)
    return jsonify({"success":True})

@app.route('/api/chat/greeting', methods=['GET'])
def chat_greeting():
    lang = request.args.get('lang','en')
    return jsonify({"success":True,"greeting":get_greeting(lang),"language":lang})

# ── LANGUAGE ───────────────────────────────────────────────────
@app.route('/api/language', methods=['POST'])
def set_language():
    sid  = get_session_id()
    lang = request.get_json().get('language','en')
    session['lang'] = lang
    update_user_language(sid, lang)
    return jsonify({"success":True,"language":lang,
                    "greeting":get_greeting(lang),
                    "language_info":LANGUAGES.get(lang,{})})

@app.route('/api/languages', methods=['GET'])
def list_languages():
    return jsonify({"success":True,"languages":LANGUAGES})

# ── HISTORY & STATS ────────────────────────────────────────────
@app.route('/api/history', methods=['GET'])
def scan_history():
    sid = get_session_id()
    return jsonify({"success":True,"history":get_scan_history(sid)})

@app.route('/api/stats', methods=['GET'])
def scan_stats():
    sid = get_session_id()
    return jsonify({"success":True,"stats":get_stats(sid)})

# ── DISEASES ───────────────────────────────────────────────────
@app.route('/api/diseases', methods=['GET'])
def list_diseases():
    diseases = []
    for cn, info in DISEASE_INFO.items():
        if cn != 'default':
            diseases.append({
                "class_name":   cn,
                "display_name": info["display_name"],
                "type":         info["type"],
                "severity":     info["severity"],
                "plant": cn.split('___')[0].replace('_',' ') if '___' in cn else 'Various',
                "emoji":        info.get("emoji","🌿")
            })
    return jsonify({"success":True,"count":len(diseases),"diseases":diseases})

@app.route('/api/disease-detail', methods=['GET'])
def disease_detail():
    cn = request.args.get('class','')
    if not cn: return jsonify({"success":False,"error":"No class name"}), 400
    info = get_disease_info(cn)
    plant = cn.split('___')[0].replace('_',' ') if '___' in cn else 'Various'
    return jsonify({"success":True,"class_name":cn,"plant":plant,**info})

@app.route('/api/health', methods=['GET'])
def health():
    model, labels = load_model_and_labels()
    return jsonify({"status":"ok","model_loaded":model is not None,
                    "labels_loaded":labels is not None,
                    "num_classes":len(labels) if labels else 0,
                    "database":"connected","version":"4.0"})

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def _demo_result():
    import random
    classes = ["Tomato___Early_blight","Tomato___Late_blight","Apple___Apple_scab","Tomato___healthy"]
    cn = random.choice(classes)
    conf = random.uniform(0.72, 0.97)
    info = get_disease_info(cn)
    return {"class_name":cn,"display_name":info["display_name"],"confidence":conf,
            "confidence_pct":f"{conf*100:.1f}%","is_healthy":info["type"]=="Healthy",
            "disease_info":info,"top3":[{"class":cn,"name":info["display_name"],"confidence":conf,"confidence_pct":f"{conf*100:.1f}%"}],
            "model_loaded":False,"demo_mode":True}

if __name__ == '__main__':
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path('static/reports').mkdir(parents=True, exist_ok=True)
    print("="*55)
    print("  🌿 LeafScan AI v4.0 — Full Featured")
    print("="*55)
    print("  🌐 App:      http://localhost:5000")
    print("  🤖 Chatbot:  POST /api/chat")
    print("  📄 PDF:      GET  /api/report/pdf/<scan_id>")
    print("  🌍 Languages: GET /api/languages")
    print("="*55)
    load_model_and_labels()
    app.run(debug=True, host='0.0.0.0', port=5000)