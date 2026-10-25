from flask import Flask
app = Flask(__name__)

tokens = {
    "dr-anil": [],
    "dr-meera": [],
    "dr-suresh": []
}

@app.route("/")
def home():
    return "Hospital Token System"

@app.route("/token/<doctor>/new")
def new_token(doctor):
    if doctor not in tokens:
        return {"error": "Doctor not found"}, 404
    number = len(tokens[doctor]) + 1
    tokens[doctor].append(number)
    return {"doctor": doctor, "token": number}

@app.route("/token/<doctor>/list")
def list_tokens(doctor):
    if doctor not in tokens:
        return {"error": "Doctor not found"}, 404
    return {"doctor": doctor, "tokens": tokens[doctor]}

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)