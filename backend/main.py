import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.architectures import router as architectures_router
from routes.scrape import router as scrape_router
from settings import LOG_LEVEL

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="Arch-Cloud Backend",
    version="1.0.0",
    openapi_tags=[
        {"name": "Architectures", "description": "List/query parsed architectures"},
        {"name": "Scrape", "description": "Trigger scraping & AI parsing (HTML / GitHub)"},
    ],
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(architectures_router)
app.include_router(scrape_router)
