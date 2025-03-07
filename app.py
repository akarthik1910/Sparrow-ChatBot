from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
app = Flask(__name__)

# Load chatbot responses from JSON file
#with open("chat_bot_responses.json", "r") as file:
    #chatbot_responses = json.load(file)
# Load responses from Excel
#df = pd.read_excel("chatbot_responses.xlsx")
#chatbot_responses = dict(zip(df["User_Input"].str.lower(), df["Bot_Response"]))

def load_responses(file_path='chatbot_responses.xlsx'):
    df = pd.read_excel(file_path,dtype={'Question':str,'Response':str})
    df["Question"]=df["Question"].apply(lambda x:str(x).strip().replace(" ",""))
    return dict(zip(df['Question'].str.lower(), df['Response']))

chatbot_responses=load_responses()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower().strip()
    user_message=user_message.replace(" ","")
    # Get response from JSON, fallback to "default" if not found
    response = chatbot_responses.get(user_message, chatbot_responses["default"])
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
