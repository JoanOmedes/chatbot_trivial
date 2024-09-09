# Proyecto Chatbot con Reconocimiento de Voz

Este es un proyecto en el que se ha desarrollado un chatbot con capacidad de reconocer voz a texto (speech-to-text) y texto a voz (text-to-speech). El chatbot utiliza el modelo GPT-4o de OpenAI para generar respuestas inteligentes y naturales en catalán o castellano, adaptándose a las necesidades de las personas mayores.

## Características

- **Conversación Natural**: Interactúa con el asistente usando el micrófono y recibe respuestas por voz.
- **Reconocimiento de Voz**: Convierte tu voz en texto utilizando una API de reconocimiento de voz.
- **Conversión de Texto a Voz**: Las respuestas del asistente se convierten automáticamente en audio.

## Requisitos

- Clave de API de OpenAI con acceso al modelo GPT-4.
- Conexión a Internet para acceder a los servicios de OpenAI y reconocimiento de voz.
- Micrófono para interactuar con el asistente.
- Python 3.8 o superior.

## Instalación

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local:

1. **Clona este repositorio** en tu máquina local:

    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. **Instala las dependencias necesarias**:

    ```bash
    pip install -r requirements.txt
    ```

    El archivo `requirements.txt` incluye las siguientes bibliotecas:

    ```plaintext
    os-sys
    time
    speechrecognition
    openai
    pygame
    keyboard
    langchain-openai
    langchain-core
    ```

3. **Configura tu clave de API de OpenAI** como una variable de entorno:

    ```bash
    export OPENAI_API_KEY="tu_clave_api"
    ```

    Reemplaza `"tu_clave_api"` con tu clave de API real de OpenAI.

## Ejecución del Programa

1. **Ejecuta el programa**:

    ```bash
    python chatbot_speech2text_text2speech.py
    ```

2. **Interacción con el Asistente**:

   - Usa el micrófono para hablar con el asistente. El chatbot reconocerá tu voz, convertirá tu discurso a texto, generará una respuesta utilizando el modelo GPT-4, y luego la convertirá en audio para que la escuches.
   - Presiona la letra 'e' en tu teclado para que el asistente empiece a escucharte, y presiona 'e' de nuevo cuando hayas terminado de hablar para que el asistente te responda.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal.
- **API de OpenAI GPT-4**: Para generar respuestas basadas en inteligencia artificial.
- **SpeechRecognition**: Para convertir el discurso en texto.
- **Pygame**: Para la reproducción de audio.
- **Keyboard**: Para detectar eventos de teclado.
- **LangChain**: Para manejar la conversación y la gestión de historial de mensajes.
