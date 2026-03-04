import requests
import langextract as lx
from openai import OpenAI
import json

# Configuración
BASE_URL = "http://localhost:1234/v1"

def obtener_modelos_activos():
    try:
        response = requests.get(f"{BASE_URL}/models")
        return [m["id"] for m in response.json().get("data", [])]
    except:
        return []

def main():
    modelos = obtener_modelos_activos()
    if not modelos:
        print("❌ Servidor de LM Studio no detectado o sin modelos cargados.")
        return

    print("--- Modelos Activos ---")
    for i, m in enumerate(modelos): print(f"[{i}] {m}")
    modelo_id = modelos[int(input("Selecciona el índice: "))]

    # El "Documento" que mencionas
    texto_ejemplo = """
    1. Apple fue fundada por Steve Jobs en California.
    2. Microsoft fue fundada por Bill Gates en Washington.
    3. Amazon fue fundada por Jeff Bezos en Washington.
    4. Tesla fue fundada por Elon Musk en California.
    5. Facebook fue fundada por Mark Zuckerberg en Massachusetts.
    """

    # Definimos el esquema exacto para tu caso
    schema = {
        "fundaciones": [
            {
                "empresa": "string",
                "fundador": "string",
                "lugar": "string"
            }
        ]
    }

    # Configuración del cliente local para la librería
    local_client = OpenAI(base_url=BASE_URL, api_key="lm-studio")

    print(f"\nExtrayendo datos con {modelo_id}...")

    try:
        # Llamada a LangExtract
        results = lx.extract(
            texto_ejemplo,
            schema=schema,
            model=modelo_id,
            client=local_client
        )

        print("\n--- JSON GENERADO (Para tu Base de Datos RAG) ---")
        print(json.dumps(results, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()