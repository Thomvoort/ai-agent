import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise Exception("API key not found.")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    
    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],system_instruction=system_prompt
            ))
            if response.candidates:
                for c in response.candidates:
                    messages.append(c.content)
        except errors.ServerError as e:
            print(f"Response error: {e}")
            
        if response.usage_metadata is None:
            raise RuntimeError("API request failed.")

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        
        function_results = []
        if response.function_calls is not None:
            for fc in response.function_calls:
                # print(f"Calling function: {fc.name}({fc.args})")
                fc_result = call_function(fc, args.verbose)
                if not fc_result.parts:
                    raise Exception("Expected function result to have non-empty parts list.")
                if fc_result.parts[0].function_response is None:
                    raise Exception("Expect function_response to be a FunctionResponse object. Instead, function_response is None.")
                if fc_result.parts[0].function_response.response is None:
                    raise Exception("Expected function_response.response to be function result. Instead, .response is None")
                function_results.append(fc_result.parts[0])
                
                if args.verbose:
                    print(f"-> {fc_result.parts[0].function_response.response}")
        
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print("Response:")
            print(response.text)
            return
    
    print("Program failed to complete task in maximum iterations (20)")
    exit(1)

if __name__ == "__main__":
    main()
