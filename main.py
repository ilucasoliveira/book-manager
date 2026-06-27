import math
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import HTTPBasicCredentials
from typing import Literal
from auth import autenticar_usuario
from models import Livro, UpdateLivro, LivroResponse, BibliotecaResponse

biblioteca = {}

app = FastAPI(
    title="Gerenciador de Livros",
    description="API para gerenciamento de uma biblioteca pessoal com autenticação básica.",
    version="1.0.0",
    contact={
        "name":"Lucas de Oliveira",
        "email":"lucasdeoliveira937@gmail.com"
    }
)

@app.post("/adicionar", status_code=201, response_model=LivroResponse)
# status_code=201 é a semântica correta para criação de recurso
def create_livro(livro: Livro, credentials: HTTPBasicCredentials=Depends(autenticar_usuario)):
    if any(i["nome"] == livro.nome for i in biblioteca.values()): # .values() para comparar os dados, não as chaves
        raise HTTPException(status_code=409, detail="Livro já existente na biblioteca.")
    
    novo_id = max(biblioteca.keys(), default=0) + 1 # gera ID incremental; default=0 garante que funciona com biblioteca vazia
    
    biblioteca[novo_id] = livro.model_dump()
    return {"id": novo_id, **livro.model_dump()} # ** "explode" o dicionário, exibindo os pares chave-valor

@app.get("/", response_model=BibliotecaResponse)
# GET não precisa de status_code= pois 200 OK é o padrão
def read_livro(
    page: int=Query(default=1, ge=1, description="Número de página"),
    limit: int=Query(default=10, ge=10, le=100, description="Itens por página"),
    ordenar: Literal["nome", "autor", "ano"]=Query(default='nome', description="Campo de ordenação"), # Literal já rejeita valor inválido com 422
    credentials: HTTPBasicCredentials=Depends(autenticar_usuario)):
    
    if not biblioteca:
        return {"page": page, "limit": limit, "total": 0, "total_page": 0, "livros": []}
    
    livros_ordenado = sorted(biblioteca.items(), key=lambda item:item[1][ordenar])
    
    start = (page - 1) * limit # índice inicial da página
    end = start + limit        # índice final da página
    
    livros_paginados = [
        {"id": id, "nome": livro_data["nome"], "autor": livro_data["autor"], "ano": livro_data["ano"], "sinopse": livro_data["sinopse"]}
        for id, livro_data in livros_ordenado[start:end]
    ]
    
    return {
        "page": page,
        "limit": limit,
        "total": len(biblioteca),
        "total_page": math.ceil(len(biblioteca) / limit), # .ceil() arredonda sempre para cima; dividir por limit, não por 2
        "livros": livros_paginados
    }

@app.put("/atualizar/{id}", status_code=200, response_model=LivroResponse)
# status_code=200 com o objeto atualizado no body é mais informativo que 204
def update_livro(id: int, novo_livro: UpdateLivro,credentials: HTTPBasicCredentials=Depends(autenticar_usuario)):
    if id not in biblioteca: # validar antes de usar o dado
        raise HTTPException(status_code=404, detail="ID não encontrado.")
    
    livro = biblioteca.get(id)
    
    # atualiza apenas os campos enviados; campos None são ignorados
    if novo_livro.nome is not None:
        livro["nome"] = novo_livro.nome
    if novo_livro.autor is not None:
        livro["autor"] = novo_livro.autor
    if novo_livro.ano is not None:
        livro["ano"] = novo_livro.ano
    if novo_livro.sinopse is not None:
        livro["sinopse"] = novo_livro.sinopse
    
    biblioteca[id] = livro
    return{"id": id, **livro} # livro já é um dict, não precisa de .model_dump()

@app.delete("/deletar/{id}", status_code=204)
# status_code=204 (No Content) é o mais semântico para delete: operação concluída, sem body de retorno
def delete_livro(id: int, credentials: HTTPBasicCredentials=Depends(autenticar_usuario)):
    if id not in biblioteca:
        raise HTTPException(status_code=404, detail="ID não encontrado.")
    
    del biblioteca[id]