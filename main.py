import os
import warnings

warnings.filterwarnings("ignore", message=".*EXPERIMENTAL.*")
warnings.filterwarnings("ignore", message=".*InMemoryCredentialService.*")

import dotenv

dotenv.load_dotenv("camila/.env")

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8000"))

from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(
    agents_dir="camila",
    web=True,
    host=host,
    port=port,
)

if __name__ == "__main__":
    import uvicorn
    print(f"\n🌐 CAMILA - Servidor web iniciado")
    print(f"   Abre tu navegador en http://localhost:{port}\n")
    uvicorn.run(app, host=host, port=port, log_level="info")
