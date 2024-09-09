import os
import time
import speech_recognition as sr
import openai
import pygame
import io
import keyboard

# Set environment variables
os.environ["OPENAI_API_KEY"] = "INSERT HERE THE API"

# Importar módulos necesarios de langchain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Inicializar el modelo
model = ChatOpenAI(model="gpt-4o")

# Almacenar historiales de sesión
session_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Obtener o crear un historial de mensajes de chat para un ID de sesión dado."""
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

# Definir la plantilla de prompt
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Ets un assistent que realitza jocs de trivial per a persones grans, en català o castellà, segons la llengua en què et parlin els usuaris. Quan et demanin fer un trivial, el joc constarà d'un nombre específic de preguntes (per exemple, 10 preguntes). Per cada trivial que et demanin has de donar 4 possibles opcions de respostes de la a) a la d). Has de presentar les preguntes d'una en una, esperar la resposta de l'usuari, i donar feedback immediat sobre si la resposta és correcta o incorrecta. Cada vegada que un usuari encerti una pregunta, has de mantenir un recompte del nombre d'encerts i del total de preguntes fetes, i comunicar el progrés en format 'x encertades/x totals' després de cada pregunta. Al final del joc, proporciona un resum del resultat total. Sigues amable, pacient i utilitza un llenguatge clar i senzill per adaptar-te a les necessitats de les persones grans."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Crear una cadena para el procesamiento
chat_chain = prompt_template | model
chat_with_history = RunnableWithMessageHistory(chat_chain, get_session_history)

# Configuración para la sesión
config = {"configurable": {"session_id": "1"}}

# Función para convertir texto a audio
def text_to_speech_stream(text):
    try:
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        
        # Convert the audio content to a byte stream
        audio_stream = io.BytesIO(response.content)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load the audio stream and play it
        pygame.mixer.music.load(audio_stream)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

text_intro = "Hola! Sóc un assistent virtual especialitzat en trivials que parla en català i en castellà. Comencem dient la temàtica del trivial i quantes preguntes vols que et faci. Digue'm 'adeu' per sortir."
texto_intro = "¡Hola! Soy un asistente virtual especializado en trivials que habla en catalán y en castellano. Empezamos diciendo la temática del trivial y cuántas preguntas quieres que te haga. Dime 'adiós' para salir."

print("\033[91mAssistant:\033[0m", text_intro)
print("-----------------------------------------")
print("\033[91mAssistant:\033[0m", texto_intro)
print("-----------------------------------------")

text_to_speech_stream(text_intro)
time.sleep(0.5)
text_to_speech_stream(texto_intro)

escoltant = "Presiona la lletra 'e' perquè et pugui escoltar i quan hagis acabat de parlar, prem la lletra 'e' de nou perquè pugui respondre"
escuchando = "Presiona la letra 'e' para que te pueda escuchar y cuando hayas terminado de hablar, presiona la letra 'e' de nuevo para que pueda responder"

# Speech Recognition Setup
r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("\n\033[91mAssistant:\033[0m", escoltant)
        print("-----------------------------------------")
        print("\033[91mAssistant:\033[0m", escuchando)

        text_to_speech_stream(escoltant)
        time.sleep(0.5)
        text_to_speech_stream(escuchando)

        listening = False

        # If letter 'e' is pressed then start listening        
        if keyboard.read_key() == 'e':
            audio = r.listen(source)
            listening = True
            if keyboard.is_pressed('e'):
                continue
    
    try:
        if listening:
            user_input = r.recognize_whisper_api(audio, api_key=os.environ["OPENAI_API_KEY"])      
            print("\n\033[92mYou:\033[0m", user_input)

            if 'adéu' in user_input.lower():
                text_despedida = "Fins aviat!"
                print("\033[91mAssistant:\033[0m", text_despedida)
                text_to_speech_stream(text_despedida)
                # Esperar unos segundos para que se reproduzca el audio
                time.sleep(3)
                break
            elif 'adiós' in user_input.lower():
                texto_despedida = "¡Hasta luego!"
                print("\033[91mAssistant:\033[0m", texto_despedida)
                text_to_speech_stream(texto_despedida)
                time.sleep(3)
                break

            # Obtener la respuesta del modelo
            time_ini = time.time()
            response = chat_with_history.invoke(
                [HumanMessage(content=user_input)],
                config=config,
            )
        
            # Imprimir la respuesta
            print("\033[91mAssistant:\033[0m", response.content)
            time_end = time.time()

            # Convertir la respuesta a audio
            text_to_speech_stream(response.content)
            time_end_speech = time.time()

            # Imprimir el tiempo total
            print(f"\033[94mTotal Time Text Generation:\033[0m {time_end - time_ini}", "s")

            # Imprimir el tiempo total de generación de audio
            print(f"\033[94mTotal Time Audio Generation:\033[0m {time_end_speech - time_end}", "s")
        
        else: 
            continue

    except sr.UnknownValueError:
        print("No se ha entendido lo que has dicho.")
    except sr.RequestError as e:
        print(f"Error con la API de Whisper; {e}")
