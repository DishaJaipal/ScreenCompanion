import requests
import json
import os
from main import client
import groq
import time
from Screendata.screen_capture import capture_screen
from Screendata.extracting import process_screenshot
# from main import user_role, user_goal  

# CAPTURE_INTERVAL = 300  

# def run_screen_assistant():
#     """Periodically capture and process screenshots, and integrate with Groq."""
#     previous_gray = None  # Store the previous grayscale screenshot for SSIM comparison

#     while True:
#         try:
#             # Step 1: Capture the current screen
#             screenshot = capture_screen()

#             # Step 2: Process the screenshot and extract meaningful text
#             result, previous_gray = process_screenshot(screenshot, previous_gray)

#             if result:
#                 # Extracted data
#                 extracted_text = result["text"]
#                 window_title = result["window_title"]

#                 # Step 3: Prepare a prompt for Groq API
#                 prompt = (
#                     f"The user is currently working in the window: {window_title}. "
#                     f"The user's role is 'student' and their goal is 'working on a productiviy app using python'. "
#                     f"Based on the content:\n\n{extracted_text}\n\n"
#                     "Provide productivity-enhancing suggestions and alert them if they deviate."
#                 )

#                 # Step 4: Send the prompt to Groq API
#                 completion = client.chat.completions.create(
#                     messages=[
#                         {"role": "system", "content": "You are a productivity assistant helping users achieve their goals."},
#                         {"role": "user", "content": prompt}
#                     ],
#                     model="deepseek-r1-distill-llama-70b",
#                     temperature=0.5,
#                     max_completion_tokens=50,
#                     top_p=1,
#                     stop=None,
#                     reasoning_format="raw"
#                 )
#                 for chunk in completion:
#                     print(chunk.choices[0].delta.content or "", end="")

#                 # # Step 5: Display and handle Groq response
#                 # response = chat_completion.choices[0].message.content
#                 # print(f"Groq Response:\n{response}")

#                 speech_file_path = "speech.wav" 
#                 model = "playai-tts"
#                 voice = "Fritz-PlayAI"
#                 text = completion.choices[0].message.content
#                 response_format = "wav"
#                 response_v = client.audio.speech.create(
#                     model=model,
#                     voice=voice,
#                     input=text,
#                     response_format=response_format)
#                 response_v.write_to_file(speech_file_path)
#             # Wait for the next interval
#             print("Full API Response:", response)
#             time.sleep(CAPTURE_INTERVAL)

#         except KeyboardInterrupt:
#             print("\nScreenCompanion stopped.")
#             break
#         except Exception as e:
#             print(f"An error occurred: {e}")

screen=capture_screen
user_role = "student"
user_goal = "working on a productivity app using python"
window=screen('window_title')
extracted_text = process_screenshot(screen, window)
completion = client.chat.completions.create(
    model="gemma2-9b-it",
    messages=[
        {
            "role": "system",
            "content": "You are ScreenCompanion, a friendly desktop productivity AI assistant. Based on the user’s screen content (text extracted using OCR), and their current role and goal, your job is to give clear, focused suggestions that improve their productivity. Your role is to help users stay focused and aligned with their goal.\n\nYou are provided:\n- The user's role (e.g., student, developer).\n- The user's goal (e.g., finish a math assignment).\n- OCR-extracted text from the current screen.\n- The title or name of the currently active window.\n\nYour tasks:\n- Give short, actionable suggestions to improve productivity.\n- Gently alert if the user seems distracted or off-task.\n- Suggest system or behavior changes to align better with their goal.\n- Recommend helpful system-level actions such as \"close distracting window,\" \"open notes app,\" \"switch to VS Code\" etc., if screen content shows misalignment with the goal. Make these suggestions **explicit and actionable** so they can be automated using ScreenPipe Terminator.\n- Encourage breaks if the screen shows signs of fatigue, boredom, or prolonged inactivity.\n- NEVER assume anything beyond what is in the OCR or window title.\n\nSpeak like a helpful accountability buddy: Keep responses concise, actionable, motivating, positive, and supportive. Avoid long text. Never use technical jargon unless the user is a developer or engineer.\n\nTone: Friendly, concise, and motivating. Prioritize goal alignment and smart habits. Do not hallucinate or make up apps or tasks not present in the screen data.\n"
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
