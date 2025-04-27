# 🤖 Jarvis: Slack-Based NLP Chatbot  

A **Slack-integrated natural language classifier** that learns from real-time user input, classifies intent using machine learning, and even responds with **GIFs** to user prompts.

---

## 📍 Project Overview

Jarvis is an interactive **Slack chatbot** that classifies text messages into predefined intent categories using **scikit-learn models**. The bot allows users to:
- **Train the classifier** by labeling custom messages.  
- **Test its predictions** on new messages.  
- **Receive instant Slack replies** based on classified intent.  
- **Request GIFs** by specifying a category (e.g., "dog", "congratulations").  

The chatbot was built as a **proof-of-concept for interactive ML-based assistants**, demonstrating **incremental learning**, **real-time classification**, and **Slack API integration**.

📺 **Demo Video:** [Click here](https://www.youtube.com/watch?v=wdcLnbDB1Jk)

---

## 🛠️ Tech Stack

- **Python** (`scikit-learn`, `sqlite3`, `websocket-client`, `requests`)
- **Slack API** (Real-Time Messaging, Chat & File Upload APIs)
- **Machine Learning Models**: 
  - `SGDClassifier`
  - `Multinomial Naive Bayes`
- **Data Storage**: SQLite database for labeled training examples

---

## 🧠 How It Works

1️⃣ **User sends a message in Slack**  
2️⃣ **Jarvis classifies the intent** using its trained ML model  
3️⃣ **Slack bot responds** with a relevant message or GIF  

### 🔄 Training & Testing Workflow
- **"Training Time"**: Users provide labeled text for training.
- **"Testing Time"**: The trained model classifies new messages.
- **"GIF Time"**: Jarvis uploads and sends a relevant GIF.

---

## 🗃️ Data & Model Training

### 📊 **Dataset**
The chatbot is trained on **user-labeled text messages**, categorized into:
- **Time** (e.g., "What time is it?")
- **Pizza** (e.g., "Can I order a large pizza?")
- **Greet** (e.g., "Hello, how are you?")
- **Weather** (e.g., "What's the weather like?")
- **Joke** (e.g., "Tell me a joke!")

Example training data:

| Text                         | Category |
|------------------------------|----------|
| "Hey, what's up?"            | Greet    |
| "Can I order a pizza?"       | Pizza    |
| "What’s the weather today?"  | Weather  |

### 🏋️ **Training Pipeline**
1. **User labels messages** → Stored in SQLite.
2. **Text preprocessing** → `CountVectorizer` + `TF-IDF`.
3. **Model training** → `SGDClassifier` or `MultinomialNB`.
4. **New messages** → Classified based on trained model.

---

## 🚀 How to Run Locally

### **1️⃣ Set up the environment**
```bash
git clone https://github.com/ghmyers96/jarvis-slack-bot.git
cd jarvis-slack-bot
conda create -n jarvis_env python=3.10
conda activate jarvis_env
pip install -r config/requirements.txt
```
---
### **2️⃣ Set Up Slack Credentials**
1. Create a `.env` file in the root directory:
  API_TOKEN=your-slack-api-token APP_TOKEN=your-slack-app-token
2. **Ensure `.env` is in your `.gitignore`** to keep credentials secure.
---
### **3️⃣ Start the Slack Bot**
```bash
python scripts/bot.py
```
---
### **4️⃣ Test the Model (Without Slack)**
```from src.ml_model import JarvisModel
model = JarvisModel()
X_train, y_train = model.import_db()
model.train(X_train, y_train)

print(model.predict(["Hey, how are you?"]))  # Expected: "GREET"
```
---


