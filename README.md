
# OpenRefine API Integration Script

This repository contains a Python script that integrates with the OpenAI API to process data from OpenRefine. The script reads a cell value, builds a prompt, and sends a request to the OpenAI API based on configuration settings provided in a JSON file. The response, containing processed arguments, is returned diectly to OpenRefine in the new added column. 

## Features

- Reads configuration settings (API key, model, max tokens, temperature, and endpoint) from a JSON file (`config.json`).
- Loads a custom system prompt from a text file (`system_prompt.txt`).
- Supports external tools specified in a `tools.json` file.
- Automatically handles errors and returns them in a readable format.
- Includes timeout and rate-limiting mechanisms.

## Prerequisites

- Python 3.6+
- An OpenAI API key
- OpenRefine (optional, if integrating with OpenRefine)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/openrefine-api-integration.git
    cd openrefine-api-integration
    ```

2. Install any necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create the required configuration files:

    - `config.json`: Contains API and model configurations.
    - `system_prompt.txt`: Contains the custom system prompt text.
    - `tools.json`: Lists the tools to be included in the request.

    Example `config.json`:

    ```json
    {
      "model": "gpt-4",
      "max_tokens": 500,
      "temperature": 0,
      "endpoint": "https://api.openai.com/v1/chat/completions",
      "api_key": "your_openai_api_key"
    }
    ```

## Usage with OpenRefine

To use this script within OpenRefine, you can execute it by calling a subprocess from OpenRefine’s Python/Jython environment. This approach passes the current cell’s value to the Python script and returns the API’s response.

1. Choose Edit column → Add column based on this column.

2. In the expressions editor window, select "Clojure & Jython" as epxression language.

3. Run this code in OpenRefine

```python
import subprocess

return subprocess.check_output(["/path/to/python", "/path/to/main.py", value.encode("utf-8")])
```

- Adjust "/path/to/python" to the location of your Python executor and "/path/to/main.py" to the path of the main script (main.py).

### Parameters

- **cell_value**: The value of the cell to be processed by the script.

### Configuration

Modify the settings in `config.json` to specify:

- `model`: The model to use for the API call.
- `max_tokens`: The maximum tokens to generate in the API response.
- `temperature`: Controls the creativity of the response.
- `endpoint`: The API endpoint URL.
- `api_key`: Your OpenAI API key (required).

### Example Files

- **system_prompt.txt**: Contains the system prompt text, which sets the context for API requests.
- **tools.json**: Defines external tools available to the model.

## Error Handling

The script handles potential errors, including:

- **HTTP Errors**: Displays the HTTP status code and message if the API request fails.
- **URL Errors**: Handles issues with connecting to the API endpoint.
- **Rate Limiting**: Includes a sleep delay to avoid exceeding API rate limits.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.