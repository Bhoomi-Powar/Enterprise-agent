HR_POLICIES = {
    "working_hours": "Our standard working hours are 9:30 AM to 6:30 PM, Monday to Friday.",
    "leave_policy": "Employees are entitled to 20 days of paid leave per year, including casual and sick leave.",
    "probation_period": "The probation period is 6 months from the date of joining.",
}
SYSTEM_PROMPT = """
You are an internal HR assistant for an enterprise.
- Answer only HR-related queries based on company policies.
- Be concise, polite, and neutral.
- If you do not know the answer or policy is not defined, say so and suggest contacting HR.
- Never invent legal or medical advice.
"""
TOOLS_DESCRIPTION = """
Tools you can use:
1. get_policy(policy_name): Returns the text of the requested HR policy.
2. get_leave_balance(employee_id): Returns remaining leave days for the employee.
3. draft_email_reply(purpose, tone): Returns a short email template.

Use tools when needed instead of guessing.
"""
def get_policy(policy_name: str) -> str:
    policy = HR_POLICIES.get(policy_name.lower())
    if policy is None:
        return "Policy not found. Please contact HR for more details."
    return policy

def get_leave_balance(employee_id: str) -> str:
    data = EMPLOYEE_LEAVE.get(employee_id.upper())
    if not data:
        return "Employee not found in leave records."
    remaining = data["total_leaves"] - data["used_leaves"]
    return f"{data['name']} has {remaining} days of leave remaining."

def draft_email_reply(purpose: str, tone: str = "polite") -> str:
    if purpose == "leave_request":
        return ("Subject: Leave Request\n\n"
                "Dear [Manager Name],\n\n"
                "I would like to request leave from [start date] to [end date]. "
                "Please let me know if this works or if any adjustments are needed.\n\n"
                "Regards,\n[Your Name]")
    if purpose == "policy_clarification":
        return ("Subject: HR Policy Clarification\n\n"
                "Dear HR Team,\n\n"
                "I would like to clarify details regarding the [policy name] policy.\n\n"
                "Thank you,\n[Your Name]")
    return "Template not available for this purpose."
def simple_agent_router(user_query: str):
    q = user_query.lower()
    
    if "working hours" in q or "timing" in q:
        return get_policy("working_hours")
    if "leave policy" in q:
        return get_policy("leave_policy")
    if "probation" in q:
        return get_policy("probation_period")
    if "leave balance" in q or "how many leaves" in q:
        # simple demo: assume EMP001
        return get_leave_balance("EMP001")
    if "email" in q and "leave" in q:
        return draft_email_reply("leave_request")
    
    return "I'm not sure about this. Please contact HR for detailed assistance."
TEST_QUERIES = [
    "What are the working hours?",
    "Tell me about the leave policy.",
    "How many leaves do I have left?",
    "Can you draft an email for leave request?",
    "What is the probation period?",
    "Give me my salary details.",  # should refuse
]

for q in TEST_QUERIES:
    print("USER:", q)
    print("AGENT:", simple_agent_router(q))
    print("-" * 40)
import datetime

def log_interaction(user_query: str, agent_reply: str):
    timestamp = datetime.datetime.now().isoformat()
    print(f"[{timestamp}] USER: {user_query}")
    print(f"[{timestamp}] AGENT: {agent_reply}")
