import requests
import json
import sys

def get_response(user_query, model="llama2"):
    """
    Generates a text response by streaming from a local Ollama model.
    Yields each token (chunk) of the response.
    """
    try:
        url = 'http://localhost:11434/api/generate'
        
        data = {
            "model": model,
            "prompt": user_query,
            "stream": True,
            "options": {
                "num_predict": 2048
            }
        }

        # Use stream=True in the requests call
        with requests.post(url, json=data, stream=True) as response:
            response.raise_for_status() # Raise an error for bad responses (4xx, 5xx)
            
            # Iterate over the streaming response line by line
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    
                    # Check if 'response' key exists and yield it
                    if 'response' in chunk:
                        yield chunk['response']
                    
                    # Stop when the 'done' key is True
                    if chunk.get('done', False):
                        break

    except requests.exceptions.ConnectionError:
        error_message = "Connection Error: Could not connect to Ollama server.\n\n" \
                        "Please make sure the Ollama application is running or " \
                        "you have run `ollama serve` in your terminal."
        print(error_message, file=sys.stderr)
        yield error_message
        
    except requests.exceptions.RequestException as e:
        error_message = f"An HTTP error occurred: {str(e)}"
        if e.response and e.response.status_code == 404:
             error_message = f"Error: Model '{model}' not found by Ollama. " \
                             f"Please run `ollama pull {model}`."
        
        print(error_message, file=sys.stderr)
        yield error_message
        
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        yield error_message