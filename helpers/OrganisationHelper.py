class OrganisationHelper:
    @staticmethod
    def clean_organisation_name(organisation_name: str) -> str:
        return organisation_name.replace(" ", "_")
