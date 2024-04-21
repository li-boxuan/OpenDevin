import subprocess

from opendevin.main import main

import asyncio


def test_write_simple_script():
    # python_command = [
    #     'python', 'opendevin/main.py',
    #     '-i', '10',
    #     '-t', 'Write a shell script "hello.sh" that prints "hello".',
    #     '-d', './'
    # ]
    task = 'Write a shell script "hello.sh" that prints "hello".'
    asyncio.run(main(task))

    # Ensure the 'hello.sh' script is executable
    subprocess.run(['chmod', '+x', 'hello.sh'], check=True)

    # Run the shell script and capture its output
    result = subprocess.run(['bash', 'hello.sh'], text=True, capture_output=True, check=True)

    # Assert that the output is as expected
    assert result.stdout.strip() == 'hello', 'The output of the shell script was not "hello"'
