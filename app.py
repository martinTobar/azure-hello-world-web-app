from flask import Flask
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import pyodbc, struct
from azure import identity
import os
import logging
app = Flask(__name__)

connection_string = os.getenv("AZURE_SQL_CONNECTIONSTRING")
# Set the logging level for the Azure Identity library
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
#logging.basicConfig(level=logging.INFO)
logger.info('Started')
logger.error("Starting with error debug dont get scared")
# Direct logging output to stdout. Without adding a handler,
# no logging output is visible.

def get_conn():
    logger.info('\n==========================================\n')
    if "WEBSITE_INSTANCE_ID" in os.environ:
        logger.info("Running in Azure App Service")
        # DefaultAzureCredential will automatically use the Managed Identity in Azure App Service
        credential = DefaultAzureCredential()
    else:
        logger.info("Running locally")
        credential =  identity.DefaultAzureCredential(exclude_interactive_browser_credential=True)
    logger.info('\n==========================================\n')   
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string)#, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

def get_persons():
    rows = []
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT TOP (1000) * FROM [dbo].[MyTestPersonTable]")

        for row in cursor.fetchall():
            print(row)
            rows.append(row)

        print(cursor.description)
        rows.append(cursor.description)
    return str(rows)

@app.route('/')
def hello_world():

    return f'Hello, World! my name is Martin from Azure,{os.getenv("CATCHPHRASE")}'

@app.route('/persons')
def hello_peeps():
    return get_persons()
#f'Hello, World! my name is Martin from Azure,{os.getenv("CATCHPHRASE")} '
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
