# Enterprise-agent
Enterprise Agent – Internal HR / Support Assistant
This project implements a small but complete Enterprise Agent that demonstrates how natural-language agents can improve business workflows without requiring large datasets or complex infrastructure.
The agent is designed as an internal assistant for a business team (e.g., HR or internal support). Users ask questions in plain language—such as:
•	“What are the working hours?”
•	“What is our leave policy?”
•	“How many leaves do I have left?”
•	“Can you draft a leave request email for me?”
The agent routes these queries to simple tools that return policy text, small internal data, or templates, and formats a clear reply.

Features
•	Answers FAQs from internal policies (e.g., working hours, leave policy, probation period).
•	Checks a mock leave balance for an example employee.
•	Generates email templates for common requests (e.g., leave request).
•	Safely handles out-of-scope questions by suggesting the user contact HR or the relevant team.
•	Demonstrates context engineering, tool-based (MCP-style) design, and a clean, extensible architecture.

Architecture Overview
The system is structured into simple, understandable layers:
1.	User Interface Layer
o	In this prototype: function calls and prints in a notebook/script.
o	Captures the user query and displays the agent’s reply.
2.	Context Builder / Orchestrator
o	Combines:
	System prompt (role, rules, tone)
	Tool descriptions
	Enterprise knowledge (mock policies, data)
	User message
o	Shapes how the agent is expected to behave.
3.	Agent Logic / Router
o	Analyses the query (keywords / intent).
o	Decides which tool to call:
	get_policy – policy lookup
	get_leave_balance – record lookup
	draft_email_reply – template generation
o	Uses a safe fallback for unsupported queries.
4.	Tools & Data Layer
o	Tools: pure Python functions implementing operations.
o	Data: small in-memory dictionaries:
 	HR_POLICIES for policy text
	EMPLOYEE_LEAVE for example employee records
Flow:
User → UI → Context Builder → Agent Router → Tools → Data → Response → User

Tech Stack
•	Language: Python 3
•	Environment: Kaggle Notebook or any local Python environment
•	Dependencies: Only standard Python libraries (no external packages required for the basic version)

Setup & Running
Option 1: Kaggle Notebook
1.	Create a new Notebook on Kaggle.
2.	Copy the code cells from this project:
o	Config & mock data (policies, employee leave).
o	Tools (get_policy, get_leave_balance, draft_email_reply, log_interaction).
o	Agent router (enterprise_agent).
o	Test queries.
3.	Run all cells from top to bottom.
4.	Observe agent responses in the output cells.
Option 2: Local Python (Script)
1.	Create and activate a virtual environment (optional):
2.	python -m venv venv
3.	source venv/bin/activate       # Windows: venv\Scripts\activate
4.	Save the agent code into enterprise_agent.py.
5.	Run:
6.	python enterprise_agent.py
7.	Check the console for example user queries and agent replies.

Core Code Snippets (Conceptual)
Mock data:
HR_POLICIES = {
    "working_hours": "Our standard working hours are 9:30 AM to 6:30 PM, Monday to Friday.",
    "leave_policy": "Employees are entitled to 20 days of paid leave per year.",
    "probation_period": "The probation period is 6 months from the date of joining."
}

EMPLOYEE_LEAVE = {
    "EMP001": {"name": "Bhoomi", "total_leaves": 20, "used_leaves": 6},
}
Tools:
def get_policy(policy_name: str) -> str:
    return HR_POLICIES.get(policy_name.lower(), "Policy not found. Please contact HR.")

def get_leave_balance(employee_id: str) -> str:
    data = EMPLOYEE_LEAVE.get(employee_id.upper())
    if not data:
        return "Employee not found in leave records."
    remaining = data["total_leaves"] - data["used_leaves"]
    return f"{data['name']} has {remaining} days of leave remaining."

def draft_email_reply(purpose: str) -> str:
    if purpose == "leave_request":
        return (
            "Subject: Leave Request\n\n"
            "Dear [Manager Name],\n\n"
            "I would like to request leave from [start date] to [end date]. "
            "Please let me know if this works.\n\n"
            "Regards,\n[Your Name]"
        )
    return "No template available for this purpose."
Agent router + logging:
import datetime

def log_interaction(user_query: str, agent_reply: str):
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    print(f"[{ts}] USER: {user_query}")
    print(f"[{ts}] AGENT: {agent_reply}")

def enterprise_agent(user_query: str, employee_id: str = "EMP001") -> str:
    q = user_query.lower()

    if "working hours" in q or "timing" in q:
        reply = get_policy("working_hours")
    elif "leave policy" in q:
        reply = get_policy("leave_policy")
    elif "probation" in q:
        reply = get_policy("probation_period")
    elif "leave balance" in q or "how many leaves" in q:
        reply = get_leave_balance(employee_id)
    elif "email" in q and "leave" in q:
        reply = draft_email_reply("leave_request")
    else:
        reply = "I'm not sure about this request. Please contact HR for detailed assistance."

    log_interaction(user_query, reply)
    return reply

Example Usage
queries = [
    "What are the working hours?",
    "Tell me about the leave policy.",
    "How many leaves do I have left?",
    "Can you draft an email for a leave request?",
    "What is the probation period?",
    "Tell me my salary structure."  # out of scope
]

for q in queries:
    print("USER :", q)
    print("AGENT:", enterprise_agent(q))
    print("-" * 50)

Evaluation & Agent Quality
•	Relevance: Does the response match the query intent?
•	Accuracy: Does the agent only use stored policies and data (no hallucinations)?
•	Tone: Is the language polite and professional?
•	Safety & Scope: For unsupported requests, does the agent respond safely and defer to HR?
You can add more test queries to evaluate different edge cases.

Future Improvements
•	Integrate with a real database or APIs for policies and employee data.
•	Replace keyword routing with LLM-based intent classification.
•	Add a web or chat UI for real users.
•	Implement more tools (ticket creation, holiday calendar, IT support, etc.).
•	Add structured logging and monitoring for production readiness.

License
This project is for educational and demonstration purposes. Feel free to adapt and extend it for your own learning or internal prototypes.
