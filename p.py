import fitz  # PyMuPDF
import langextract as lx
import os
from dotenv import load_dotenv

# 1. Configuración
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 2. Definir el esquema de lo que queremos extraer
# LangExtract usa ejemplos para "entrenar" al modelo sobre la marcha
schema_prompt = "Extrae los nombres de las empresas y las personas clave mencionadas en el documento."

examples = [
    lx.ExampleData(
        text="Apple fue fundada por Steve Jobs en California.",
        extractions=[
            {"entidad": "Apple", "tipo": "Empresa"},
            {"entidad": "Steve Jobs", "tipo": "Persona"}
        ]
    )
]

def run_extraction(pdf_path):
    full_text = extract_text_from_pdf(pdf_path)
    
    # Creamos el extractor
    # Nota: Por defecto usa Gemini si detecta la API Key
    extractor = lx.Extractor(
        prompt=schema_prompt,
        examples=examples,
        model="gemini-2.0-flash" # O el modelo que prefieras
    )

    # 3. Ejecutar la magia
    results = extractor.extract(full_text)
    
    for item in results:
        print(f"Encontrado: {item.data} | Texto original: '{item.text_segment}'")

# Prueba con un archivo
run_extraction("prueba_langExtract.pdf")