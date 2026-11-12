from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/send_otp", methods=["POST"])
def send_otp():
    data = request.json
    email = data.get("email")
    otp_type = data.get("type") # ingame ya unsubscribe

    if not email:
        return jsonify({"success": False, "message": "Email required"}), 400

    # ========================================================
    # GARENA KI ASLI API KO CALL KAR RAHE HAIN
    # ========================================================
    try:
        # Garena ka OTP endpoint (Session Security)
        garena_url = "https://100067.connect.garena.com/game/account_security/bind:send_otp"
        
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; A063 Build/TKQ1.221220.001)",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "email": email,
            "otp_type": "1" if otp_type == "ingame" else "2"
        }

        # Request bhej rahe hain
        response = requests.post(garena_url, json=payload, headers=headers, timeout=10)

        if response.status_code == 200:
            return jsonify({"success": True, "message": f"Garena OTP sent to {email}!"})
        else:
            return jsonify({"success": False, "message": f"Garena Error: {response.status_code}"}), response.status_code

    except Exception as e:
        return jsonify({"success": False, "message": f"Network Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)