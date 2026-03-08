# 🤖 AI Task Management Agent

סוכן בינה מלאכותית חכם לניהול משימות המבוסס על **Groq (Llama 3.3)** ו-**FastAPI**.  
הסוכן יודע לקבל הוראות בשפה חופשית, לבצע פעולות בבסיס הנתונים (CRUD) ולוודא שהמשתמש מספק את כל הפרטים הנדרשים.

---

## ✨ תכונות עיקריות (Features)
- **הבנת שפה טבעית:** הוספת משימות, עדכון סטטוס ומחיקה בדיבור חופשי.
- **אימות נתונים חכם:** הסוכן לא יבצע פעולה אם חסרה כותרת או מזהה (ID), ויציע למשתמש דוגמה לתיקון.
- **ניהול קטגוריות:** אפשרות לשייך משימות לסוגים (עבודה, אישי וכו') ולהוסיף תיאור מפורט.
- **ממשק API:** בנוי על FastAPI עם תמיכה מלאה ב-CORS.

---

## 🛠 טכנולוגיות (Tech Stack)
- **AI Engine:** [Groq Cloud](https://console.groq.com/) (Llama-3.3-70b)
- **Framework:** FastAPI (Python)
- **Environment:** Dotenv for secure API keys
- **Tools:** OpenAI SDK for Tool Calling

---

## 🚀 הוראות הפעלה (Setup)

### 1. התקנת דרישות
וודא שמותקן אצלך Python 3.10 ומעלה, והרצ:
```bash
pip install -r requirements.txt
