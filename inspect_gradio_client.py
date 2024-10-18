import gradio_client
from gradio_client import Client
import inspect
import urllib.parse

class CustomClient(Client):
    def __init__(self, src, *args, **kwargs):
        print("Entering CustomClient.__init__")
        try:
            # Set basic attributes
            self.src = src
            print(f"self.src: {self.src}")
            self.api_prefix = "/api/v1/"
            print(f"self.api_prefix: {self.api_prefix}")
            self.src_prefixed = urllib.parse.urljoin(self.src, self.api_prefix).rstrip("/") + "/"
            print(f"self.src_prefixed: {self.src_prefixed}")

            # Set other attributes from parent class
            self.hf_token = kwargs.get('hf_token', False)
            self.max_workers = kwargs.get('max_workers', 40)
            self.verbose = kwargs.get('verbose', True)
            self.auth = kwargs.get('auth', None)
            self.httpx_kwargs = kwargs.get('httpx_kwargs', None)
            self.headers = kwargs.get('headers', None)
            self.download_files = kwargs.get('download_files', '/tmp/gradio')
            self.ssl_verify = kwargs.get('ssl_verify', True)

            # Now call _get_config
            self.config = self._get_config()

            # Complete initialization with parent class
            super().__init__(src, *args, **kwargs)
            print("CustomClient.__init__ completed")
        except Exception as e:
            print(f"Error in CustomClient.__init__: {str(e)}")
            raise

    def _get_config(self):
        print("Entering _get_config method")
        try:
            print(f"self.src: {self.src}")
            print(f"self.api_prefix: {self.api_prefix}")
            print(f"self.src_prefixed: {self.src_prefixed}")

            config = super()._get_config()

            print("Config retrieved successfully")
            print(f"Config: {config}")

            return config
        except Exception as e:
            print(f"Error in _get_config: {str(e)}")
            print("Exception details:")
            for frame in inspect.trace():
                print(f"File: {frame.filename}, Line: {frame.lineno}")
                print(f"Function: {frame.function}")
                print(f"Code: {frame.code_context[0].strip() if frame.code_context else 'N/A'}")
                print("---")
            raise

def inspect_client():
    print("Contents of gradio_client module:")
    print(dir(gradio_client))

    print("\nContents of gradio_client.exceptions module:")
    print(dir(gradio_client.exceptions))

    print("\nInspecting Gradio Client class:")
    print("Attributes and methods:")
    for attr in dir(Client):
        if not attr.startswith("__"):
            print(f"- {attr}")

    print("\nTrying to create a CustomClient instance:")
    try:
        print("Initializing CustomClient...")

        # Pre-initialization
        print("Pre-initialization:")
        print(f"CustomClient.__init__ parameters: {inspect.signature(CustomClient.__init__)}")

        # Client creation
        client = CustomClient("https://869b55c94cf0750550.gradio.live/")
        print("CustomClient instance created successfully")

        # Post-initialization
        print("\nPost-initialization:")
        print(f"src: {client.src}")
        print(f"hf_token: {client.hf_token}")
        print(f"space_id: {client.space_id}")

        # Before _get_config
        print("\nBefore _get_config:")
        print(f"ssl_verify: {client.ssl_verify}")
        print(f"headers: {client.headers}")

        # After _get_config
        print("\nAfter _get_config:")
        print(f"config: {client.config}")
        print(f"protocol: {client.protocol}")
        print(f"api_prefix: {client.api_prefix}")
        print(f"src_prefixed: {client.src_prefixed}")

        # Final Client attributes
        print("\nFinal CustomClient instance attributes:")
        for attr in dir(client):
            if not attr.startswith("__"):
                value = getattr(client, attr)
                if not callable(value):
                    print(f"- {attr}: {value}")
                else:
                    print(f"- {attr}: <callable>")
    except Exception as e:
        print(f"Error creating CustomClient instance: {str(e)}")
        print("Exception details:")
        for frame in inspect.trace():
            print(f"File: {frame.filename}, Line: {frame.lineno}")
            print(f"Function: {frame.function}")
            print(f"Code: {frame.code_context[0].strip() if frame.code_context else 'N/A'}")
            print("---")

if __name__ == "__main__":
    inspect_client()
