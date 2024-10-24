# EOI Master Digital Business 

A simple microservices system to manage a drug inventory and place orders for them.
- Microservice Frontend web: React + Typescript + Vite
- Microservice Inventory: FastAPI + Postgres
- Microservice Orders: FastAPI + MongoDB

Async communication between Inventory and Orders: Redis Streams


## How to run with Docker Compose
1. Create .env file with keys 
    - Postgres: POSTGRES_USER, POSTGRES_PASSWORD y POSTGRES_DB
    - Redis Streams: REDIS_STREAM_PENDING, REDIS_STREAM_COMPLETE, REDIS_STREAM_REFUND
2. Run `docker-compose up -d`
