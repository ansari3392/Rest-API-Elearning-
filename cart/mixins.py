from rest_framework.exceptions import ValidationError

from cart.models.cart import Cart
from course.models import Course

CART_SESSION_ID = "cart"

class AnonymousCart:
    """ get the session id of user if not exists it will create one """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        # cart = self.session.get('cart')

        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
            # cart = self.session['cart'] = {}
        self.cart = cart

    def __iter__(self):
        course_skus = self.cart.keys()
        courses = Course.objects.filter(sku__in=course_skus)
        cart = self.cart.copy()
        for course in courses:
            cart[course.sku]['course'] = course

        for item in cart.values():
            yield item

    def add_course_to_session(self, course):
        """ will add course sku to the session if not exists """
        course_sku = str(course.sku)
        if course_sku not in self.cart:
            self.cart[course_sku] = {}
        else:
            raise ValidationError(detail={"message": "you have already added to your cart"})
        self.save()

    def remove_course_to_session(self, course):
        """ will remove course form the cart session """
        course_sku = str(course.sku)
        if course_sku not in self.cart:
            raise ValidationError(detail={"message": "course not found"})
        del self.cart[course_sku]
        self.save()

    def save(self):
        """ will inform django that the session has been modified, and it needs to be saved """
        self.session.modified = True

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()


class CartHandler:
    def __init__(self, *args, **kwargs):
        super(CartHandler, self).__init__(*args, **kwargs)

    @classmethod
    def get_user_cart(cls, user):
        """get user's cart
        authenticated get from db
        """
        user = user
        carts = user.carts.filter(step__in=['initial', 'pending']).order_by('-step')
        if carts.exists():
            cart = carts.first()
        else:
            cart = Cart.objects.create(user=user)
        return cart

    @classmethod
    def get_user_anonymous_cart(cls, request):
        """get anonymous user's cart"""
        cart = AnonymousCart(request=request)
        return cart




