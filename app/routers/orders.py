from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.order import Order
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()


def process_order(order_id: int):
    import time
    time.sleep(2)
    print(f"Order {order_id} processed")


@router.post("/orders")
def create_order(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(status_code=400, detail="Cart empty")

    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    if not items:
        raise HTTPException(status_code=400, detail="Cart empty")

    total = 0

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        total += product.price * item.quantity

    order = Order(user_id=current_user.id, total_price=total)
    db.add(order)

    for item in items:
        db.delete(item)

    db.commit()

    # 🔴 BACKGROUND TASK
    background_tasks.add_task(process_order, order.id)

    return {"msg": "order created", "total": total}