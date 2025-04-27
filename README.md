![github-submission-banner](https://github.com/user-attachments/assets/a1493b84-e4e2-456e-a791-ce35ee2bcf2f)

# 🚀 ScreenCompanion

> Boosting productivity with real-time, context-aware suggestions to keep you focused and efficient.
---

## 📌 Problem Statement
 
****
In today’s world, staying productive is harder than ever with constant distractions, multitasking, and mental fatigue. Traditional tools don't offer the personalized, real-time help people need to stay focused.

We’re building a smart screen productivity assistant that uses OCR to understand what the user is doing and provides real-time suggestions to stay focused. These could include things like music recommendations, focus mode activation, or help with writing emails. The app runs locally, is lightweight, and works silently in the background as a desktop tray app, making it easy to stay on track without distractions.

---

## 🎯 Objective

Our project captures screen content in real-time, extracts meaningful text using OCR (Optical Character Recognition), and streams the data using Fluvio for downstream processing.
It serves teams or individuals who need live screen monitoring, text extraction, or real-time analytics from screen activities — helpful for accessibility, productivity tools, or automating workflows.

We enhance the extracted text using Groq's ultra-fast LLM inference for real-time insights and pattern detection, enabling instant feedback or action suggestions based on screen activity.
---



## 🧠 Team & Approach

### Team Name:  
DONBONDUS

### Team Members:  
- Disha Jaipal (GitHub- https://github.com/DishaJaipal / LinkedIn- www.linkedin.com/in/disha-jaipal-25318a247 / Role- Sysytem SetUP & GROQ AI / Responsibilities- System Setup & Tooling,Groq API Integration,Fluvio Integration (Collaborated) )  
- Prakruti U  (GitHub- https://github.com/PRAKRUTHI77 / LinkedIn- www.linkedin.com/in/prakruthi-u-180463296 /Role- OCR & Streaming /Responsibilities- OCR Integration ,Fluvio Integration (Collaborated))
- Sindhushree N H (GitHub- https://github.com/SindhushreeNH / LinkedIn- www.linkedin.com/in/sindhushree-nh-38a748332 / Role- UI & Automation / Responsibilities- Integrated  for UI control,Built GUI )
- D M Shreya (GitHub- https://github.com/dmshreya / LinkedIn- https://www.linkedin.com/in/shreya-dm-a749432a6 / Role- Docs & git  / Responsibilities- Wrote and structured project documentation,Edited demo video for presentation,Managed GitHub repo setup )


### Our Approach:  
- Why we chose this problem :
  We wanted to build something that actually makes our daily lives better—especially with how easy it is to get distracted or overwhelmed when you're working on a laptop all day. So, we came up with this idea   
 of a smart screen productivity assistant that can understand what the user is doing and give helpful, real-time suggestions to stay on track. We wanted it to feel lightweight, run locally, and still be smart— 
 so no bloated apps. Optional cloud features were a bonus for personalization later.
  
- Key challenges we addressed :
  Screen Understanding Without SDK Access: Since the ScreenPipe SDK wasn’t publicly available, we creatively used Terminator (UI automation) and OCR tools to simulate contextual screen awareness.
  AI Suggestions: We integrated the Groq API to generate accurate, relevant suggestions (like recommending music, activating focus mode, or drafting emails).
  Desktop-Friendly UX: We ensured the assistant works as a tray app, is lightweight, and doesn’t interrupt the user.
  Collaborative Development: We balanced 4 contributors working on different but interconnected parts.

- Any pivots, brainstorms, or breakthroughs during hacking  :
  🧠 Initially, we planned on screen recording + content classification, but pivoted to UI automation + OCR due to SDK access limits.
  🔁 We creatively reused Fluvio for non-standard use cases, like streaming OCR data in real-time.
  🧩 We brainstormed how to structure recommendations using Groq and simple logic from OCR context.
  🎯 Combining screen structure via Terminator + text context via OCR gave us a powerful foundation for screen awareness.
  🛠️ We integrated components like Groq, OCR, and the GUI into a modular system that can be improved later with the actual ScreenPipe SDK or ML models.



---

## 🛠️ Tech Stack

### Core Technologies Used:
Frontend: Python (Tkinter or PyQt for the GUI)
Backend: Python (for OCR and task detection), Groq (for AI-driven suggestions)
Database: Firebase (optional for cloud activity logging)
APIs: Groq API (for task analysis and suggestions)
Hosting: Local environment (desktop application, tray app)

### Sponsor Technologies Used :
✅ Groq: Used to generate accurate, context-aware suggestions such as focus mode activation, music recommendations, or email drafting.

[ ] Monad: Your blockchain implementation

✅ Fluvio: Used for real-time data handling, streaming OCR output to ensure fast task detection and response. Running via Docker for integration.

[ ] Base: AgentKit / OnchainKit / Smart Wallet usage

[ ] Screenpipe: Used Terminator repo for UI automation and task detection, simulating screen awareness.

[ ] Stellar: Payments, identity, or token usage

## ✨ Key Features

Highlight the most important features of your project:
- ✅ Real-time task detection: Using OCR (pytesseract + OpenCV) to capture and analyze screen content instantly.
- ✅ AI-driven suggestions: Powered by the Groq API to provide intelligent recommendations like focus mode activation and background music suggestions.
- ✅ UI automation: Using ScreenPipe’s Terminator for automating UI interactions based on detected tasks.
- ✅ Lightweight desktop assistant: Tray app that runs silently in the background, offering productivity-enhancing features without disrupting the user.

Add images, GIFs, or screenshots if helpful!

---


## 📽️ Demo & Deliverables

- **Demo Video Link:** [Paste YouTube or Loom link here]  
- **Pitch Deck / PPT Link:** [Paste Google Slides / PDF link here]  

---

## ✅ Tasks & Bonus Checklist

- [✅] **All members of the team completed the mandatory task - Followed at least 2 of our social channels and filled the form** (Details in Participant Manual)  
- [✅] **All members of the team completed Bonus Task 1 - Sharing of Badges and filled the form (2 points)**  (Details in Participant Manual)
- [✅] **All members of the team completed Bonus Task 2 - Signing up for Sprint.dev and filled the form (3 points)**  (Details in Participant Manual)

---

## 🧪 How to Run the Project

### Requirements:

- Python 3.10+

- Fluvio CLI installed

- Tesseract OCR

- Groq API Key

- .env file with keys

### Local Setup:
```bash
# Clone the repo
git clone https://github.com/your-team/project-name

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Add your Groq API Key to .env file
echo "GROQ_API_KEY=your_api_key_here" > .env

# Start screen capture and streaming
python main.py

# In a separate terminal, consume data:
fluvio consume screen-data

```

Provide any backend/frontend split or environment setup notes here.

---

## 🧬 Future Scope

List improvements, extensions, or follow-up features:

- 📈 More integrations  
- 🛡️ Security enhancements  
- 🌐 Localization / broader accessibility  

---

## 📎 Resources / Credits

- Groq – Ultra-low-latency LLM inference

- Pytesseract

- OpenCV

---

## 🏁 Final Words

This hackathon taught us how powerful real-time data, intelligent processing, and fast inference can be when combined. Groq's performance amazed us, and the overall system worked smoothly even under high frame loads. Excited to keep building

---
