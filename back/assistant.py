import ollama
import json
import os
import shutil
from PyPDF2 import PdfReader
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import StreamingResponse, JSONResponse

app = FastAPI()

# Variable global para almacenar el contenido del PDF cargado
pdf_text = None

# Función para extraer texto de un archivo PDF
def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error al extraer texto del PDF: {e}")
    return text


# Endpoint para cargar el PDF
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_text
    # Guardar el archivo PDF en el sistema de archivos
    file_path = f"./uploads/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extraer texto del PDF
    pdf_text = extract_text_from_pdf(file_path)
    return {"message": f"Archivo {file.filename} cargado y procesado correctamente"}


# Endpoint para eliminar el PDF cargado
@app.post("/delete_pdf")
async def delete_pdf():
    global pdf_text
    pdf_text = None

    # Eliminar el archivo del sistema de archivos
    if os.path.exists("./uploads"):
        for filename in os.listdir("./uploads"):
            file_path = os.path.join("./uploads", filename)
            os.remove(file_path)

    return {"message": "Archivo PDF eliminado, el asistente responderá preguntas generales"}

# Endpoint para interactuar con el chatbot usando el PDF cargado (si está disponible)
@app.post("/chat_with_pdf")
async def chat_with_pdf(request: Request):
    global pdf_text
    user_message = (await request.json()).get('message')
    
    # Si no hay PDF cargado, devolver un error
    if pdf_text is None:
        return JSONResponse(status_code=400, content={"error": "No hay PDF cargado"})
    
    # Llamada a Ollama con el contenido del PDF y el mensaje del usuario
    response = ollama.chat(model='llama3.2:1b', messages=[
        {
            'role': 'system',
            'content': f"El siguiente texto es una referencia del documento PDF cargado:\n\n{pdf_text}"
        },
        {
            'role': 'user',
            'content': user_message
        }
    ], stream=True)
    
    # Respuesta en streaming
    async def event_stream():
        for chunk in response:
            yield json.dumps(chunk['message']['content']) + "\n"
    
    return StreamingResponse(event_stream(), media_type="application/json")


# Endpoint para interactuar con el chatbot de forma general (sin usar PDF)
@app.post("/chat")
async def chat(request: Request):
    user_message = (await request.json()).get('message')
    
    # Llamada a Ollama sin contenido del PDF
    response = ollama.chat(model='llama3.2:1b', messages=[
        {
            'role': 'user',
            'content': user_message
        }
    ], stream=True)
    
    # Respuesta en streaming
    async def event_stream():
        for chunk in response:
            yield json.dumps(chunk['message']['content']) + "\n"
    
    return StreamingResponse(event_stream(), media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("assistant:app", host="127.0.0.1", port=8000, reload=True)
