from semantic_kernel.functions import kernel_function

class OrderPizzaPlugin:
    def __init__(self):
        self.menu = {
            "margherita": {"name": "margherita", "price": 10},
            "pepperoni": {"name": "pepperoni", "price": 12},
            "vegetarian": {"name": "vegetarian", "price": 11},
            "capricciosa": {"name": "capricciosa", "price": 13}
        }
        self.chart = {"pizzaList": []}

    @kernel_function(description="Get the pizza menu")
    async def get_pizza_menu(self):
        print("get_pizza_menu - Returning the pizza menu.")
        return self.menu

    @kernel_function(
        description="Add a pizza to the user's cart; returns the new item and updated cart"
    )
    async def add_pizza_to_cart(self, pizzaName: str):
        print(f"add_pizza_to_cart - Adding {pizzaName} to your cart.")
        pizza = self.menu[pizzaName]
        self.chart["pizzaList"].append(pizza)
        return pizza

    @kernel_function(
        description="Remove a pizza from the user's cart; returns the updated cart"
    )
    async def remove_pizza_from_cart(self, pizza_id: int):
        print(f"remove_pizza_from_cart - Removing pizza with ID {pizza_id} from your cart.")
        self.chart["pizzaList"].pop(pizza_id)
        return self.chart

    @kernel_function(
        description="Returns the specific details of a pizza in the user's cart; use this instead of relying on previous messages since the cart may have changed since then."
    )
    async def get_pizza_from_cart(self, pizzaName: str):
        print(f"get_pizza_from_cart - Looking for {pizzaName} in your cart.")
        for pizza in self.chart["pizzaList"]:
            if pizza["name"] == pizzaName:
                return pizza

    @kernel_function(
        description="Returns the user's current cart, including the total price and items in the cart."
    )
    async def get_cart(self):
        total = 0
        for pizza in self.chart["pizzaList"]:
            total += pizza["price"]
        print(f"get_cart - Your total is ${total}.")
        return {"total": total, "items": self.chart["pizzaList"]}

    @kernel_function(
        description="Checkouts the user's cart; this function will retrieve the address and the name of the user and complete the order."
    )
    async def checkout(self, address: str, name: str):
        total = 0
        for pizza in self.chart["pizzaList"]:
            total += pizza["price"]
        self.chart["pizzaList"] = []
        
        #print all the informations
        print(f"checkout - Your order has been placed. Your total is ${total}. Your order will be delivered to {address}. Thank you, {name}!")

        return {"total": total}