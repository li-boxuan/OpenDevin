import os
import asyncio

from opendevin.main import main


def test_write_simple_script():
    task = "Write a shell script 'hello.sh' that prints 'hello'."
    asyncio.run(main(task))
    assert os.path.exists('workspace/hello.sh'), 'The file "hello.sh" does not exist'
