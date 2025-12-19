# main.py
from dotenv import load_dotenv
load_dotenv()
from ucloud_sandbox.code_interpreter import Sandbox
import time

# Import for logs API
from e2b.connection_config import ConnectionConfig
from e2b.api.client_sync import get_api_client
from e2b.api.client.api.sandboxes import get_sandboxes_sandbox_id_logs

# Run code

sbx = Sandbox.create(template="code-interpreter-v1",timeout=30) # By default the sandbox is alive for 5 minutes
# sbx = Sandbox.create(template="mcp-gateway",timeout=3600) # By default the sandbox is alive for 5 minutes
# sbx.set_timeout(120)
# time.sleep(10)
# sbx = Sandbox.connect(sandbox_id="ixnn3woo2qt8etsgcbgc2")
info = sbx.get_info()
print("sandbox info:",info)

# # time.sleep(10)
# files = sbx.files.list("/etc")
# print(files)
execution = sbx.commands.run("echo 'hello!'")
print(execution)

sbx.kill()
# # List sandbox
# paginator = Sandbox.list()
# firstPage = paginator.next_items()

# running_sandbox = firstPage[0]

# print('Running sandbox metadata:', running_sandbox.metadata)
# print('Running sandbox id:', running_sandbox.sandbox_id)
# print('Running sandbox started at:', running_sandbox.started_at)
# print('Running sandbox template id:', running_sandbox.template_id)

# # Get the next page of sandboxes
# nextPage = paginator.next_items()

