import os


import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from decimal import Decimal
from main_app.models import Profile, Product, Order
from django.db.models import Q,Count


# # Create queries within functions
# def populate_db():
#     adam = Profile.objects.create(
#         full_name="Adam Smith",
#         email="adam.smith@example.com",
#         phone_number="123456789",
#         address="123 Main St, Springfield",
#         is_active=True,
#     )
#
#     susan = Profile.objects.create(
#         full_name="Susan James",
#         email="susan.james@example.com",
#         phone_number="987654321",
#         address="456 Elm St, Metropolis",
#         is_active=True,
#     )
#
#     # --- Create Products ---
#     desk = Product.objects.create(
#         name="Desk M",
#         description="A medium-sized office desk",
#         price=Decimal("150.00"),
#         in_stock=10,
#         is_available=True,
#     )
#
#     display = Product.objects.create(
#         name="Display DL",
#         description="A 24-inch HD display",
#         price=Decimal("200.00"),
#         in_stock=5,
#         is_available=True,
#     )
#
#     printer = Product.objects.create(
#         name="Printer Br PM",
#         description="A high-speed printer",
#         price=Decimal("300.00"),
#         in_stock=3,
#         is_available=True,
#     )
#
#     # --- Create Orders ---
#     # Order 1: Adam Smith - Desk M + Display DL = $350.00, not completed
#     order1 = Order.objects.create(
#         profile=adam,
#         total_price=Decimal("350.00"),
#         is_completed=False,
#     )
#     order1.products.add(desk, display)
#
#     # Order 2: Adam Smith - Printer Br PM = $300.00, completed
#     order2 = Order.objects.create(
#         profile=adam,
#         total_price=Decimal("300.00"),
#         is_completed=True,
#     )
#     order2.products.add(printer)
#
#     # Order 3: Adam Smith - Desk M + Display DL + Printer Br PM = $650.00, not completed
#     order3 = Order.objects.create(
#         profile=adam,
#         total_price=Decimal("650.00"),
#         is_completed=False,
#     )
#     order3.products.add(desk, display, printer)
#
#     # Order 4: Susan James - Desk M + Printer Br PM = $450.00, not completed
#     order4 = Order.objects.create(
#         profile=susan,
#         total_price=Decimal("450.00"),
#         is_completed=False,
#     )
#     order4.products.add(desk, printer)

def get_profiles(search_string=None):
    if search_string is None:
        return ''

    query_name = Q(full_name__icontains=search_string)
    query_email = Q(email__icontains=search_string)
    query_phone = Q(phone_number__icontains=search_string)



    query = query_name | query_email | query_phone

    profile = Profile.objects.annotate(number_of_orders= Count('orders')).filter(query).order_by('full_name')
    final_text = []
    for p in profile:
        final_text.append(f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.number_of_orders}')


    return  '\n'.join(final_text) if final_text else ''

# print(get_profiles('Co'))
# print(get_profiles('9zz'))

def get_loyal_profiles():
    loyal_orders = Profile.objects.get_regular_customers()
    final_text = []
    for p in loyal_orders:
        final_text.append(f'Profile: {p.full_name}, orders: {p.orders_count}')


    return '\n'.join(final_text) if final_text else ''

#print(get_loyal_profiles())
def get_last_sold_products():
    last_product = Order.objects.prefetch_related('products').order_by('-creation_date').first() #todo
    if not last_product:
        return ''
    product = last_product.products.all().order_by('name')

    return f'Last sold products: {', '.join(p.name for p in product)}'

# print(get_last_sold_products())


def get_top_products():
    top_product =...
def apply_discounts():
    ...
def complete_order():
    ...
# print(Profile.objects.get_regular_customers())

# print(get_profiles('Co'))
#
# print(get_profiles('9zz'))
# print(get_loyal_profiles())
# print(get_last_sold_products())