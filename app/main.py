from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api import router
from app.config import close_redis

tags_metadata = [
    {
        "name": "phones",
        "description": "Store and retrieve address records keyed by phone number.",
    }
]

app = FastAPI(
    title="Phone-Address Service",
    description="Microservice for storing and managing phone-address pairs.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.include_router(router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Phone-Address Service</title>
        <meta name="description" content="API for storing and retrieving phone-address pairs." />
        <meta property="og:title" content="Phone-Address Service" />
        <meta property="og:description" content="FastAPI microservice for phone-to-address lookups." />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary" />
        <meta name="twitter:title" content="Phone-Address Service" />
        <meta name="twitter:description" content="FastAPI microservice for phone-to-address lookups." />
    </head>
    <body>
        <main>
            <h1>Phone-Address Service</h1>
            <p>Use the API to store and retrieve addresses keyed by phone number.</p>
            <p>API docs: <a href="/docs">/docs</a></p>
        </main>
    </body>
    </html>
    """
    return HTMLResponse(content=html.strip())


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    await close_redis()
    
