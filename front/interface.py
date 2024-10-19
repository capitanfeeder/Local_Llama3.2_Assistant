import streamlit as st
import requests
import json
import re

# Función para enviar un mensaje al backend y recibir la respuesta en forma de stream
def send_message(message):
    """
    Envía un mensaje al backend y recibe la respuesta en forma de stream.

    Args:
        message (str): El mensaje del usuario que se enviará al backend.

    Returns:
        iter: Un iterador que proporciona las líneas de la respuesta del backend.
    """
    response = requests.post('http://localhost:8000/chat', json={'message': message}, stream=True)
    return response.iter_lines(decode_unicode=True)

# Función para verificar si el texto contiene bloques de código
def is_code(text):
    """
    Verifica si el texto contiene bloques de código.

    Args:
        text (str): El texto a verificar.

    Returns:
        bool: True si el texto contiene bloques de código, False en caso contrario.
    """
    return re.search(r'```.*```', text, re.DOTALL) is not None

# Función para formatear el texto de respuesta
def format_response(text):
    """
    Formatea el texto de respuesta para resaltar bloques de código y reemplazar etiquetas HTML.

    Args:
        text (str): El texto de respuesta a formatear.

    Returns:
        str: El texto formateado.
    """
    # Encuentra todos los bloques de código y los formatea
    code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    for code_block in code_blocks:
        formatted_code = f"```\n{code_block}\n```"
        text = text.replace(f'```{code_block}```', formatted_code)
    
    # Reemplaza las etiquetas <br> con saltos de línea
    text = text.replace('<br>', '\n')
    
    return text

# Función principal
def main():
    """
    Función principal que maneja la interfaz de usuario y la lógica de chat.

    Esta función configura la interfaz de Streamlit, maneja la entrada del usuario,
    envía mensajes al backend, y muestra las respuestas del asistente en tiempo real.
    """
    st.title("Asistente Local Ollama")
    st.caption("Chatea con tu modelo Ollama local para obtener respuestas a tus preguntas. 🦙")

    # Inicializa el historial de chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Layout principal
    chat_placeholder = st.container()

    with chat_placeholder:
        # Muestra el historial de chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=message["avatar"]):
                st.markdown(message["content"])

    # Área de entrada del usuario en la parte inferior
    prompt = st.chat_input("¿En qué puedo ayudarte?")

    if prompt:
        # Añade el mensaje del usuario al historial de chat
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👨‍💼"})  # Emoji para el usuario
        # Muestra el mensaje del usuario en el contenedor de chat
        with chat_placeholder:
            with st.chat_message("user", avatar="👨‍💼"):  # Emoji para el usuario
                st.markdown(prompt)
        
        with st.spinner('Generando respuesta...'):
            # Envía el mensaje del usuario al backend y obtiene la respuesta en stream
            response_stream = send_message(prompt)
            assistant_response = ""
            assistant_message_placeholder = st.empty()

            for chunk in response_stream:
                if chunk:
                    try:
                        chunk_data = json.loads(chunk)
                        assistant_response += chunk_data
                        # Formatea la respuesta incrementalmente
                        formatted_response = format_response(assistant_response)
                        # Actualiza el mensaje del asistente en tiempo real
                        with assistant_message_placeholder.container():
                            with st.chat_message("assistant", avatar="🤖"):
                                st.markdown(formatted_response, unsafe_allow_html=True)
                    except json.JSONDecodeError:
                        pass

        # Añade el mensaje del asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": formatted_response, "avatar": "🤖"})  # Emoji para el asistente


if __name__ == "__main__":
    main()
