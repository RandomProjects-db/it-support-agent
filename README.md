# IT Support Agent

AI-powered IT support ticket management system with intelligent policy consultation and automated troubleshooting assistance.

## 🎥 Demo Video

**[Watch Live Demo](https://www.youtube.com/watch?v=3m9ieKRyR-I)** - See the AI agent in action with ticket management, chat interface, and policy consultation.

## Features

🎫 **Ticket Management**
- Create, track, and manage IT support tickets
- Automatic AI analysis of new tickets
- Status tracking (New → In Progress → Resolved → Closed)
- Priority assignment and filtering

🤖 **AI Assistant**
- Chat interface for instant IT support
- Policy consultation with citations
- Transparent reasoning and decision-making
- Step-by-step troubleshooting guides

📊 **Analytics Dashboard**
- Ticket metrics and trends
- Status and priority distributions
- Resolution rate tracking
- Performance insights

## Architecture

**Backend (Python FastAPI)**
- RESTful API for ticket management
- Groq LLM integration for AI responses
- Policy database and search
- Audit logging and compliance

**Frontend (React/Next.js)**
- Modern, responsive dashboard
- Real-time ticket updates
- Interactive chat interface
- Analytics visualizations

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/RandomProjects-db/it-support-agent.git
cd it-support-agent

# Copy environment template and add your API key
cp .env.example .env
# Edit .env file and replace with your actual Groq API key:
# GROQ_API_KEY=your-actual-groq-api-key-here
```

### 2. Start Backend API

```bash
# Install Python dependencies
pip install fastapi uvicorn requests python-dotenv

# Start the API server
python main.py
```

API will be available at: `http://localhost:8000`

### 3. Start Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### 4. Get Your Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file

### 2. Start the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## API Endpoints

### Tickets
- `GET /api/tickets` - List all tickets
- `POST /api/tickets` - Create new ticket
- `PATCH /api/tickets/{id}` - Update ticket status

### AI Assistant
- `POST /api/chat` - Chat with AI assistant
- `GET /api/policies` - List IT policies

### Analytics
- `GET /api/analytics` - Get ticket analytics

## Usage Examples

### Creating a Ticket
```json
POST /api/tickets
{
  "title": "VPN Connection Issues",
  "description": "Cannot connect to company VPN from home",
  "user_email": "user@company.com",
  "priority": "high"
}
```

### Chat with AI Assistant
```json
POST /api/chat
{
  "message": "How do I reset my password?"
}
```

## AI Features

**Policy Consultation**
- Automatically references relevant IT policies
- Provides step-by-step instructions
- Indicates if actions require approval

**Transparent Reasoning**
- Explains decision-making process
- Cites policy sources
- Logs all actions for compliance

**Intelligent Analysis**
- Categorizes tickets automatically
- Suggests troubleshooting steps
- Prioritizes based on severity

## Configuration

The system uses Groq API for LLM integration. The API key is configured in `main.py`.

For production deployment:
1. Set environment variables for API keys
2. Use a proper database (PostgreSQL, MySQL)
3. Implement user authentication
4. Add rate limiting and security measures

## Technology Stack

- **Backend**: Python, FastAPI, Groq API
- **Frontend**: React, Next.js, TypeScript, Tailwind CSS
- **AI**: Llama 3.1 via Groq
- **Storage**: In-memory (development), JSON files

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'dotenv'"**
```bash
pip install python-dotenv
```

**"API service temporarily unavailable"**
- Check your Groq API key in `.env` file
- Ensure you have internet connection
- Verify API key is valid at [console.groq.com](https://console.groq.com)

**Port 8000 already in use**
```bash
# Kill existing process
lsof -i :8000
kill <PID>
```

**Frontend can't connect to API**
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Restart both frontend and backend

## Development

The system is designed for local development with external AI services:
- Backend runs locally with full API functionality
- Frontend connects to local backend
- AI responses fetched from Groq cloud service
- All data stored locally for privacy and compliance
