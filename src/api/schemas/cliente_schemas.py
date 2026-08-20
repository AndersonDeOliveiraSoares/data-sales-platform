from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClienteCreate(BaseModel):
    nome: str
    cpf_cnpj: str
    email: str
    telefone: str | None = None
    endereco: str | None = None
    cidade: str | None = None
    estado: str | None = None
    cep: str | None = None


class ClienteResponse(BaseModel):
    id_cliente: int
    nome: str
    cpf_cnpj: str
    email: str
    telefone: str | None
    endereco: str | None
    cidade: str | None
    estado: str | None
    cep: str | None
    data_cadastro: datetime

class ClienteListResponse(BaseModel):
    items: list[ClienteResponse]
    page: int
    limit: int
    total: int
    pages: int
    model_config = ConfigDict(from_attributes=True)

class ClienteUpdate(BaseModel):
    nome: str
    cpf_cnpj: str
    email: str
    telefone: str | None = None
    endereco: str | None = None
    cidade: str | None = None
    estado: str | None = None
    cep: str | None = None