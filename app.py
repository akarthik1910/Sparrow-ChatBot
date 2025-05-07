from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
EXCEL_FILE = os.path.join(app.config['UPLOAD_FOLDER'], 'chatbot_responses.xlsx')

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load responses from Excel
def load_responses(file_path=EXCEL_FILE):
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return dict(zip(df['Question'].str.strip().str.lower(), df['Response']))
    else:
        return {}

chatbot_responses = load_responses()

# Save or update a question-response pair
def save_or_update_response(question, response):
    question = question.strip()
    response = response.strip()

    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame(columns=["Question", "Response"])

    lower_questions = df["Question"].str.strip().str.lower()
    if question.lower() in lower_questions.values:
        idx = lower_questions[lower_questions == question.lower()].index[0]
        df.at[idx, "Response"] = response
    else:
        df = df.append({"Question": question, "Response": response}, ignore_index=True)

    df.to_excel(EXCEL_FILE, index=False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower().strip()
    response = chatbot_responses.get(user_message, chatbot_responses.get("default", "Sorry, I didn't understand that."))
    return jsonify({"response": response})

@app.route("/suggest", methods=["GET"])
def suggest():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify([])

    suggestions = [q for q in chatbot_responses.keys() if q.find(query) != -1]
    return jsonify(suggestions[:10])

@app.route("/update", methods=["GET", "POST"])
def update_response():
    global chatbot_responses
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        response = request.form.get("response", "").strip()

        if not question or not response:
            return "Both fields are required", 400

        save_or_update_response(question, response)
        chatbot_responses = load_responses()  # Reload updated data
        return redirect(url_for("home"))

    return '''
    <!doctype html>
    <title>Update Chatbot Response</title>
    <h1>Enter or Update a Question and Response</h1>
    <form method="post">
      <label>Question:</label><br>
      <input type="text" name="question" required><br><br>
      <label>Response:</label><br>
      <textarea name="response" rows="4" cols="50" required></textarea><br><br>
      <input type="submit" value="Submit">
    </form>
    <br>
    <a href="/">Back to Chat</a>
    '''

if __name__ == "__main__":
    app.run(debug=True)
