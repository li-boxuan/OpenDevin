import json
import os

import pytest
from litellm import completion

script_dir = os.path.dirname(os.path.realpath(__file__))
mock_dir = os.path.join(script_dir, 'mock')


def get_mock_response(kwargs_json):
    # Find mock response based on prompt. Prompts are stored under nested
    # folders under mock folder. If prompt_{id}.json matches `json.dumps(kwargs)`,
    # then the mock response we're looking for is at `resp_{id}.json`.
    for root, _, files in os.walk(mock_dir):
        for file in files:
            if file.startswith('prompt_') and file.endswith('.json'):
                file_path = os.path.join(root, file)
                # Open the prompt file and compare its contents to kwargs_json
                with open(file_path, 'r') as f:
                    file_content = f.read()
                    # TODO: use a more lenient approach, e.g. simple text similarity matching or vector DB
                    if file_content.strip() == kwargs_json.strip():
                        # If a match is found, construct the corresponding response file path
                        resp_file_path = os.path.join(root, f'resp_{file[len("prompt_"): -5]}.json')
                        # Read the response file and return its content
                        with open(resp_file_path, 'r') as resp_file:
                            return json.loads(resp_file.read())


def mock_completion(*args, **kwargs):
    # Convert kwargs to JSON string for comparison
    messages = kwargs.get('messages', [])
    kwargs_json = json.dumps({'messages': messages})
    mock_response = get_mock_response(kwargs_json)
    assert mock_response is not None, 'Mock response for prompt is not found'
    response = completion(**kwargs, mock_response=mock_response)
    return response


@pytest.fixture(autouse=True)
def patch_completion(monkeypatch):
    monkeypatch.setattr('opendevin.llm.llm.litellm_completion', mock_completion)
