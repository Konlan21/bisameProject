from fastapi import FastAPI
from auth.routes import router as auth_router 
from db.mongo import db 
from products.routes import router as product_router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded



app = FastAPI()


app.include_router(auth_router, prefix='/auth', tags=["Auth"])
app.include_router(product_router, prefix="/products", tags=["Products"])


# Test mongodb connection
@app.get("/ping-mongo")
async def ping_mongo():
    try:
        # List collections to verify connection
        collections = await db.list_collection_names()
        return {"status": "connected", "collections": collections}
    except Exception as e:
        return {"status": "error", "message": str(e)}



limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



