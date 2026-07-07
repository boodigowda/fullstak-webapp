from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import engine, session
from database_models import Base, Product as DbProduct
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_methods=["*"],
    )

Base.metadata.create_all(bind=engine)

products = [
    Product(id=1,name="laptop", description="A high-performance laptop", price=100, quantity=20),
    Product(id=2,name="bag",description="A stylish bag", price=20, quantity=10),
    Product(id=3,name="pen",description="A fine-tip pen", price=5, quantity=30),
    Product(id=4,name="mobile",description="A latest smartphone", price=300, quantity=2),
    Product(id=5,name="headphones",description="Noise-cancelling headphones", price=150, quantity=5)
]

def get_db():
    db = session()
    try:
        yield db    
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(DbProduct).count
    if count==0:
        for product in products:
            print(product)
            db.add(DbProduct(**product.model_dump()))
    
    db.commit()
init_db()

@app.get("/")
def greet():
    return "Welcome to python programming!"

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(DbProduct).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(DbProduct).filter(DbProduct.id == id).first()
    if db_product == None:
        return "Product not found"
    return db_product

@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(DbProduct(**product.model_dump()))
    db.commit()
    return product

# @app.post("/product")
# def create_product(product: Product):
#     products.append(product)
#     return product

@app.put("/products/{id}")
def update_product_by_id(id: int, product:Product,  db: Session = Depends(get_db)):
    db_product = db.query(DbProduct).filter(DbProduct.id == id).first()
    if db_product:
        db_product.name = product.name,
        db_product.description = product.description,
        db_product.price = product.price,
        db_product.quantity = product.quantity

        db.commit()
    return product

@app.delete("/products/{id}")
def delete_product_by_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(DbProduct).filter(DbProduct.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Delete Successfully"
