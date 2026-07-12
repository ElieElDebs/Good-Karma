from openai import OpenAI
import os


ENDPOINT = os.environ["AZURE_FOUNDRY_ENDPOINTS"]
KEY = os.environ["AZURE_FOUNDRY_API_KEY"]
MODEL_NAME = os.environ["AZURE_FOUNDRY_API_MODEL_NAME"]


CLIENT = None


def init_client() -> OpenAI:
    """
    init the client of the openAI model
    """

    global CLIENT

    if CLIENT is None:
        CLIENT = OpenAI(base_url=ENDPOINT, api_key=KEY)

    return CLIENT


def ask_model(query: str) -> str:
    """
    Send a query to the model to get an answer

    ### args :
        - query (str) : The query to send to the model

    ### Return :
        Return the answer of the model
    """
    global CLIENT
    global MODEL_NAME

    if CLIENT is None or MODEL_NAME is None:
        print("ERROR: OPEN AI CLIENT OR MODEL NAME IS NOT DEFINE")
        print(f"CLIENT = {CLIENT} \n\n MODEL_NAME = {MODEL_NAME}")
        return None

    message: str = query

    response = CLIENT.responses.create(
        model=MODEL_NAME,
        input=message,
    )

    return response.output
