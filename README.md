# LaudAI-Backend

## How to run the application

1. Download Docker Engine [link](https://docs.docker.com/engine/install/ubuntu/)
2. Install the **NVIDIA Container Toolkit** to use the GPU [link](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
3. Download the **Qwen3-8B GGUF** model and place it in `./model/qwen3-8B-GGUF/`:

```bash
mkdir -p model/qwen3-8B-GGUF
cd model/qwen3-8B-GGUF
hf download hf://Qwen/Qwen2.5-7B-Instruct-GGUF/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf --local-dir .
```

4. Configure the `.env` file at the project root:

```bash
cp .env.example .env
```

5. Place the Firebase credentials in `laudAI-server/config/firebase/firebase-auth.json` and configure `laudAI-server/.env`:

```bash
cp laudAI-server/.env.example laudAI-server/.env
```

6. Run the command:

```bash
docker compose up --build -d
```

7. Now access the API at `http://localhost:8001` (the interactive Swagger documentation is available at `http://localhost:8001/docs` and the health check at `http://localhost:8001/health`)
8. Done, the Backend is ready to use

**Note: Docker commands that may be useful**

```bash
docker compose up -d # doesn't show logs in the terminal and frees it up for use.
docker logs fastapi # shows the FastAPI server logs.
docker logs llamacpp-qwen3-8b # shows the model logs.
docker compose down # tear down the container.
docker compose down -v # tear down the container and remove the saved data volume.
```

## Project Structure

```
.
├── docker-compose.yaml              # Orchestrates llama.cpp (Qwen3-8B) + FastAPI server
├── .env.example                     # LLAMACPP_BASE_URL and LLAMACPP_API_KEY
├── model/                           # Qwen3-8B GGUF model (not versioned)
│   └── qwen3-8B-GGUF/
│       └── Qwen3-8B-Q4_K_M.gguf     # Quantized model file
└── laudAI-server/
    ├── app/
    │   ├── main.py                  # FastAPI instance (root_path /api/v1) + health check
    │   ├── core/
    │   │   ├── config_app.py        # Router registration and CORS middleware
    │   │   └── settings.py          # Settings via Pydantic (.env variables)
    │   ├── routers/
    │   │   └── model_routers.py     # Endpoints for analysis, chat, streaming, and report correction
    │   ├── schemas/
    │   │   ├── auth_schemas.py      # Firebase token data types (uid, email, role)
    │   │   └── model_schemas.py     # Pydantic request/response schemas for the model
    │   └── services/
    │       ├── auth_service.py      # Firebase initialization + Bearer token verification
    │       ├── model_service.py     # OpenAI-compatible client for the llama.cpp API
    │       └── model_util_service.py # Model prompts (criteria, CoT, chat, and correction)
    ├── config/
    │   └── firebase/
    │       └── firebase-auth.json   # Firebase credentials (not versioned)
    ├── Dockerfile                   # FastAPI server image (uv + python 3.13)
    ├── pyproject.toml               # Project dependencies and configuration (fastapi, firebase-admin, openai)
    └── .env.example                 # PATH_FIREBASE_CREDENTIALS
```

## Integrating with the Frontend

1. Clone the repository in the same location as the Backend repository

```bash
git clone https://github.com/Pibic-Pibiti-Huac/LaudAI-Frontend.git
```

2. Create the **network** between the two containers (if it doesn't already exist)

```bash
docker network create app-network
```

3. Start the Backend by running `docker compose up --build -d` at the root of the repository

4. In the Frontend, set the API URL in the app's `.env` (`laudAI-app/.env`):

```env
VITE_API_URL="http://localhost:8001"
```

5. Start the Frontend with `docker compose up --build -d` and access the address provided by **VITE**
