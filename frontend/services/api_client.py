import requests

from services.endpoints import *

class APIClient:

    def __init__(self):
        self.base_url = API_BASE_URL

    def upload_document(self, uploaded_file):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type,
            )
        }

        response = requests.post(
            self.base_url + UPLOAD_ENDPOINT,
            files=files,
        )

        response.raise_for_status()

        return response.json()

    def ask_question(self, question):

        response = requests.post(
            self.base_url + CHAT_ENDPOINT,
            json={
                "question": question
            }
        )

        response.raise_for_status()

        return response.json()

    def get_documents(self):
        
        response = requests.get(
            self.base_url + DOCUMENTS_ENDPOINT
        )

        response.raise_for_status()

        return response.json()


    def delete_document(self, document_id):

        response = requests.delete(
            f"{self.base_url}{DOCUMENTS_ENDPOINT}{document_id}"
        )

        response.raise_for_status()

        return response.json()

    def get_statistics(self):

        response = requests.get(
            self.base_url + STATS_ENDPOINT
        )

        response.raise_for_status()

        return response.json()
