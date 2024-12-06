import json
import os


def load_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


mock_products_file_path = os.path.join(os.path.dirname(__file__), "mock-products.json")
mock_data = load_json_file(mock_products_file_path)

# Calculate the total price
total_price = sum(product["price"] for product in mock_data)

print(f"Total price: {total_price}")
