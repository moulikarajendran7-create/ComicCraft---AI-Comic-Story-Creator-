import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import google.generativeai as genai

app = FastAPI()

# Configure Gemini AI Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>🎨 ComicCraft - AI Comic Generator</h2>
    <form action="/generate" method="post">
        <input type="text" name="topic" placeholder="Enter comic idea..." required style="width: 300px; padding: 8px;"><br><br>
        <button type="submit" style="padding: 8px 15px;">Generate Script</button>
    </form>
    """

@app.post("/generate", response_class=HTMLResponse)
def generate(topic: str = Form(...)):
    prompt = f"Create a 4-panel comic script for: {topic}. Include panel visual descriptions and dialogue."
    response = model.generate_content(prompt)
    script = response.text.replace("\n", "<br>")
    return f"<h3>Generated Script:</h3><div>{script}</div><br><a href='/'>← Back</a>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
