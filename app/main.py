from fastapi import FastAPI, Request
import time

from app.db.database import engine
from app.db.init_db import wait_for_db

from app.models import user, product, order, cart, cart_item
from app.routers import auth, products, orders, cart as cart_router

app = FastAPI()

wait_for_db()

user.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)
cart.Base.metadata.create_all(bind=engine)
cart_item.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart_router.router)


# 🔴 MIDDLEWARE
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start
    print(f"{request.method} {request.url} - {duration:.4f}s")

    return response


@app.get("/")
def root():
    return {"msg": "backend running"}