import os
from google import genai
from dotenv import load_dotenv

# # 1. Cargar la API Key
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# # 2. Configurar el cliente oficial
# client = genai.Client(api_key=api_key)

# def probar_conexion():
#     print("--- Probando conexión con Gemini ---")
#     try:
#         # Intentamos una respuesta simple
#         response = client.models.generate_content(
#             model="gemini-2.0-flash", 
#             contents="Hola, responde solo con la palabra: FUNCIONA"
#         )
        
#         print(f"Respuesta del modelo: {response.text}")
        
#     except Exception as e:
#         print(f"Error de conexión: {e}")
#         print("\nCosas a revisar:")
#         print("1. ¿Tu API Key en el archivo .env es correcta?")
#         print("2. ¿Tienes instalada la librería 'google-genai'?")

# if __name__ == "__main__":
#     probar_conexion()
# 1. Cargar la API Key
load_dotenv()
api_key = os.getenv("#####")

# 2. Configurar el cliente oficial
client = genai.Client(api_key=api_key)

def probar_conexion():
    print("--- Probando conexión con Gemini ---")
    try:
        # Intentamos una respuesta simple
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Hola, responde solo con la palabra: FUNCIONA"
        )
        
        print(f"Respuesta del modelo: {response.text}")
        
    except Exception as e:
        print(f"Error de conexión: {e}")
        print("\nCosas a revisar:")
        print("1. ¿Tu API Key en el archivo .env es correcta?")
        print("2. ¿Tienes instalada la librería 'google-genai'?")

if __name__ == "__main__":
    probar_conexion()