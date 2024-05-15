from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Part codes and their respective details
parts_catalog = {
    "A": {"price": 10.28, "description": "LED Screen"},
    "B": {"price": 24.07, "description": "OLED Screen"},
    "C": {"price": 33.30, "description": "AMOLED Screen"},
    "D": {"price": 25.94, "description": "Wide-Angle Camera"},
    "E": {"price": 32.39, "description": "Ultra-Wide-Angle Camera"},
    "F": {"price": 18.77, "description": "USB-C Port"},
    "G": {"price": 15.13, "description": "Micro-USB Port"},
    "H": {"price": 20.00, "description": "Lightning Port"},
    "I": {"price": 42.31, "description": "Android OS"},
    "J": {"price": 45.00, "description": "iOS OS"},
    "K": {"price": 45.00, "description": "Metallic Body"},
    "L": {"price": 30.00, "description": "Plastic Body"}
}

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    components = data.get('components', [])

    if not components:
        abort(400, description="No components specified.")

    # Validate components and calculate total
    component_types = {'Screen': 0, 'Camera': 0, 'Port': 0, 'OS': 0, 'Body': 0}
    total_price = 0.0
    order_parts = []

    for code in components:
        part = parts_catalog.get(code)

        if not part:
            abort(400, description=f"Invalid component code: {code}")

        part_type = part['description'].split()[1]  # Gets the type from description
        component_types[part_type] += 1
        total_price += part['price']
        order_parts.append(part['description'])

    if any(count != 1 for count in component_types.values()):
        abort(400, description="Invalid order: Ensure exactly one of each component type.")

    order_response = {
        "order_id": "some-id",  # This should be generated uniquely in a real scenario
        "total": round(total_price, 2),
        "parts": order_parts
    }

    return jsonify(order_response), 201

if __name__ == '__main__':
    app.run(debug=True)
