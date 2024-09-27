import uvicorn
from pyngrok import ngrok

# Start ngrok tunnel

ngrok.set_auth_token("2mbnW70OX8zOEkqiL4p9j1IXsRC_7U824K8AdkFMhNm4cxSH9")


public_url = ngrok.connect(8000)
print(f"ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:8000\"")

# Start FastAPI application
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")