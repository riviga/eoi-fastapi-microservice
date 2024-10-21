from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
import farmacos
import db_postgres
import db_redis

@asynccontextmanager
async def lifespan(app: FastAPI):       
    try:         
        db_postgres.start()        
        db_redis.start_consumer()
        print("FastAPI started", flush=True)
        yield
    finally:        
        print("FastAPI shutdown", flush=True)

app = FastAPI(
    description="Sencilla aplicación de gestión de inventario de fármacos",
    version="0.1.0",
    title="Máster EOI Digital Business - API REST Inventario fármacos",
    contact={
        "name": "Ricardo Vilchez",
        "url": "https://rickandmortyapi.com/",
        "email": "riviga77@gmail.com"
    },
    license_info={
        "name": "GPLv3",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html", 
    }, 
    openapi_tags= [ 
                    {
                        "name": "farmacos",
                        "description": "Operaciones sobre farmacos",
                    }                     
                ],
    lifespan=lifespan
)

app.include_router(farmacos.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# APM
apm = make_apm_client({
'SERVICE_NAME': 'fastapi-farmacos',
'DEBUG': True,
'SERVER_URL': 'http://apm-server:8200',
'CAPTURE_HEADERS': True,
'CAPTURE_BODY': 'all'
})
app.add_middleware(ElasticAPM, client=apm)

