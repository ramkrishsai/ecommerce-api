from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.services.redis_cache import get_cache, set_cache
from app.core.deps import require_admin
from app.models.user import User
import json

router = APIRouter()


@router.post("/products")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)  # 🔴 ADMIN PROTECTED
):
    new = Product(**product.dict())
    db.add(new)
    db.commit()
    return {"msg": "product added"}


@router.get("/products", response_model=list)
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    key = f"products:{skip}:{limit}"

    cached = get_cache(key)
    if cached:
        return json.loads(cached)

    products = db.query(Product).offset(skip).limit(limit).all()
    data = [{"id": p.id, "name": p.name, "price": p.price} for p in products]

    set_cache(key, json.dumps(data))
    return data