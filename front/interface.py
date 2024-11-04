import streamlit as st
import requests
import json
import re

# Configuración de la página
st.set_page_config(
    page_title="Ollama Local",
    page_icon="🦙",
    layout="centered"
)

# Función para enviar un mensaje al backend y recibir la respuesta en forma de stream
def send_message(message, use_pdf):
    """
    Envía un mensaje al backend y recibe la respuesta en forma de stream.
    
    Args:
        message (str): El mensaje del usuario que se enviará al backend.
        use_pdf (bool): Indica si el mensaje debe procesarse utilizando el PDF cargado.
    
    Returns:
        iter: Un iterador que proporciona las líneas de la respuesta del backend.
    """
    url = 'http://localhost:8000/chat' if not use_pdf else 'http://localhost:8000/chat_with_pdf'
    response = requests.post(url, json={'message': message}, stream=True)
    return response.iter_lines(decode_unicode=True)

# Función para cargar el PDF al backend
def upload_pdf(file):
    response = requests.post("http://localhost:8000/upload_pdf", files={"file": file})
    if response.status_code == 200:
        return response.json().get("message")
    return response.json().get("error")

# Función para eliminar el PDF cargado
def delete_pdf():
    response = requests.post("http://localhost:8000/delete_pdf")
    if response.status_code == 200:
        return response.json().get("message")
    return response.json().get("error")

# Función para formatear el texto de respuesta
def format_response(text):
    code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    for code_block in code_blocks:
        formatted_code = f"```\n{code_block}\n```"
        text = text.replace(f'```{code_block}```', formatted_code)
    
    text = text.replace('<br>', '\n')
    return text

# Interfaz principal
def main():
    st.title("Asistente Local Ollama con Capacidad RAG")

    # Barra lateral para cargar/eliminar PDF
    st.sidebar.header("Configuración de PDF")
    pdf_file = st.sidebar.file_uploader("Sube un archivo PDF", type="pdf")
    pdf_uploaded = False

    if pdf_file:
        upload_response = upload_pdf(pdf_file)
        st.sidebar.success(upload_response)
        pdf_uploaded = True

    if st.sidebar.button("Eliminar PDF"):
        delete_response = delete_pdf()
        st.sidebar.info(delete_response)
        pdf_uploaded = False

    # Mensaje de indicación de estado del PDF
    if pdf_uploaded:
        st.sidebar.markdown("📄 PDF cargado: Las respuestas se basarán en este archivo.")
    else:
        st.sidebar.markdown("💬 No hay PDF cargado: El chatbot responderá de forma general.")

    # Inicializa el historial de chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Muestra el historial de chat
    chat_placeholder = st.container()
    with chat_placeholder:
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.markdown(message["content"])

    # Entrada de mensaje del usuario
    prompt = st.chat_input("Escribe tu mensaje para el asistente")

    if prompt:
        # Añade el mensaje del usuario al historial de chat
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👨‍💼"})
        with chat_placeholder:
            with st.chat_message("user", avatar="👨‍💼"):
                st.markdown(prompt)

        # Determina si se debe utilizar el PDF cargado en la respuesta
        with st.spinner('Generando respuesta...'):
            response_stream = send_message(prompt, pdf_uploaded)
            assistant_response = ""
            assistant_message_placeholder = st.empty()

            for chunk in response_stream:
                if chunk:
                    try:
                        chunk_data = json.loads(chunk)
                        assistant_response += chunk_data
                        formatted_response = format_response(assistant_response)
                        with assistant_message_placeholder.container():
                            with st.chat_message("assistant", avatar="🤖"):
                                st.markdown(formatted_response, unsafe_allow_html=True)
                    except json.JSONDecodeError:
                        pass

        # Añade el mensaje del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": formatted_response, "avatar": "🤖"})

if __name__ == "__main__":
    main()
