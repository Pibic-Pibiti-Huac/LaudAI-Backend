# LaudAI-Backend

## Como subir a aplicação

1. Baixe o docker engine [link](https://docs.docker.com/engine/install/ubuntu/)
2. Instale o **NVIDIA Container Toolkit** para utilizar a GPU [link](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
3. Baixe o modelo **Qwen3-8B GGUF** e coloque-o em `./model/qwen3-8B-GGUF/`:

```bash
mkdir -p model/qwen3-8B-GGUF
wget https://huggingface.co/Qwen/Qwen3-8B-GGUF/resolve/main/Qwen3-8B-Q4_K_M.gguf -O model/qwen3-8B-GGUF/Qwen3-8B-Q4_K_M.gguf
```

4. Configure o arquivo `.env` na raiz:

```bash
cp .env.example .env
```

5. Coloque as credenciais do Firebase em `laudAI-server/config/firebase/firebase-auth.json` e configure o `laudAI-server/.env`:

```bash
cp laudAI-server/.env.example laudAI-server/.env
```

6. Crie a **rede** utilizada na integração com o Frontend:

```bash
docker network create app-network
```

7. Rode o comando:

```bash
docker compose up --build
```

8. Agora acesse a API em `http://localhost:8001` (a documentação interativa do Swagger fica em `http://localhost:8001/docs` e o health check em `http://localhost:8001/health`)
9. Pronto, o Backend está pronto para uso

**Obs: Comandos que podem ser úteis com docker** 

```bash
docker compose up -d # não mostra os logs no terminal e permite o uso do mesmo.
docker logs fastapi # mostra os logs do servidor FastAPI.
docker logs llamacpp-qwen3-8b # mostra os logs do modelo.
docker compose down # destruir o container.
docker compose down -v # destruir o container e remover o volume de dados salvos/
```

## Estrutura do Projeto

```
.
├── docker-compose.yaml              # Orquestra llama.cpp (Qwen3-8B) + servidor FastAPI
├── .env.example                     # LLAMACPP_BASE_URL e LLAMACPP_API_KEY
├── model/                           # Modelo Qwen3-8B GGUF (não versionado)
│   └── qwen3-8B-GGUF/
│       └── Qwen3-8B-Q4_K_M.gguf     # Arquivo do modelo quantizado
└── laudAI-server/
    ├── app/
    │   ├── main.py                  # Instância FastAPI (root_path /api/v1) + health check
    │   ├── core/
    │   │   ├── config_app.py        # Registro de routers e middleware CORS
    │   │   └── settings.py          # Configurações via Pydantic (variáveis do .env)
    │   ├── routers/
    │   │   └── model_routers.py     # Endpoints de análise, chat, streaming e correção do laudo
    │   ├── schemas/
    │   │   ├── auth_schemas.py      # Tipos de dados do token Firebase (uid, email, role)
    │   │   └── model_schemas.py     # Schemas Pydantic de request/response do modelo
    │   └── services/
    │       ├── auth_service.py      # Inicialização do Firebase + verificação de token Bearer
    │       ├── model_service.py     # Cliente OpenAI compatível com a API do llama.cpp
    │       └── model_util_service.py # Prompts do modelo (critérios, CoT, chat e correção)
    ├── config/
    │   └── firebase/
    │       └── firebase-auth.json   # Credenciais do Firebase (não versionado)
    ├── Dockerfile                   # Imagem do servidor FastAPI (uv + python 3.13)
    ├── pyproject.toml               # Dependências e configuração do projeto (fastapi, firebase-admin, openai)
    └── .env.example                 # PATH_FIREBASE_CREDENTIALS
```

## Integrar com o Frontend 

1. Clonar o Repositório no mesmo local do repositório do Backend

```bash
git clone https://github.com/Pibic-Pibiti-Huac/LaudAI-Frontend.git
```

2. Criar a **rede** entre os dois containers (se ainda não existir)

```bash
docker network create app-network
```

3. Suba o Backend executando `docker compose up --build` na raiz do repositório

4. No Frontend, defina a URL da API no `.env` do app (`laudAI-app/.env`):

```env
VITE_API_URL="http://localhost:8001"
```

5. Suba o Frontend com `docker compose up --build` e acesse o endereço disponibilizado pelo **VITE**
