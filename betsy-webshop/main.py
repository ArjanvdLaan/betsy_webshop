# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line

from peewee import fn
from models import User, Product, Tag, Transaction

def search(term):
    # Returns products that have the search term in their name
    return Product.select().where(Product.name.contains(fn.Lower(term)))

def list_user_products(user_id):
    # Returns products of a user
    user = User.get_by_id(user_id)
    return user.products

def list_products_per_tag(tag_id):
    # Returns all products for atag
    tag = Tag.get_by_id(tag_id)
    return tag.products

def add_product_to_catalog(user_id, product):
    # Adds a product to a user
    user = User.get_by_id(user_id)
    product.owner = user
    product.save()

def update_stock(product_id, new_quantity):
    # Updates the stock quantity of a product
    product = Product.get_by_id(product_id)
    product.quantity = new_quantity
    product.save()

def purchase_product(product_id, buyer_id, quantity):
    # Handles a purchase between a buyer and a seller for a given product
    product = Product.get_by_id(product_id)
    buyer = User.get_by_id(buyer_id)
    
    # Check if the requested quantity is available
    if product.quantity < quantity:
        raise Exception("Requested quantity is not available")

    # Create a new transaction
    Transaction.create(buyer=buyer, product=product, quantity=quantity)

    # Update the product's stock
    product.quantity -= quantity
    product.save()

def remove_product(product_id):
    # Removes a product from the user
    product = Product.get_by_id(product_id)
    product.delete_instance()

def populate_test_database():
    # create users
    user1 = User.create(name="Alice", address="123 Main Street", billing_information="Visa 1234")
    user2 = User.create(name="Bob", address="456 Market Street", billing_information="MasterCard 5678")

    # create products
    sweater = Product.create(name="Sweater", description="A warm woolen sweater", price_per_unit=50.00, quantity=100, owner=user1)
    hat = Product.create(name="Hat", description="A stylish hat", price_per_unit=20.00, quantity=50, owner=user2)

    # create tags
    winter = Tag.create(name="winter")
    style = Tag.create(name="style")

    # connect products with tags
    winter.product.add([sweater, hat])
    style.product.add(hat)

    # create some transactions
    Transaction.create(buyer=user2, product=sweater, quantity=2)
    Transaction.create(buyer=user1, product=hat, quantity=1)

# Execute the function to populate the test data
populate_test_database()