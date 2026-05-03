from typing import ClassVar

from pydantic import BaseModel


class RoleSettings(BaseModel):
    operator: ClassVar[str] = "operator"
    member: ClassVar[str] = "member"
    parent: ClassVar[str] = "parent"


class EmailSettings(BaseModel):
    suffix: ClassVar[str] = "@blustory.internal"
    max_length: ClassVar[int] = 254


class OperatorSettings(BaseModel):
    prefix: ClassVar[str] = "BluStoryOps_"


class SupabaseSettings(BaseModel):
    url: str
    service_role_key: str


class DeepLinkSettings(BaseModel):
    scheme: ClassVar[str] = "com.pallondomus.blustoryapp"
    callback: ClassVar[str] = "://auth/callback"
    url: ClassVar[str] = scheme + callback


class InternalClientsSettings(BaseModel):
    organisation_service_url: ClassVar[str] = "http://127.0.0.1:8080"


class Settings(BaseModel):
    supabase: SupabaseSettings
    email: ClassVar[type[EmailSettings]] = EmailSettings
    roles: ClassVar[type[RoleSettings]] = RoleSettings
    deeplink: ClassVar[type[DeepLinkSettings]] = DeepLinkSettings
    operator: ClassVar[type[OperatorSettings]] = OperatorSettings
    internal_clients: ClassVar[type[InternalClientsSettings]] = InternalClientsSettings

    model_config = {"extra": "allow"}
