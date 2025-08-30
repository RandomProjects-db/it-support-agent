from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime
import requests

app = FastAPI(title="IT Support Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Data models
class TicketCreate(BaseModel):
    title: str
    description: str
    user_email: str
    priority: str = "medium"

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    ticket_id: Optional[int] = None

# In-memory storage (replace with database in production)
def load_tickets():
    """Load tickets from JSON file"""
    try:
        with open('tickets.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tickets():
    """Save tickets to JSON file"""
    with open('tickets.json', 'w') as f:
        json.dump(tickets, f, indent=2)

tickets = load_tickets()
policies = [
    {
        "id": 1,
        "title": "Password Reset Policy",
        "content": "Users can reset passwords using self-service portal. For admin accounts, manager approval required.",
        "category": "authentication"
    },
    {
        "id": 2,
        "title": "VPN Troubleshooting",
        "content": "1. Check internet connection 2. Restart VPN client 3. Clear DNS cache 4. Contact IT if issues persist",
        "category": "network"
    },
    {
        "id": 3,
        "title": "Software Installation",
        "content": "Standard software can be installed via company portal. Custom software requires IT approval.",
        "category": "software"
    }
]

def call_groq_api(messages):
    """Call Groq API for AI responses"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI service temporarily unavailable: {str(e)}"

@app.get("/")
def read_root():
    return {"message": "IT Support Agent API is running"}

@app.get("/api/tickets")
def get_tickets():
    return tickets

@app.post("/api/tickets")
def create_ticket(ticket: TicketCreate):
    new_ticket = {
        "id": len(tickets) + 1,
        "title": ticket.title,
        "description": ticket.description,
        "user_email": ticket.user_email,
        "priority": ticket.priority,
        "status": "new",
        "assigned_to": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "resolution": None,
        "ai_analysis": None
    }
    
    # Get AI analysis of the ticket
    messages = [
        {
            "role": "system",
            "content": """You are an IT support agent. Analyze the ticket using Chain of Thought reasoning:

STEP 1: CATEGORIZATION - What type of IT issue is this?
STEP 2: SEVERITY ASSESSMENT - How urgent/critical is this issue?
STEP 3: POLICY CONSULTATION - Which policies apply to this situation?
STEP 4: TROUBLESHOOTING STEPS - What are the recommended actions?
STEP 5: APPROVAL STATUS - Is this allowed/denied/requires approval?

Provide your analysis following this exact format."""
        },
        {
            "role": "user",
            "content": f"Ticket: {ticket.title}\nDescription: {ticket.description}"
        }
    ]
    
    ai_analysis = call_groq_api(messages)
    new_ticket["ai_analysis"] = ai_analysis
    
    # Log the Chain of Thought reasoning
    cot_log = {
        "ticket_id": new_ticket["id"],
        "timestamp": datetime.now().isoformat(),
        "reasoning_steps": ai_analysis,
        "policies_consulted": ["Password Reset Policy", "VPN Troubleshooting"]  # Would be dynamic
    }
    # In production, save this to a COT log database
    
    tickets.append(new_ticket)
    save_tickets()  # Save to file
    return new_ticket

@app.patch("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: int, update: TicketUpdate):
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if update.status:
        ticket["status"] = update.status
    if update.assigned_to:
        ticket["assigned_to"] = update.assigned_to
    if update.resolution:
        ticket["resolution"] = update.resolution
    
    ticket["updated_at"] = datetime.now().isoformat()
    save_tickets()  # Save to file
    return ticket

@app.post("/api/chat")
def chat_with_agent(chat: ChatMessage):
    # Find relevant policies
    relevant_policies = []
    for policy in policies:
        if any(keyword in chat.message.lower() for keyword in policy["title"].lower().split()):
            relevant_policies.append(policy)
    
    # Get historical context from similar resolved tickets
    similar_tickets = []
    for ticket in tickets:
        if ticket["status"] == "resolved" and any(word in ticket["title"].lower() for word in chat.message.lower().split()):
            similar_tickets.append({
                "title": ticket["title"],
                "resolution": ticket.get("resolution", "No resolution recorded"),
                "ai_analysis": ticket.get("ai_analysis", "")[:200]  # First 200 chars
            })
    
    # Prepare context for AI
    policy_context = "\n".join([f"Policy: {p['title']} - {p['content']}" for p in relevant_policies])
    history_context = "\n".join([f"Previous Case: {t['title']} - Resolution: {t['resolution']}" for t in similar_tickets[:3]])
    
    messages = [
        {
            "role": "system",
            "content": f"""You are an IT support agent. Follow these rules STRICTLY:
1. Always consult official policies before responding
2. Learn from previous similar cases to improve responses
3. Provide step-by-step instructions as a numbered checklist
4. MUST include one of these statements: "ACTION ALLOWED", "ACTION DENIED", or "REQUIRES APPROVAL"
5. Include policy citations for every recommendation
6. Be transparent about your reasoning process

Available Policies:
{policy_context}

Previous Similar Cases:
{history_context}

Response Format:
1. [Step-by-step checklist]
2. STATUS: [ALLOWED/DENIED/REQUIRES APPROVAL]
3. POLICY CITATION: [Reference to specific policy]
4. REASONING: [Explain decision process]
5. HISTORICAL CONTEXT: [Reference similar past cases if relevant]"""
        },
        {
            "role": "user",
            "content": chat.message
        }
    ]
    
    ai_response = call_groq_api(messages)
    
    return {
        "response": ai_response,
        "relevant_policies": relevant_policies,
        "similar_cases": len(similar_tickets),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/policies")
def get_policies():
    return policies

@app.get("/api/analytics")
def get_analytics():
    total_tickets = len(tickets)
    status_counts = {}
    priority_counts = {}
    
    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]
        
        status_counts[status] = status_counts.get(status, 0) + 1
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    return {
        "total_tickets": total_tickets,
        "status_distribution": status_counts,
        "priority_distribution": priority_counts
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
