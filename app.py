from flask import Flask
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    # keyVaultName = 'myKeyVaultForLearning'
    # KVUri = f"https://{keyVaultName}.vault.azure.net"

    # credential = DefaultAzureCredential()
    # client = SecretClient(vault_url=KVUri, credential=credential)

    # retrieved_secret = client.get_secret('mySecret')
    #os.getEnv("CATCHPHRASE")
    return f'Hello, World! my name is Martin from Azure,{os.getenv("CATCHPHRASE")} '
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
hello_world()