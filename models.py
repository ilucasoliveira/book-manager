from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class BaseLivro(BaseModel):
    # classe pai criada para evitar repetição dos validators em Livro e UpdateLivro
    @field_validator("nome", check_fields=False) # "check_fields=False" diz ao pydantic "não verifica se o campo existe nessa classe, que ele existirá em quem herdar"
    @classmethod
    def title_nome(cls, v):
        return v.title()
    
    @field_validator("autor", check_fields=False) # "check_fields=False" diz ao pydantic "não verifica se o campo existe nessa classe, que ele existirá em quem herdar"
    @classmethod
    def title_autor(cls, v):
        return v.title()

class Livro(BaseLivro): # herda os validators do BaseLivro
    nome: str=Field(min_length=1, max_length=50, description="Nome do livro")
    autor: str=Field(min_length=1, max_length=50, description="Nome do autor")
    ano: int=Field(ge=1000, le=date.today().year, description="Ano de publicação")
    sinopse: Optional[str]=Field(default=None, max_length=300, description="Sinopse do livro")

class UpdateLivro(BaseLivro): # herda os validators do BaseLivro
    # todos os campos são Optional para permitir atualização parcial
    # Field valida apenas quando o valor é enviado; None é sempre aceito
    nome: Optional[str]=Field(default=None, min_length=1, max_length=50)
    autor: Optional[str]=Field(default=None, min_length=1, max_length=50)
    ano: Optional[int]=Field(default=None, ge=1000, le=date.today().year)
    sinopse: Optional[str]=Field(default=None, max_length=300)

class LivroResponse(BaseModel):
    # modelo de saída separado: documenta o retorno no Swagger e evita vazar dados internos
    id: int
    nome: str
    autor: str
    ano: int
    sinopse: Optional[str] = None

class BibliotecaResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_page: int
    livros: list[LivroResponse] # ajuda na validação e documentação automática do Swagger