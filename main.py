import json
import os
import time
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def main(cell_value):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to config.json relative to the script location
    config_path = os.path.join(script_dir, "config.json")
    prompt_path = os.path.join(script_dir, "system_prompt.txt")

    # Load settings from the configuration file
    with open(config_path, "r") as f:
        config = json.load(f)
        model = config.get("model")
        max_tokens = config.get("max_tokens")
        temperature = config.get("temperature")
        endpoint = config.get("endpoint")
        api_key = config.get("api_key")

    # Load the prompt from a text file
    with open(prompt_path, "r") as f:
        message_prompt_content = f.read()

    # Load the tools from a JSON file
    tools_path = os.path.join(script_dir, "tools.json")
    with open(tools_path, "r") as f:
        tools = json.load(f)

    # Check if the API key is available
    if not api_key:
        raise ValueError("API key not found in configuration file.")

    # Check if the cell_value is null or empty and return null directly
    if cell_value is None or cell_value.strip() == "":
        return None

    # Call prompt values
    system_prompt = {
        "role": "system",
        "content": message_prompt_content
    }
    user_prompt = {
        "role": "user",
        "content": cell_value
    }

    # Set the headers and data for the API request
    auth_header = "Bearer " + api_key
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }

    # Set the POST data
    data = json.dumps({
        "model": model,
        "messages": [system_prompt, user_prompt],
        "tools": tools,
        "tool_choice": "required",
        "max_tokens": max_tokens,
        "temperature": temperature
    })

    # Make the API request
    request = Request(endpoint, data=data.encode('utf-8'), headers=headers)

    # Handle the response
    try:
        response = urlopen(request, timeout=10)
        raw_response = response.read().decode('utf-8')
        response_data = json.loads(raw_response)
        arguments = response_data["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"].replace("\n", "")
        return arguments
    except HTTPError as e:
        return "HTTP Error: " + str(e.code) + " - " + e.read().decode('utf-8')
    except URLError as e:
        return "URL Error: " + str(e.reason)

    # Sleep for a short time to avoid rate limiting
    time.sleep(1)

if __name__ == "__main__":
    try:
        cell_value = sys.argv[1] if len(sys.argv) > 1 else ""
        result = main(cell_value)
        print(result)
    except Exception as e:
        print("Error:", str(e))