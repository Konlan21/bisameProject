from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from auth.routes import router as auth_router 
from db.mongo import db 
from products.routes import router as product_router
from rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from affiliate.routes import router as affiliate_router






app = FastAPI()


app.include_router(auth_router, prefix='/auth', tags=["Auth"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(affiliate_router, prefix="/affiliate", tags=["Affiliate"])


# Test mongodb connection
@app.get("/ping-mongo")
async def ping_mongo():
    try:
        # List collections to verify connection
        collections = await db.list_collection_names()
        return {"status": "connected", "collections": collections}
    except Exception as e:
        return {"status": "error", "message": str(e)}



app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

