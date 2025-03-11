from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load chatbot responses from Excel
def load_responses(file_path='chatbot_responses.xlsx'):
    df = pd.read_excel(file_path)
    data = dict(zip(df['Question'].str.strip().str.lower(), df['Response']))
    return data

# Load responses from Excel
chatbot_responses = load_responses()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower().strip()
    response = chatbot_responses.get(user_message, chatbot_responses.get("default", "Sorry, I didn't understand that."))
    return jsonify({"response": response})

# Suggestion endpoint — exact matches, up to 10 suggestions
@app.route("/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify([])

    # Get up to 10 suggestions where questions start with the query
    suggestions = [q for q in chatbot_responses.keys() if q.find(query)!=-1]
    return jsonify(suggestions[:10])

if __name__ == "__main__":
    app.run(debug=True)
