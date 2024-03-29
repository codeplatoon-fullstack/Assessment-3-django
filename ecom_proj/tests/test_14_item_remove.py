from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from cart_app.models import Cart_item
import json


"""
This test will send a post request to signup to first create a new user and 
acquire the token provided in the response. Then it will set the token under the 
AUTHORIZATION HEADER of the next request where the APIView will utilize TokenAuthentication
to authenticate the user.

The client will send a series of POST requests to the endpoint with the name of "an_item" to build
the clients cart. 

The client will send a DELETE request to the endpoint with the name of "delete_item" and the number 2 
as the cart_item_id. This will delete the Cart_item with the ID of 2

The client will send a GET request to the endpoint with the name of "cart" to see their updated cart items 
and price.
This endpoint must return the following Response status code of 200
"""
answer = {
    "cart_items": [
        {
            "id": 1,
            "item": {
                "id": 10,
                "category": "Other",
                "name": "Wireless Keyboard and Mouse",
                "price": "20.03",
            },
            "quantity": 1,
        },
        {
            "id": 3,
            "item": {
                "id": 3,
                "category": "Electronics",
                "name": "Lenovo ThinkPad",
                "price": "200.30",
            },
            "quantity": 1,
        },
        {
            "id": 4,
            "item": {
                "id": 5,
                "category": "Books",
                "name": "Cracking the Coding Interview",
                "price": "30.27",
            },
            "quantity": 1,
        },
    ],
    "total_price": 250.6,
}
"""
in order to pass the test. Pay attention to order and formatting of your data.
"""


class Test_item_remove(APITestCase):
    fixtures = ["items.json"]

    def test_14_item_remove(self):
        client = Client()
        sign_up_response = client.post(
            reverse("signup"),
            data={"email": "fr@fr.com", "password": "fr"},
            content_type="application/json",
        )
        response_body = json.loads(sign_up_response.content)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response_body['token']}")
        self.client.post(reverse("an_item", args=[10]))
        self.client.post(reverse("an_item", args=[9]))
        self.client.post(reverse("an_item", args=[3]))
        self.client.post(reverse("an_item", args=[5]))
        self.client.delete(reverse("delete_item", args=[2]))
        response = self.client.get(reverse("cart"))
        # print(response.content)
        with self.subTest():
            self.assertTrue(response.status_code == 200 and len(Cart_item.objects.all()) == 3)
        self.assertEqual(json.loads(response.content), answer)
