from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.schemas.cart import AddToCart
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

def get_user_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.post("/cart/add")
def add_to_cart(
    data: AddToCart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = get_user_cart(db, current_user.id)

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id
    ).first()

    if item:
        item.quantity += data.quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        db.add(item)

    db.commit()
    return {"msg": "added to cart"}


@router.get("/cart")
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = get_user_cart(db, current_user.id)

    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    return [
        {"product_id": i.product_id, "quantity": i.quantity}
        for i in items
    ]


@router.delete("/cart/remove/{product_id}")
def remove_item(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = get_user_cart(db, current_user.id)

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"msg": "removed"}