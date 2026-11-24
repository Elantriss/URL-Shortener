from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from core import encode_base62

app = FastAPI(title= 'URL Shortener API')

_in_memory_store = {}
id_counter = 1

class ShortenRequest(BaseModel):
    target_url: HttpUrl


@app.post('/shorten', status_code=201)
def shorten_url(request: ShortenRequest):
    global id_counter

    current_id = id_counter
    
    short_code = encode_base62(current_id)

    _in_memory_store[short_code] = str(request.target_url)
    
    id_counter += 1
    
    return {'short_code': short_code, 
            'short_url': f'http://localhost:8000/{short_code}', 
            'target_url': str(request.target_url)
        }


def run() -> None:
    """Start the dev server. Entry point for the `uv run api` script."""
    import uvicorn

    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)