from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt

# От пользователя получаем одно из этих значений:
# 1. VPN subscription URI <-- и парсим саму подписку целиком
# 2. VLESS URI
# 3. JSON файл, содержащий саму стратегию для VPN
# Конвертируем всё в единый формат, валидируем входные данные
# через pydantic модель

# TODO: флаг для использования конкретного json файла
# с подпиской, например (пока только наброски):
#   vless-vpn-cli s -j strategy.json 
# и/или:
#   vless-vpn-cli set --json strategy.json

class Strategy(BaseModel):

    # Temporarily set, used to tell Pydantic to ignore
    # validation check for unknown fields (if presented)
    # TODO: explicitly validate input according to model fields
    model_config = ConfigDict(extra="allow") # <-- FIXME
    
    uuid: str
    address: str
    port: NonNegativeInt

    encryption: str = "none"
    network_type: str = Field(alias="type", default="tcp")
    security: str = "none"

    # tls / reality
    server_name: str | None = Field(alias="sni", default=None)
    public_key: str | None = Field(alias="pbk", default=None)
    fingerprint: str | None = Field(alias="fp", default=None)
    short_id: str | None = Field(alias="sid", default=None)
    flow: str | None = None # <-- if network_type is tcp

    # ws / httpupgrade / xhttp
    path: str | None = None
    host_header: str | None = Field(alias="host", default=None)

    #  grpc
    service_name: str | None = Field(alias="serviceName", default=None)

    # label / fragment
    label: str | None = Field(alias="fragment", default=None)
