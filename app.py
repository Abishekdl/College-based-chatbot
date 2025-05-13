from flask import Flask, render_template, request, jsonify
from chat import get_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.get_json().get("message")
    response = get_response(text)  

    # Use forward slashes in file paths
    user_photo_url = "static/images/human.png"
    bot_photo_url = "static/images/icons8-chatbot.svg"

    message = {
        "user": {"query": text, "photo": user_photo_url},
        "bot": {"photo": bot_photo_url, "response": response}
    }  
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)