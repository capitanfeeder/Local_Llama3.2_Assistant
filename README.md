# **`Asistente Local Llama 3.2`**

## **Introducción**

###  El presente proyecto es un asistente virtual offline que, mediante el uso de modelos locales de inteligencia artificial, responde preguntas de manera eficiente y segura. Este asistente está diseñado para funcionar en entornos locales, lo que garantiza la privacidad y seguridad de los datos, ya que no se requiere conexión a internet para su funcionamiento.

## **Tecnologías Utilizadas**

- ![Python](https://img.shields.io/badge/Python-black?style=flat&logo=python)&nbsp; Lenguaje de programación utilizado para el desarrollo del asistente.

- ![Llama 3.2](https://img.shields.io/badge/Llama%203.2-black?style=flat&logo=llama)&nbsp; Utiliza un modelo de lenguaje avanzado para generar respuestas precisas y contextuales.

- ![FastAPI](https://img.shields.io/badge/FastAPI-black?style=flat&logo=fastapi)&nbsp; Framework moderno y rápido para construir APIs en Python.

- ![Streamlit](https://img.shields.io/badge/Streamlit-black?style=flat&logo=streamlit)&nbsp; Biblioteca de Python para crear aplicaciones web interactivas de manera sencilla.

- ![Ollama](https://img.shields.io/badge/Ollama-black?style=flat&logo=ollama)&nbsp; Plataforma que facilita la gestión y ejecución de modelos de inteligencia artificial locales.

## **Beneficios**

- `Privacidad y Seguridad:` Al funcionar completamente offline, se evita la exposición de datos a terceros.

- `Rendimiento:` Los modelos locales pueden ofrecer respuestas rápidas y eficientes sin depender de conexiones de red.

## **Aplicaciones**

`Consultas Generales:` Responder preguntas sobre una amplia gama de temas.

`Asistencia Técnica:` Proporcionar soporte y respuestas técnicas en entornos controlados.

`Educación:` Ayudar en la enseñanza y el aprendizaje mediante preguntas y respuestas interactivas.

`Investigación:` Facilitar la búsqueda y análisis de información en entornos académicos o empresariales.

## **Requerimientos**

### 1. **Ingresar al sitio web de ollama:** https://ollama.com/

### 2. **Descargar e instalar**

### 3. **Abrir una terminal de Windows (CMD o Powershell) e iniciar ollama con el comando ollama:**

<p align="center"> <img src="https://i.imgur.com/xTeYJWC.png" width="500" /> </p> <p align="center"> <img src="https://i.imgur.com/0K6FMRG.png" width="500" /> </p>

### 4. **Regresar al sitio de ollama y elegir el modelo llama3.2 o el de su preferencia:**

<p align="center"> <img src="https://i.imgur.com/xq6AkFR.png" width="500" /> </p>

### 5. **Seleccionar el modelo que se ajuste a la capacidad de la máquina, por defecto nos permite la descarga del modelo de 1000 millones de parámetros o el de 3000 millones de parámetros.**
### **Por regla general, la máquina debe tener como mínimo el doble de capacidad de RAM para un mejor rendimiento. Ej: para 3b se debe contar con 6gb de RAM.**

<p align="center"> <img src="https://i.imgur.com/YdsiToc.png" width="500" /> </p>

### 6. **Copiamos el comando de descarga y lo pegamos en la terminal**

<p align="center"> <img src="https://i.imgur.com/gulpTE4.png" width="500" /> </p> <p align="center"> <img src="https://i.imgur.com/yiGsCF3.png" width="500" /> </p>

### 7. **Finalizada la descarga, configuramos un entorno siguiendo los siguientes pasos en el editor:**

**a) Crear un entorno virtual**: colocando el siguiente comando en terminal, reemplazando `your-env-name` por el nombre que desees darle al entorno virtual:

`python -m venv "your-env-name"`

**b) Activar el entorno virtual**: colocando el siguiente comando en terminal:

Desde windows:

`.\your-env-name\Scripts\Activate`

Desde linux:

`source your-env-name/bin/activate`

**c) Ubicarse dentro del entorno y clonar el repositorio**

### 8. **Instalar las librerías necesarias mediante el comando:**

`pip install -r requirements.txt`

### 9. **En caso de haber descargado otro modelo se debe cambiar el nombre del mismo en el archivo back/assistant.py en el parámetro `model`**
### **Por defecto viene configurado con el modelo de 1000 millones de parámetros por tener un rendimiento para un equipo con 16gb de RAM y procesador Intel Core i7 de 11° generación.**

<p align="center"> <img src="https://i.imgur.com/mp9QDhY.png" width="500" /> </p>

### 10. **Ejecutar el programa con el comando:** 
 `python main.py`

<p align="center"> <img src="https://i.imgur.com/CiHCEmt.png" width="500" /> </p>

## **Descripción General de la Funcionalidad:**

### 1. `Chat con Modelo Local Llama 3.2:`

- Permite a los usuarios interactuar con un modelo de lenguaje local (Llama 3.2) para obtener respuestas a sus preguntas.

- La interacción se realiza a través de una interfaz de chat en Streamlit.

### 2. `Gestión de Procesos Backend y Frontend:`

- Inicia y gestiona el servidor backend utilizando FastAPI.

- Inicia y gestiona la aplicación frontend utilizando Streamlit.

- Mantiene la aplicación en ejecución hasta que se interrumpa manualmente (Ctrl+C).

## **Análisis del Código:**

### 1. `main.py`:
- Maneja la configuración y gestión de procesos para el backend y frontend.

- Inicia el servidor backend utilizando FastAPI en el puerto 8000.

- Inicia la aplicación frontend utilizando Streamlit en el puerto 8501.

- Mantiene la aplicación en ejecución hasta que se interrumpa manualmente.

### 2. `back/assistant.py`:
- Define el endpoint /chat para interactuar con el chatbot.

- Utiliza el modelo Llama 3.2 para generar respuestas a las preguntas del usuario.

- Devuelve las respuestas en forma de stream.

### 3. `front/interface.py`:
- Configura la interfaz de usuario utilizando Streamlit.

- Maneja la entrada del usuario y envía mensajes al backend para obtener respuestas.

- Muestra las respuestas del asistente en tiempo real.


## **Autor:**
- Sosa Gabriel (Analista de Datos Jr.)