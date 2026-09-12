"""LeafScan AI v4 — SQLite Database Module"""
import sqlite3, os, json
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leafscan.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scan_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL,
        filename TEXT, disease_name TEXT NOT NULL, class_name TEXT,
        disease_type TEXT, severity TEXT, confidence REAL, is_healthy INTEGER DEFAULT 0,
        emoji TEXT, plant TEXT, symptoms TEXT, treatment TEXT, prevention TEXT,
        farmer_tip TEXT, description TEXT, top3 TEXT, demo_mode INTEGER DEFAULT 0,
        language TEXT DEFAULT 'en', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL,
        role TEXT NOT NULL, message TEXT NOT NULL, language TEXT DEFAULT 'en',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT UNIQUE NOT NULL,
        language TEXT DEFAULT 'en', name TEXT, total_scans INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()
    print("DB initialized:", DB_PATH)

def save_scan(session_id, result, filename='', language='en'):
    info = result.get('disease_info', {})
    conn = get_connection()
    conn.execute('''INSERT INTO scan_history
        (session_id,filename,disease_name,class_name,disease_type,severity,confidence,
         is_healthy,emoji,plant,symptoms,treatment,prevention,farmer_tip,description,top3,demo_mode,language)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (session_id, filename, result.get('display_name',''), result.get('class_name',''),
         info.get('type',''), info.get('severity',''), result.get('confidence',0),
         1 if result.get('is_healthy') else 0, info.get('emoji','🌿'),
         result.get('class_name','').split('___')[0].replace('_',' ') if '___' in result.get('class_name','') else 'Various',
         json.dumps(info.get('symptoms',[])), json.dumps(info.get('treatment',[])),
         info.get('prevention',''), info.get('farmer_tip',''), info.get('description',''),
         json.dumps(result.get('top3',[])), 1 if result.get('demo_mode') else 0, language))
    conn.execute('INSERT OR IGNORE INTO users (session_id,language) VALUES(?,?)', (session_id, language))
    conn.execute('UPDATE users SET total_scans=total_scans+1 WHERE session_id=?', (session_id,))
    conn.commit()
    scan_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return scan_id

def get_scan_history(session_id, limit=50):
    conn = get_connection()
    rows = conn.execute('SELECT * FROM scan_history WHERE session_id=? ORDER BY created_at DESC LIMIT ?', (session_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_scan_by_id(scan_id):
    conn = get_connection()
    row = conn.execute('SELECT * FROM scan_history WHERE id=?', (scan_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_stats(session_id):
    conn = get_connection()
    r = conn.execute('''SELECT COUNT(*) as total,
        SUM(CASE WHEN is_healthy=1 THEN 1 ELSE 0 END) as healthy,
        SUM(CASE WHEN is_healthy=0 THEN 1 ELSE 0 END) as diseased,
        AVG(confidence) as avg_confidence
        FROM scan_history WHERE session_id=?''', (session_id,)).fetchone()
    conn.close()
    return dict(r) if r else {}

def save_message(session_id, role, message, language='en'):
    conn = get_connection()
    conn.execute('INSERT INTO chat_messages (session_id,role,message,language) VALUES(?,?,?,?)',
                 (session_id, role, message, language))
    conn.commit()
    conn.close()

def get_chat_history(session_id, limit=30):
    conn = get_connection()
    rows = conn.execute('SELECT role,message,created_at FROM chat_messages WHERE session_id=? ORDER BY created_at ASC LIMIT ?', (session_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def clear_chat(session_id):
    conn = get_connection()
    conn.execute('DELETE FROM chat_messages WHERE session_id=?', (session_id,))
    conn.commit()
    conn.close()

def get_or_create_user(session_id, language='en'):
    conn = get_connection()
    conn.execute('INSERT OR IGNORE INTO users (session_id,language) VALUES(?,?)', (session_id, language))
    conn.commit()
    user = conn.execute('SELECT * FROM users WHERE session_id=?', (session_id,)).fetchone()
    conn.close()
    return dict(user)

def update_user_language(session_id, language):
    conn = get_connection()
    conn.execute('UPDATE users SET language=? WHERE session_id=?', (language, session_id))
    conn.commit()
    conn.close()