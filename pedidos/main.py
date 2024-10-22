from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import router
import db_redis


@asynccontextmanager
async def lifespan(app: FastAPI):       
    try:                         
        db_redis.start_threads()
        print("FastAPI started", flush=True)
        yield
    finally:        
        print("FastAPI shutdown", flush=True) 

app = FastAPI(
    description="Sencilla aplicación de gestión de pedidos de fármacos",
    version="0.1.0",
    title="Máster EOI Digital Business - API REST Pedidos de fármacos",
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
                        "name": "pedidos",
                        "description": "Operaciones sobre pedidos",
                    }                     
                ],
    lifespan=lifespan
)     

app.include_router(router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# APM
apm = make_apm_client({
'SERVICE_NAME': 'fastapi-pedidos',
'DEBUG': True,
'SERVER_URL': 'http://apm-server:8200',
'CAPTURE_HEADERS': True,
'CAPTURE_BODY': 'all'
})
app.add_middleware(ElasticAPM, client=apm)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    print(f"Caputando HTTPException motivo {exc.detail}")
    apm.capture_exception()
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,exc: RequestValidationError):
    detail = "{}".format(str([i for i in exc.errors()][0]['msg']) + ": " + str([i for i in exc.errors()][0]['loc']))
    print(f"Caputando RequestValidationError motivo {detail}")
    apm.capture_exception()
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": detail})

@app.exception_handler(ValidationError)
async def validationerror_exception_handler(request: Request,exc: ValidationError):
    detail = "{}".format(str([i for i in exc.errors()][0]['msg']) + ": " + str([i for i in exc.errors()][0]['loc']))
    print(f"Caputando ValidationError motivo {detail}")
    apm.capture_exception()
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": detail})


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):    
    print(f"Caputando Exception {exc}")
    apm.capture_exception()
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": repr(exc)})
