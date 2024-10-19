from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import ollama
import json

app = FastAPI()

# Endpoint para interactuar con el chatbot
@app.post("/chat")
async def chat(request: Request):
    user_message = (await request.json()).get('message')
    response = ollama.chat(model='llama3.2:1b', messages=[
        {
            'role': 'user',
            'content': user_message
        }
    ], stream=True)
    
    async def event_stream():
        for chunk in response:
            yield json.dumps(chunk['message']['content']) + "\n"
    
    return StreamingResponse(event_stream(), media_type="application/json")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("assistant:app", host="127.0.0.1", port=8000, reload=True)
