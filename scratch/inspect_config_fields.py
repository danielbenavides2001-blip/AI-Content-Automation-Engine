from google.genai import types
import json

config = types.GenerateVideosConfig()
print(f"Fields in GenerateVideosConfig: {config.model_fields.keys()}")
