from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v2.endpoints import products
from app.core.config import settings
from app.core.db import create_db_and_tables

# Função de evento que cia as tableas no banco ao iniciar a API
def startup_event():
    create_db_and_tables()
    
app = FastAPI(
    title="Arda Games Affiliate API", 
    description="API para Marktplace de Afiliados da Arda Games - MVP",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Adiciona o evento de startup para criar as tabelas
app.add_event_handler("startup", startup_event)

# CORS Middleware para conectar o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["htt://localhost:3000", "http://127.0.0.1:3000"],  # Permitir todas as origens (ajuste conforme necessário)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Inclui as rotas de produtos
app.include_router(
    products.router, 
    prefix="/api/v2/products", 
    tags=["Products"]
)

@app.get("/")
def root():
    return {
        "message": "Arda Games API - MVP funcionando!",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/")
def health_check():
    return {"status": "ok", "service": "arda_games"}