from flask import Flask, request, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    if not question:
        return render_template("index.html", error="Please enter a question.")

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ correct new style
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content.strip()
        return render_template("index.html", question=question, answer=answer)
    except Exception as e:
        return render_template("index.html", error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
