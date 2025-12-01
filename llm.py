from google import genai
from google.genai import types

from config import LLM_MODEL, LLM_PROMPT

def llm(client: genai.Client, input_content: str, verbose: bool = False) -> str:
    try:
        if verbose:
            print(f"Setting LLM client with model and getting response ({LLM_MODEL})")

        response = client.models.generate_content(
            model=LLM_MODEL, 
            contents=input_content,
            config=types.GenerateContentConfig(
                system_instruction=LLM_PROMPT
            ),
        )

        if verbose:
            print("\n---Response---")
            print(response.text)
            print("---------\n")
            print("\n===COST===")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            print("===$$$===\n")

    except Exception as e:
        print(f"\nError: {e}")

    return response.text