import hashlib
from faker import Faker
import json
import random
import time
from .. import views
from ..models import Order, Information

# -------------------------
# --- Utility Functions ---
# -------------------------

# Return the hashed JSON and the actual JSON of the given dictionary
def get_item_hash(item):
    item_json = json.dumps(item, sort_keys=True)
    item_hash = hashlib.sha256()
    item_hash.update(item_json.encode())
    return item_hash.hexdigest(), item_json

# Add item_hash to the blockchain and return the block the item_hash was stored in
def add_to_unconfirmed(item_hash):
    views.add_to_unconfirmed(item_hash)
    views.save_blockchain_to_file()
    return -1

# ------------------------
# --- Misc. Generators ---
# ------------------------

# Here we use the 'random' and 'Faker' modules to generate random data for use in tracking

def get_timestamp(previous_timestamp):
    return previous_timestamp + random.randint(5000, 100000)

def generate_address():
    fake = Faker()
    return fake.address().replace("\n", ", ")

# Generate a random delivery method using weighted probabilities
def generate_delivery_method():
    methods = [("truck", 0.5), ("train", 0.2), ("boat/ship", 0.2), ("plane", 0.1)]
    method_val = random.random()
    for method, prob in methods:
        if prob >= method_val:
            return method
        method_val -= prob

# NOTE(brandon) - We may want to give the ability for customers to click on a shipping company and
# see more detailed information about them, in which case we will need some sort of database of companies
def generate_shipping_company():
    fake = Faker()
    return fake.company()

# NOTE(brandon) - Same note as for the shipping company
def generate_qa_company():
    fake = Faker()
    return fake.company()

# Generate a fake temperature based on the product type.
def generate_temperature(product):
    product = product.lower()
    if product == "milk":
        return round(random.uniform(3, 7), 2)
    if product == "yoghurt":
        return round(random.uniform(3, 7), 2)
    if product == "beef":
        return round(random.uniform(0, 5), 2)
    return -1

# Generate a fake quality rating and quality note based on the product type.
def generate_quality(product):

    product = product.lower()
    ratings = {
        "very_bad": {
            "range": [0.0, 3.0],
            "notes": {
                "milk": [
                    "Unhealthy amounts of bacteria were found",
                    "Leaks found in bottles",
                ],
                "yoghurt": [
                    "Algae found in yoghurt storage",
                ],
                "beef": [
                    "Algae found in beef storage"
                ]
            }
        },
        "bad": {
            "range": [3.0, 6.0],
            "notes": {
                "milk": [
                    "Milk hasn't been pasteurised completely",
                ],
                "yoghurt": [
                    "Uneven consistency",
                ],
                "beef": [
                    "Beef has been bruised in travel"
                ]
            }
        },
        "acceptable": {
            "range": [6.0, 8.5],
            "notes": {
                "milk": [
                    "Dents found in bottle",
                ],
                "yoghurt": [
                    "Malformed Containers",
                ],
                "beef": [
                    "Beef fat has been torn"
                ]
            }
        },
        "good": {
            "range": [8.5, 10.0],
            "notes": {
                "milk": [
                    "No issues",
                ],
                "yoghurt": [
                    "No issues",
                ],
                "beef": [
                    "No issues"
                ]
            }
        },
    }

    quality_frequencies = [("very_bad", 0.1), ("bad", 0.2), ("acceptable", 0.3), ("good", 0.4)]
    quality_roll = random.random()
    for quality, quality_prob in quality_frequencies:
        if quality_roll <= quality_prob:
            # Generate the random rating/note using the info in 'ratings'
            rating = round(random.uniform(ratings[quality]["range"][0], ratings[quality]["range"][1]), 1)
            note = random.choice(ratings[quality]["notes"][product])
            break
        quality_roll -= quality_prob

    return rating, note

# -------------------------------------
# --- Main Tracking Info Generators ---
# -------------------------------------

# Generate the next tracking item
def generate_next_item(previous_hash, previous_item_location, previous_state, previous_items, basic_order_info):

    # For each state, give the probabilities that it will be to each other state. This function
    # should never get called with previous_state = "delivered", it is just here for completeness.
    # The probabilities in the entry for each state should add up to 1.
    # NOTE(brandon): If we want to, we can use len(previous_items) to influence these parameters,
    # so that the item is less likely to keep bouncing between delivery stations
    state_transition = {
        "order_placed": [("order_received", 1.0)],
        "order_received": [("sent_to_checkpoint", 0.8), ("sent_to_customer", 0.2)],
        "sent_to_checkpoint": [("arrived_at_checkpoint", 1.0)],
        "arrived_at_checkpoint": [("temperature_check", 0.2), ("quality_check", 0.2), ("temp_and_quality_check", 0.1), ("sent_to_checkpoint", 0.15), ("sent_to_customer", 0.35)],
        "temperature_check": [("sent_to_checkpoint", 0.5), ("sent_to_customer", 0.5)],
        "quality_check": [("sent_to_checkpoint", 0.5), ("sent_to_customer", 0.5)],
        "temp_and_quality_check": [("sent_to_checkpoint", 0.5), ("sent_to_customer", 0.5)],
        "sent_to_customer": [("delivered", 1.0)],
        "delivered": [("delivered", 1.0)],
    }

    # Use the state transition dict to generate the new state
    state_val = random.random()
    for new_state, prob in state_transition[previous_state]:
        if prob >= state_val:
            next_state = new_state
            break
        state_val -= prob
    
    # Create the tracking info
    order_info = {
        "order_id": previous_items[0].order_id,
        "order_state": next_state,
        "time_stamp": get_timestamp(previous_items[len(previous_items) - 1].time_stamp),
        "previous_hash": previous_hash,
        "previous_block_loc": previous_item_location
    }

    # --- Add additional info needed by different states ---

    # When the order is received, add the designated start point
    if next_state == "order_received":
        order_info["location"] = generate_address()

    # When the order is sent, give the location it is being sent from/to, as well as information
    # about shipping. Use the previous tracking item to dictate the starting address
    if next_state == "sent_to_checkpoint" or next_state == "sent_to_customer":
        if (previous_items[len(previous_items) - 1].location != "NULL"):
            order_info["start_location"] = previous_items[len(previous_items) - 1].location
        else:
            order_info["start_location"] = previous_items[len(previous_items) - 1].end_location
        if next_state == "sent_to_checkpoint":
            order_info["end_location"] = generate_address()
        else:
            order_info["end_location"] = basic_order_info.delivery_address
        order_info["delivery_method"] = generate_delivery_method()
        order_info["shipping_company"] = generate_shipping_company()

   
    # NOTE(brandon) - We may also want to add in more shipping info such as truck temperature
    
    # When the order has arrived (or been delivered), we just need the information from the last tracking item
    if next_state == "arrived_at_checkpoint" or next_state == "delivered":
        order_info["start_location"] = previous_items[len(previous_items) - 1].start_location
        order_info["end_location"] = previous_items[len(previous_items) - 1].end_location
        order_info["delivery_method"] = previous_items[len(previous_items) - 1].delivery_method
        order_info["shipping_company"] = previous_items[len(previous_items) - 1].shipping_company
    
    # For a temperature checking station, we use the location from the last tracking item as well
    # as a company that is doing the assessing
    if next_state == "temperature_check":
        order_info["location"] = previous_items[len(previous_items) - 1].end_location
        order_info["temperature"] = generate_temperature(basic_order_info.product_name)
        order_info["qa_company"] = generate_qa_company()

    # Quality checking station is mostly the same as above, but we generate a rating and a note
    if next_state == "quality_check":
        order_info["location"] = previous_items[len(previous_items) - 1].end_location
        order_info["quality_rating"], order_info["quality_note"] = generate_quality(basic_order_info.product_name)
        order_info["qa_company"] = generate_qa_company()

    # Temperature and quality checking station combines the above two
    if next_state == "temp_and_quality_check":
        order_info["location"] = previous_items[len(previous_items) - 1].end_location
        order_info["temperature"] = generate_temperature(basic_order_info.product_name)
        order_info["quality_rating"], order_info["quality_note"] = generate_quality(basic_order_info.product_name)
        order_info["qa_company"] = generate_qa_company()

    return order_info

def add_first_tracking_item(order):

    # The first tracking state will be when the order is placed. This will be used to show a record
    # that the order was placed at a certain time.
    order_place = {
        "order_id": order.id,
        "order_state": "order_placed",
        "time_stamp": get_timestamp(int(time.time())),
        "user": order.user,
        "product_name": order.product_name,
        "producer_name": order.producer_name,
        "quantity": order.quantity,
        "delivery_address": order.delivery_address
    }

    item_hash, hashed_text = get_item_hash(order_place)
    item_location = add_to_unconfirmed(item_hash)

    order_place["hash"] = item_hash
    order_place["hashed_text"] = hashed_text
    order_place["block_loc"] = item_location

    views.add_database(**order_place)

def add_next_tracking_item(order_id):

    basic_order_info = Order.objects.get(id=order_id)
    tracking_items = Information.objects.filter(order_id=order_id).order_by('time_stamp')

    previous_state = tracking_items[len(tracking_items) - 1].order_state
    
    # Don't generate a new item if the order has already been delivered
    if previous_state == "delivered":
        return

    previous_hash = tracking_items[len(tracking_items) - 1].hash
    previous_location = tracking_items[len(tracking_items) - 1].block_loc
    current_item = generate_next_item(previous_hash, previous_location, previous_state, tracking_items, basic_order_info)
    
    item_hash, hashed_text = get_item_hash(current_item)
    item_location = add_to_unconfirmed(item_hash)
    views.broadcast_tx(item_hash)
    current_item["hash"] = item_hash
    current_item["hashed_text"] = hashed_text
    current_item["block_loc"] = item_location
    
    views.add_database(**current_item)
    return current_item["order_state"]

# Continually generate tracking items until the 'delivered' state is reached
def generate_full_tracking(order_id):
    while (add_next_tracking_item(order_id) != "delivered"):
        pass