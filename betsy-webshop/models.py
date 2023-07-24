# Models go here
from peewee import *

# Initialize the database
database = SqliteDatabase('betsy.db')

# Define the base model class
class BaseModel(Model):
    class Meta:
        database = database

# Define the User model. 
class User(BaseModel):
    name = CharField()
    address = TextField()  # multi-line address strings
    billing_information = TextField()  # multi-line billing information strings

# Define the Product model. 
class Product(BaseModel):
    name = CharField()
    description = TextField()
    price_per_unit = DecimalField(decimal_places=2) 
    quantity = IntegerField()

    # Establish a one-to-many relationship between User and Product
    owner = ForeignKeyField(User, backref='products')

# Define the Tag model. 
class Tag(BaseModel):
    name = CharField(unique=True)  
    # Establish a many-to-many relationship between Product and Tag
    product = ManyToManyField(Product, backref='tags')

# Create a through model for the many-to-many relationship between Product and Tag
ProductTag = Tag.product.get_through_model()

# Define the Transaction model.
class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref='purchases')
    product = ForeignKeyField(Product, backref='sales')
    quantity = IntegerField()

# Create the actual tables
def create_tables():
    with database:
        database.create_tables([User, Product, Tag, ProductTag, Transaction])

# Execute the function create_tables
create_tables()
