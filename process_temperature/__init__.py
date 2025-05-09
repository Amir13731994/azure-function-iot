import logging
import azure.functions as func
import json
import os
from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError
from azure.digitaltwins.core.models import JsonPatchOperation

TWIN_ID = "Room5015"
PROPERTY_NAME = "temperature"
adt_instance_url = os.environ["ADT_SERVICE_URL"]

def main(event: func.EventHubEvent):
    logging.info("IoT Hub trigger received an event.")

    try:
        body = event.get_body().decode('utf-8')
        message = json.loads(body)
        logging.info(f"Meddelande från IoT: {message}")

        temperature = message.get("temperature")
        if temperature is None:
            logging.warning("Ingen 'temperature' hittades i meddelandet.")
            return

        credential = DefaultAzureCredential()
        client = DigitalTwinsClient(adt_instance_url, credential)

        patch = [
            JsonPatchOperation(
                op="replace",
                path=f"/{PROPERTY_NAME}",
                value=temperature
            )
        ]

        client.update_digital_twin(TWIN_ID, patch)
        logging.info(f"Uppdaterade twin '{TWIN_ID}' med {PROPERTY_NAME} = {temperature}")

    except Exception as e:
        logging.error(f"Fel: {e}")
