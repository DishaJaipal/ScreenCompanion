![github-submission-banner](https://github.com/user-attachments/assets/a1493b84-e4e2-456e-a791-ce35ee2bcf2f)

# 🚀 Project Title

> A one-line tagline or mission statement for your project.
Screen Companion using groq and Screenpipe 
---

## 📌 Problem Statement
 
****

---

## 🎯 Objective

Our project captures screen content in real-time, extracts meaningful text using OCR (Optical Character Recognition), and streams the data using Fluvio for downstream processing.
It serves teams or individuals who need live screen monitoring, text extraction, or real-time analytics from screen activities — helpful for accessibility, productivity tools, or automating workflows.

We enhance the extracted text using Groq's ultra-fast LLM inference for real-time insights and pattern detection, enabling instant feedback or action suggestions based on screen activity.
---

## 🧠 Team & Approach

### Team Name:  


### Team Members:  
- Name 1 (GitHub / LinkedIn / Role)  
- Name 2  
- Name 3  
*(Add links if you want)*

### Your Approach:  
- Chose this problem to explore real-time text processing + intelligent stream analysis, using powerful tools like OpenCV, Pytesseract, Fluvio, and Groq.

- Key challenges included OCR optimization, efficient real-time streaming, and seamless LLM integration with minimal latency.

- Breakthroughs included successful low-latency streaming and integrating Groq for rapid LLM inference on extracted text.



---

## 🛠️ Tech Stack

### Core Technologies Used:
- Frontend: React (for consumer visualization)

- Backend: Python (for frame processing, Fluvio producer, and Groq integration)

- Database: N/A

- APIs: Pytesseract, OpenCV, Groq Cloud API

- Hosting: GitHub 

### Sponsor Technologies Used :
- [✅] **Groq:** Used to process extracted screen text with high-speed LLM inference for smart insights.
- [ ] **Monad:**   
- [✅] **Fluvio:** Used for streaming extracted text data from screen in real-time.  
- [ ] **Base:** 
- [✅] **Screenpipe:** Used for efficient screen capturing and frame handling.
- [ ] **Stellar:** 

---

## ✨ Key Features

Highlight the most important features of your project:

- ✅ Real-time screen capture using ScreenPipe

- ✅ Text extraction via OCR (Pytesseract)

- ✅ Real-time data streaming using Fluvio

- ✅ Groq-powered LLM analysis on extracted text




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

- ScreenPipe installed

- .env file with keys and topic names

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

- ScreenPipe

- Fluvio

- Pytesseract

- OpenCV

- Huge thanks to mentors and hackathon organizers!
---

## 🏁 Final Words

This hackathon taught us how powerful real-time data, intelligent processing, and fast inference can be when combined. Groq's performance amazed us, and the overall system worked smoothly even under high frame loads. Excited to keep building

---
