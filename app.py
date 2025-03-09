from flask import Flask, render_template, request, jsonify
import pandas as pd
import openpyxl
from fuzzywuzzy import process

app = Flask(__name__)

# Function to read Excel and retain bold text formatting
def read_excel_with_format(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=False):  # Assuming headers in row 1
        question_cell = row[0]  # First column: Question
        response_cell = row[1]  # Second column: Response
        

        # Format questions (strip spaces, lowercase)
        question = str(question_cell.value).strip().replace(" ", "").lower()

        # Retain bold formatting in response
        is_bold = response_cell.font and response_cell.font.bold
        response = response_cell.value
        formatted_response = f"<b>{response}</b>" if is_bold else response

        #print(f"Question: {question}, Response: {formatted_response}")  # Debug print

        data.append((question, formatted_response))

    return data

# Load chatbot responses from Excel, calling read_excel_with_format()
def load_responses(file_path='chatbot_responses.xlsx'):
    data = read_excel_with_format(file_path)
    return dict(data)

# Remove articles like 'a', 'an', 'the' from user input
def remove_articles(sentence):
    articles = {"a", "an", "the"}
    words = sentence.split()
    filtered_words = [word for word in words if word.lower() not in articles]
    return ' '.join(filtered_words)

def get_best_match(user_message, responses_dict, threshold=80):
    best_match, score = process.extractOne(user_message, responses_dict.keys())
    if score >= threshold:
        return responses_dict[best_match]
    return responses_dict.get("default", "Sorry, I didn't understand that.")

# Load responses from Excel
chatbot_responses = load_responses()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower().strip()
    user_message = remove_articles(user_message)
    user_message = user_message.replace(" ", "")

    # Get response from Excel, fallback to "default" if not found
    #response = chatbot_responses.get(user_message, chatbot_responses.get("default", "Sorry, I didn't understand that."))
    response = get_best_match(user_message, chatbot_responses)
    #print(response)  # Debug print to confirm bold tags
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
