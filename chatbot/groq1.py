import requests
import json
import os
from groq import Groq
import time
from screen_capture import capture_screen, get_active_window_title
from extracting import OCRProcessor
from dotenv import load_dotenv

load_dotenv()
client=Groq(api_key = os.getenv("GROQ_API_KEY"))
ocr_processor = OCRProcessor()
def generate_suggestion(role, goal, text,window):
    completion = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {
                 "role": "system",
                 "content": f"You are ScreenCompanion, a friendly desktop productivity AI assistant. Based on the user’s screen content (text extracted using OCR), and their current role and goal, your job is to give clear, focused suggestions that improve their productivity. Your role is to help users stay focused and aligned with their goal.\n\nYou are provided:\n- The user's role (e.g., student, developer).\n- The user's goal (e.g., finish a math assignment).\n- OCR-extracted text from the current screen.\n- The title or name of the currently active window.\n\nYour tasks:\n- Give short, actionable suggestions to improve productivity.\n- Gently alert if the user seems distracted or off-task.\n- Suggest system or behavior changes to align better with their goal.\n- Recommend helpful system-level actions such as \"close distracting window,\" \"open notes app,\" \"switch to VS Code\" etc., if screen content shows misalignment with the goal. Make these suggestions **explicit and actionable** so they can be automated using ScreenPipe Terminator.\n- Encourage breaks if the screen shows signs of fatigue, boredom, or prolonged inactivity.\n- NEVER assume anything beyond what is in the OCR or window title.\n\nSpeak like a helpful accountability buddy: Keep responses concise, actionable, motivating, positive, and supportive. Avoid long text. Never use technical jargon unless the user is a developer or engineer.\n\nTone: Friendly, concise, and motivating. Prioritize goal alignment and smart habits. Do not hallucinate or make up apps or tasks not present in the screen data.\n"
            },
            {
                "role": "user",
                "content": f"USER ROLE: {role}\nUSER GOAL: {goal}\nSCREEN CONTENT (OCR): {text} \nCURRENT ACTIVE WINDOW: {window}\n\nBased on the above ,Give helpful, short suggestions and note if I'm distracted. Be friendly and clear.Based on the screen activity above these instructions as to what to do :\n1.tell me if I’m on track with my goal.\n2.If I seem off-task or distracted, gently alert me and suggest what I can change to stay on track.\n3.Suggest short, actionable ways I can improve my productivity right now.\n4.If possible, recommend system-level actions (e.g., close a distracting app, open something relevant to the goal) that can be passed to an automation tool.\n5.Encourage breaks only if it makes sense from the context.\n6.Keep your tone like a kind productivity buddy—short, friendly, helpful.\n7.Do NOT guess what I might be doing if it isn’t present in the screen data but if screen data is absent you need to check with me if it on track with my goal to make sure I'm not wasting time.\n8.DO NOT fabricate tasks, websites, or applications that are not shown in the text or window name.\n\nGive your response in this format:\n    Productivity Suggestion:\n    Suggested Action (if applicable):\n\n"
            },
            {
                "role": "assistant",
                "content": "Okay, I'm ready to be your productivity buddy!  Just tell me your role, goal, and what's on your screen, and I'll do my best to help you stay focused and make progress.  \n"
            }
             ],
             temperature=1,
             max_completion_tokens=1024,
             top_p=1,
             stream=True,
             stop=None,
         )
    response=""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response.strip()




# text1="Inbox (3) - user@gmail.com\nSubject: Team Meeting Tomorrow at 10am\nHi everyone, just a reminder about our meeting tomorrow at 10am"
# try:
#     ans = generate_suggestion(
#         "student",
#         "studying for my operating system program",
#         f"text: {text1}",
#         "Window Title: extracting.py - Screenassisstant - Visual Studio Code " 
#     )
#     print(ans)
# except Exception as e:
#     print(f"An error occurred: {e}")

