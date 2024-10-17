from gradio_client import Client

def view_gradio_api():
    client = Client('https://d016ac7f0067803207.gradio.live')
    api_info = client.view_api(return_format='dict')
    print(api_info)

if __name__ == "__main__":
    view_gradio_api()
