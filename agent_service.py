import os
import json
from openai import OpenAI
from dotenv import load_dotenv  # <--- הוסף את זה
from todo_service import add_task, get_tasks, update_task, delete_task


load_dotenv()  # <--- והוסף את זה
api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

# הגדרת הכלים - שומרים על הגמישות כדי למנוע קריסות טכניות, אך הלוגיקה אוכפת חוקים
tools_todo = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "הוספת משימה חדשה",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "כותרת המשימה"},
                    "description": {"type": "string", "description": "תיאור"},
                    "task_type": {"type": "string", "description": "סוג (אישי/עבודה)"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "הצגת משימות",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["pending", "completed"]},
                    "sort_by": {"type": "string", "enum": ["title"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "עדכון משימה",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "status": {"type": "string", "enum": ["pending", "completed"]}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "מחיקת משימה",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"}
                },
                "required": ["task_id"]
            }
        }
    }
]

def run_agent(user_query: str):
    try:
        messages = [
            {
                "role": "system", 
                "content": """אתה עוזר ניהול משימות מקצועי. ענה בעברית.
                
                חוקי הברזל שלך:
                1. הוספה: אם המשתמש לא ציין כותרת ברורה, אל תבצע. ענה: 'עליך לספק כותרת למשימה כדי שאוכל להוסיף אותה'.
                2. מחיקה/עדכון: אם המשתמש לא ציין מספר משימה (ID), עצור והסבר: 'כדי לבצע את הפעולה עליך לציין את מספר המשימה. תוכל לראות את המספרים על ידי בקשת "הצג משימות"'.
                3. תיקון טעויות: אם המשתמש כותב משהו לא מובן או חסר, תמיד תן לו דוגמה לאיך לכתוב נכון. למשל: 'נסה לכתוב: "מחק משימה 5"'.
                4. לאחר הוספה מוצלחת: הודע למשתמש שהמשימה נוספה, וציין שהוא יכול להוסיף גם תיאור וסוג משימה (עבודה/אישי) כדי לארגן את הרשימה טוב יותר.
                5. בחיפוש/הצגה: אם לא צוין סטטוס, הצג משימות בסטטוס 'pending'."""
            },
            {"role": "user", "content": user_query}
        ]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools_todo,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                f_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments or "{}")
                
                if f_name == "add_task":
                    # וידוא כותרת לפני הרצה
                    if not args.get("title"):
                         return "עליך לספק כותרת למשימה כדי שאוכל להוסיף אותה."
                    
                    result = add_task(
                        title=args.get("title"),
                        description=args.get("description", "ללא תיאור"),
                        task_type=args.get("task_type", "כללי")
                    )
                elif f_name == "get_tasks":
                    result = get_tasks(
                        status=args.get("status", "pending"), 
                        sort_by=args.get("sort_by", "title")
                    )
                elif f_name == "update_task":
                    if args.get("task_id") is None:
                        return "כדי לעדכן, עליך לספק את מספר המשימה (ID)."
                    
                    result = update_task(
                        task_id=args.get("task_id"),
                        title=args.get("title", "משימה מעודכנת"),
                        status=args.get("status", "pending")
                    )
                elif f_name == "delete_task":
                    if args.get("task_id") is None:
                        return "כדי למחוק, עליך לספק את מספר המשימה (ID)."
                    
                    result = delete_task(task_id=args.get("task_id"))
                else:
                    result = {"error": "unknown function"}

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result if result else {"status": "success"}, ensure_ascii=False)
                })
            
            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )
            return final_response.choices[0].message.content

        return response_message.content

    except Exception as e:
        # טיפול חכם בשגיאת מכסה (Rate Limit)
        if "429" in str(e):
            return "הגעתי למכסת הטוקנים היומית ב-Groq. נסה שוב בעוד מספר דקות או החלף מודל בקוד ל-8b."
        
        print(f"DEBUG ERROR: {e}")
        return "מצטער, הייתה לי שגיאה פנימית. נסה שוב או בקש 'הצג משימות'."