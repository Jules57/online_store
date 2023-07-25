from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        """
        Initialize cart
        :param request:
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # save current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add product to cart or update its quantity.
        :param product: Product object to add it to cart or update it
        :param quantity: optional integer value with product's quantity, default 1
        :param override_quantity: boolean value for replacing or adding new quantity
        :return: None
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark session as 'modified' to guarantee that is has been saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove product from the cart and update cart.
        :param product:
        :return: None
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate products in the cart in a loop and get product from the DB.
        :return: items
        """
        product_ids = self.cart.keys()
        # get Product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Calculate all the products in the cart.
        :return: total quantity of products
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        # delete the cart from the session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
