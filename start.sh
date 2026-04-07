#!/bin/bash

# --- বটের নাম বা ডিরেক্টরি সেট করা ---
APP_NAME="IBRAHIM BOT X"

echo "🚀 $APP_NAME চালু করার প্রক্রিয়া শুরু হচ্ছে..."

# ১. প্রয়োজনীয় লাইব্রেরি ইনস্টল করা (যদি না থাকে)
if [ -f "requirements.txt" ]; then
    echo "📦 লাইব্রেরি চেক করা হচ্ছে..."
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt পাওয়া যায়নি, সরাসরি রান করা হচ্ছে।"
fi

# ২. মেইন পাইথন ফাইলটি রান করা
# আপনার ফাইলের নাম যদি main.py না হয়ে অন্য কিছু হয়, তবে এখানে পরিবর্তন করুন
PYTHON_FILE="main.py"

if [ -f "$PYTHON_FILE" ]; then
    echo "✅ $PYTHON_FILE খুঁজে পাওয়া গেছে। বট স্টার্ট হচ্ছে..."
    python3 $PYTHON_FILE
else
    echo "❌ ত্রুটি: $PYTHON_FILE ফাইলটি খুঁজে পাওয়া যায়নি!"
    exit 1
fi
