import fitz
from openai import OpenAI
import json

# Conexión a tu LM Studio
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def extraer_metadatos_estilo_langextract(pdf_path):
    doc = fitz.open(pdf_path)
    texto = "".join([page.get_text() for page in doc])
    
    # Este es el "Schema" que le pedimos al modelo local
    prompt_sistema = """
    Actúa como un extractor de datos profesional. 
    Analiza el texto y devuelve un JSON estrictamente formateado con:
    {
      "entidades": [{"nombre": "", "tipo": "Empresa/Persona/Lugar"}],
      "temas_clave": [],
      "resumen_ejecutivo": ""
    }
    """

    print(f"--- Procesando {pdf_path} con LM Studio ---")
    
    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Extrae la info de este fragmento:\n\n{texto[:3000]}"}
        ],
        temperature=0.1,
    )

    # Aquí tienes tu información extraída lista para el RAG
    info_extraida = completion.choices[0].message.content
    return info_extraida

# Ejecución
metadatos = extraer_metadatos_estilo_langextract("prueba_langExtract.pdf")
print("Información estructurada para tu base de datos:")
print(metadatos)