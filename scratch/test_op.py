from google import genai
import os
import time

client = genai.Client(
    vertexai=True,
    project="automatizacion-475715",
    location="us-central1"
)

# Test with a dummy prompt (or just list operations)
print("Testing operation polling...")
try:
    # We'll try to list recent operations to see if we can 'get' them
    ops = list(client.operations.list())
    if ops:
        op = ops[0]
        print(f"Testing 'get' for operation: {op.name}")
        try:
            op_refreshed = client.operations.get(name=op.name)
            print("✅ 'client.operations.get(name=...)' works!")
        except Exception as e:
            print(f"❌ 'client.operations.get(name=...)' failed: {e}")
            
        try:
            op_refreshed = client.operations.get(op)
            print("✅ 'client.operations.get(op)' works!")
        except Exception as e:
            print(f"❌ 'client.operations.get(op)' failed: {e}")
    else:
        print("No operations found to test.")
except Exception as e:
    print(f"Could not list operations: {e}")
