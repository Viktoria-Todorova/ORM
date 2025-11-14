import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
# Create queries within functions
from main_app.models import Profile, Product, Order
from django.db.models import Q, F, Count

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
    if last_product is None:
        return ''
    product = last_product.products.all().order_by('name')


    return f'Last sold products: {", ".join(p.name for p in product)}'


# def get_last_sold_products():
#     try:
#         last_order = Order.objects.prefetch_related('products').latest('creation_date')
#         last_sold_products = last_order.products.all().order_by('name')
#
#         if last_sold_products:
#             last_sold_products_str = ", ".join(product.name for product in last_sold_products)
#             return f"Last sold products: {last_sold_products_str}"
#         return ""
#     except Order.DoesNotExist:
#         return ""
def get_top_products():
    products = Product.objects.annotate(count_products = Count('products_ordered')).order_by('-count_products','name')[:5]

    final_text = ["Top products:"]
    for p in products:
        final_text.append(f'{p.name}, sold {p.count_products} times')

    return '\n'.join(final_text) if final_text else ''
# print(get_top_products())
def apply_discounts():
    order = Order.objects.annotate(num_of_products= Count('products')).filter(is_completed=False,num_of_products__gt=2)
    if not order:
        num_of_updated_orders =0
    num_of_updated_orders = order.count()
    order.update(total_price = F('total_price') +0.1 )
    return f"Discount applied to {num_of_updated_orders} orders."
# print(apply_discounts())

def complete_order():
    last_product = Order.objects.prefetch_related('products').filter(is_completed=False).order_by('creation_date').first()

    if not last_product:
        return ""
    for p in last_product.products.all():
        p.in_stock = F('in_stock') - 1
        p.save(update_fields=['in_stock'])

        p.refresh_from_db(fields=['in_stock'])
        if p.in_stock == 0:
            p.is_available = False
            p.save(update_fields=['is_available'])

    last_product.is_completed = True
    last_product.save(update_fields=['is_completed'])

    return f"Order has been completed!"
# print(complete_order())


