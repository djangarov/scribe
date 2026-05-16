from fastapi import FastAPI

from .routers import internal, scribe

app = FastAPI(title='Scribe', version='1.0.0')

app.include_router(internal.router)
app.include_router(scribe.router)
