import fitz  # PyMuPDF
from openai import OpenAI

# 1. Configuración para conectar con LM Studio
# No necesitas API Key real, pero la librería pide una (puedes poner 'lm-studio')
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def extract_text_from_pdf(pdf_path):
    print(f"Leyendo: {pdf_path}...")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def procesar_con_modelo_local(pdf_path):
    texto_pdf = extract_text_from_pdf(pdf_path)
    
    if not texto_pdf.strip():
        print("El PDF parece estar vacío.")
        return

    print("Enviando texto al modelo en LM Studio...")

    # Creamos el prompt para que el modelo se comporte como LangExtract
    prompt_sistema = (
        "Eres un experto en extracción de datos. Tu tarea es leer el texto y "
        "devolver ÚNICAMENTE un objeto JSON con las entidades encontradas "
        "(Empresas, Personas, Fechas)."
    )
    
    try:
        completion = client.chat.completions.create(
            model="google/gemma-3-4b", # LM Studio ignora este nombre y usa el que tengas cargado
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Extrae la información relevante de este texto:\n\n{texto_pdf[:4000]}"} 
            ],
            temperature=0.1, # Baja temperatura para que sea más preciso
        )

        print("\n--- RESPUESTA DEL MODELO LOCAL ---")
        print(completion.choices[0].message.content)

    except Exception as e:
        print(f"Error al conectar con LM Studio: {e}")
        print("¿Te has asegurado de dar a 'Start Server' en LM Studio?")

if __name__ == "__main__":
    # Cambia esto por el nombre de tu archivo real
    procesar_con_modelo_local("prueba_langExtract.pdf")