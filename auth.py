import os # "operating system": permite interagir com o sistema operacional
from dotenv import load_dotenv # "load_dotenv": vai ler do arquivo .env para o python saber o que há nele
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from secrets import compare_digest # percorre tudo em tempo constante para evitar ataques de timing

load_dotenv() # precisa carregar para ler os valores dentro de .env

security = HTTPBasic()

USUARIO = os.getenv("MEU_USUARIO") # ".getenv": get environment; método do OS para pegar o valor pelo nome no arquivo .env
SENHA = os.getenv("MINHA_SENHA")

def autenticar_usuario(credentials: HTTPBasicCredentials=Depends(security)):
    is_username_correct = compare_digest(credentials.username, USUARIO)
    is_passeword_correct = compare_digest(credentials.password, SENHA)
    
    if not(is_username_correct and is_passeword_correct):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.", headers={"WWW-Authenticate": "Basic"})
    
    return credentials