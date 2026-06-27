# 📚 Book Manager API

API REST para gerenciamento de uma biblioteca pessoal, construída com **FastAPI** e **Python**.

> ⚠️ Este projeto é um projeto de aprendizado. As credenciais de acesso estão disponíveis abaixo para fins de teste.

---

## 🚀 Tecnologias

- [Python 3.14](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic v2](https://docs.pydantic.dev/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Poetry](https://python-poetry.org/)

---

## 📁 Estrutura do Projeto

```
book-manager/
├── .env           # Variáveis de ambiente (credenciais)
├── main.py        # Rotas da API (POST, GET, PUT, DELETE)
├── auth.py        # Autenticação HTTP Basic
├── models.py      # Modelos Pydantic (validação de dados)
└── pyproject.toml # Dependências do projeto
```

---

## ⚙️ Como rodar localmente

**1. Clone o repositório:**
```bash
git clone https://github.com/ilucasoliveira/book-manager.git
cd book-manager
```

**2. Instale as dependências:**
```bash
poetry install
```

**3. Configure o arquivo `.env`:**
```env
MEU_USUARIO=admin
MINHA_SENHA=admin123
```

**4. Inicie o servidor:**
```bash
poetry run fastapi dev main.py
```

**5. Acesse a documentação:**
```
http://127.0.0.1:8000/docs
```

---

## 🔐 Autenticação

A API utiliza **HTTP Basic Auth**. Para testar:

| Campo    | Valor      |
|----------|------------|
| Usuário  | `admin`    |
| Senha    | `admin123` |

---

## 📖 Endpoints

| Método   | Rota                | Descrição                        | Status |
|----------|---------------------|----------------------------------|--------|
| `POST`   | `/adicionar`        | Adiciona um novo livro           | 201    |
| `GET`    | `/`                 | Lista livros com paginação       | 200    |
| `PUT`    | `/atualizar/{id}`   | Atualiza um livro existente      | 200    |
| `DELETE` | `/deletar/{id}`     | Remove um livro da biblioteca    | 204    |

---

## 📝 Exemplo de uso

**Adicionar livro (POST /adicionar):**
```json
{
  "nome": "O Senhor dos Anéis",
  "autor": "J.R.R. Tolkien",
  "ano": 1954,
  "sinopse": "Uma épica jornada pela Terra Média."
}
```

**Resposta:**
```json
{
  "id": 1,
  "nome": "O Senhor Dos Anéis",
  "autor": "J.R.R. Tolkien",
  "ano": 1954,
  "sinopse": "Uma épica jornada pela Terra Média."
}
```

---

## ✨ Funcionalidades

- ✅ CRUD completo de livros
- ✅ Autenticação HTTP Basic com `compare_digest` (proteção contra timing attacks)
- ✅ Validação de dados com Pydantic v2
- ✅ Paginação e ordenação na listagem
- ✅ Verificação de duplicatas no cadastro
- ✅ Variáveis de ambiente com `.env`
- ✅ Documentação automática via Swagger UI

---

## 👨‍💻 Autor

**Lucas de Oliveira**  
[github.com/ilucasoliveira](https://github.com/ilucasoliveira)  
lucasdeoliveira937@gmail.com