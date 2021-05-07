import crud
import model

def get_subtotal(cart):
    """Retrieves cart items and adds up prices"""

    # Cart format: {image_id: [name, price, img_url]}
    subtotal = sum([item_data[1] for item_data in cart.values()])

    return subtotal