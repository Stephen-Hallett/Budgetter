from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .router.accounts import router as AccountRouter
from .router.models import router as ModelRouter
from .router.transactions import router as TransactionRouter
from .router.users import router as UserRouter
from .utils.logger import MyLogger

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = MyLogger().get_logger()

app.include_router(AccountRouter, prefix="/accounts")
app.include_router(TransactionRouter, prefix="/transactions")
app.include_router(UserRouter, prefix="/users")
app.include_router(ModelRouter, prefix="/models")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
