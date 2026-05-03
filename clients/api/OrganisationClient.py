import requests
from uuid import UUID

from blustorymicroservices.BluStoryAccounts.models.responses.api.organisations.OrganisationNameResponse import (
    OrganisationNameResponse,
)


class OrganisationClient:
    def __init__(self, base_url: str, access_token: str):
        self.base_url = base_url
        self.access_token = access_token

    def get_organisation_name(self, organisation_id: UUID) -> OrganisationNameResponse:
        print(self.access_token, "access token in organisation client")
        response = requests.get(
            f"{self.base_url}/organisations/{organisation_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        response.raise_for_status()

        return OrganisationNameResponse(**response.json())
