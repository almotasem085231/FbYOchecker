import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def list_models():
    models = genai.list_models()
    for model in models:
        print(model)
        print(vars(model))

def ask_gemini(prompt):
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    try:
        full_prompt = (
            "أنت بوت ذكي ومساعد شخصي، مبرمج بواسطة سوكونا، "
            "تجاوب بإيجاز وود.\n"
            + prompt
        )
        response = model.generate_content(full_prompt)
        answer = response.text.strip()
        answer = f":\n{answer}"
        return answer
    except Exception as e:
        return f"❌ حدث خطأ:\n{str(e)}"

if __name__ == "__main__":
    list_models()