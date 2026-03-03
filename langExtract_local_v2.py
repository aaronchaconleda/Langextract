import json
import os

import fitz  # PyMuPDF
import langextract as lx
import requests

BASE_URL = "http://localhost:1234/v1"
INPUT_CHAR_LIMIT = 5000
MAX_OUTPUT_TOKENS = 80
MAX_CHAR_BUFFER = 2500
OUTPUT_JSON_PATH = "resultado_fundaciones.json"


def obtener_modelos_activos():
    try:
        response = requests.get(f"{BASE_URL}/models", timeout=10)
        response.raise_for_status()
        return [m["id"] for m in response.json().get("data", [])]
    except Exception:
        return []


def extraer_texto_pdf(ruta_pdf):
    if not os.path.exists(ruta_pdf):
        return None
    doc = fitz.open(ruta_pdf)
    return "".join([p.get_text() for p in doc])


def construir_ejemplos():
    return [
        lx.data.ExampleData(
            text="Apple fue fundada por Steve Jobs en California.",
            extractions=[
                lx.data.Extraction(
                    extraction_class="fundacion",
                    extraction_text="Apple fue fundada por Steve Jobs en California",
                    attributes={
                        "empresa": "Apple",
                        "fundador": "Steve Jobs",
                        "lugar": "California",
                    },
                )
            ],
        )
    ]


def main():
    modelos = obtener_modelos_activos()
    if not modelos:
        print("No se detectaron modelos activos en LM Studio.")
        return

    print("\n--- Modelos Activos ---")
    for i, m in enumerate(modelos):
        print(f"[{i}] {m}")
    modelo_id = modelos[int(input("\nSelecciona el indice: "))]

    texto_pdf = extraer_texto_pdf("prueba_langExtract.pdf")
    if not texto_pdf:
        print("No se pudo leer el PDF.")
        return
    texto_pdf = texto_pdf[:INPUT_CHAR_LIMIT]

    prompt_instrucciones = (
        "Extrae eventos de fundacion de empresas. "
        "Para cada evento usa la clase 'fundacion' y llena atributos: "
        "'empresa', 'fundador' y 'lugar'. "
        "Responde solo JSON valido y conciso, sin explicaciones."
    )

    config = lx.factory.ModelConfig(
        model_id=modelo_id,
        provider="openai",
        provider_kwargs={
            "base_url": BASE_URL,
            "api_key": "lm-studio",
            "response_format": {"type": "text"},
            "max_workers": 1,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "temperature": 0,
        },
    )

    print(f"\nProcesando con {modelo_id}...")

    try:
        result = lx.extract(
            texto_pdf,
            prompt_description=prompt_instrucciones,
            examples=construir_ejemplos(),
            config=config,
            use_schema_constraints=False,
            fence_output=True,
            max_char_buffer=MAX_CHAR_BUFFER,
            batch_length=1,
            max_workers=1,
            resolver_params={"suppress_parse_errors": True},
            show_progress=False,
        )

        fundaciones = []
        for ext in (result.extractions or []):
            if ext.extraction_class == "fundacion":
                fundaciones.append(ext.attributes or {})

        salida = {
            "modelo": modelo_id,
            "input_char_limit": INPUT_CHAR_LIMIT,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "fundaciones": fundaciones,
            "total_fundaciones": len(fundaciones),
        }

        with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(salida, f, indent=2, ensure_ascii=False)

        print("\n--- RESULTADO ---")
        print(json.dumps(salida, indent=2, ensure_ascii=False))
        print(f"\nJSON guardado en: {OUTPUT_JSON_PATH}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
