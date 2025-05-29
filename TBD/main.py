import asyncio
from agents import Agent, Runner, function_tool
from typing import List, TypedDict


# Define a structure for the order
class PizzaOrder(TypedDict):
    crust: str
    sauce: str
    toppings: List[str]


# Step 0: Take the order
@function_tool
def take_order(request: str) -> PizzaOrder:
    return {
        "crust": "thin",
        "sauce": "tomato basil",
        "toppings": ["mozzarella", "pepperoni", "olives"],
    }

# Step 1: Choose the crust
@function_tool
def choose_crust(order: PizzaOrder) -> str:
    return f"{order['crust']} crust"

# Step 2: Add sauce
@function_tool
def add_sauce(crust: str, order: PizzaOrder) -> str:
    return f"{crust} with {order['sauce']} sauce"

# Step 3: Add toppings
@function_tool
def add_toppings(base: str, order: PizzaOrder) -> str:
    topping_list = ", ".join(order["toppings"])
    return f"{base} topped with {topping_list}"

# Step 4: Bake the pizza
@function_tool
def bake_pizza(prepped_pizza: str, temperature: int = 475, time_minutes: int = 12) -> str:
    return f"Baked {prepped_pizza} at {temperature}°F for {time_minutes} minutes"

# Step 5: Deliver the pizza
@function_tool
def deliver_pizza(final_pizza: str) -> str:
    return f"Your pizza is ready! {final_pizza}. Enjoy your meal! 🍕"

# Agents
order_agent = Agent(
    name="Order Taker Agent",
    instructions="Ask the user for their pizza preferences and return an order with crust, sauce, and toppings.",
    tools=[take_order],
)

crust_agent = Agent(
    name="Crust Agent",
    instructions="Use the order details to prepare the crust.",
    tools=[choose_crust],
)

sauce_agent = Agent(
    name="Sauce Agent",
    instructions="Use the order to add the appropriate sauce.",
    tools=[add_sauce],
)

toppings_agent = Agent(
    name="Toppings Agent",
    instructions="Use the order to add toppings to the pizza.",
    tools=[add_toppings],
)

bake_agent = Agent(
    name="Bake Agent",
    instructions="Bake the pizza.",
    tools=[bake_pizza],
)

delivery_agent = Agent(
    name="Delivery Agent",
    instructions="Deliver the finished pizza and describe it to the user.",
    tools=[deliver_pizza],
)


# Run the assembly line
async def main():
    # Step 0
    order = await Runner.run(order_agent, input="I'd like a thin crust pizza with tomato basil sauce, mozzarella, pepperoni, and olives.")
    order_data = order.function_call.output
    # Step 1
    crust = await Runner.run(crust_agent, input=order_data)
    # Step 2
    sauce = await Runner.run(sauce_agent, input={"crust": crust.final_output, "order": order_data})
    # Step 3
    toppings = await Runner.run(toppings_agent, input={"base": sauce.final_output, "order": order_data})
    # Step 4
    baked = await Runner.run(bake_agent, input=toppings.final_output)
    # Step 5
    delivery = await Runner.run(delivery_agent, input=baked.final_output)

    print(delivery.final_output)


if __name__ == "__main__":
    asyncio.run(main())
