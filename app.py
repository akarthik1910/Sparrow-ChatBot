from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
app = Flask(__name__)

# Load chatbot responses from JSON file
#with open("chat_bot_responses.json", "r") as file:
    #chatbot_responses = json.load(file)
# Load responses from Excel
df = pd.read_excel("chatbot_responses.xlsx")
chatbot_responses = dict(zip(df["User_Input"].str.lower(), df["Bot_Response"]))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    # Get response from JSON, fallback to "default" if not found
    response = chatbot_responses.get(user_message, chatbot_responses["default"])
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
