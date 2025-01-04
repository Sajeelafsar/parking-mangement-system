from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Sample data: list of parking spots with car details
parking_spots = [
    {"id": 1, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
    {"id": 2, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
    {"id": 3, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
    {"id": 4, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
    {"id": 5, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
    {"id": 6, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
    {"id": 7, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
    {"id": 8, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
    {"id": 9, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
    {"id": 10, "is_occupied": False, "car_name": None, "number_plate": None, "owner_name": None},
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .container {
            margin-top: 20px;
        }
        h1 {
            margin-bottom: 20px;
            color: #343a40;
        }
        .input-field {
            margin-bottom: 10px;
        }
    </style>
    <title>Sajeel Parking Management System</title>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Parking Management System</h1>
        <table class="table table-bordered table-striped">
            <thead class="thead-dark">
                <tr>
                    <th>Spot ID</th>
                    <th>Status</th>
                    <th>Car Name</th>
                    <th>Number Plate</th>
                    <th>Owner Name</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for spot in spots %}
                <tr>
                    <td>{{ spot.id }}</td>
                    <td>{{ 'Occupied' if spot.is_occupied else 'Available' }}</td>
                    <td>{{ spot.car_name if spot.is_occupied else 'N/A' }}</td>
                    <td>{{ spot.number_plate if spot.is_occupied else 'N/A' }}</td>
                    <td>{{ spot.owner_name if spot.is_occupied else 'N/A' }}</td>
                    <td>
                        {% if not spot.is_occupied %}
                        <div>
                            <input type="text" class="form-control input-field" id="car-name-{{ spot.id }}" placeholder="Car Name">
                            <input type="text" class="form-control input-field" id="number-plate-{{ spot.id }}" placeholder="Number Plate">
                            <input type="text" class="form-control input-field" id="owner-name-{{ spot.id }}" placeholder="Owner Name">
                            <button class="btn btn-success mt-2" onclick="reserveSpot({{ spot.id }})">Reserve</button>
                        </div>
                        {% else %}
                        <button class="btn btn-danger" onclick="releaseSpot({{ spot.id }})">Release</button>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
        function reserveSpot(spotId) {
            const carName = document.getElementById(`car-name-${spotId}`).value;
            const numberPlate = document.getElementById(`number-plate-${spotId}`).value;
            const ownerName = document.getElementById(`owner-name-${spotId}`).value;

            if (!carName || !numberPlate || !ownerName) {
                alert("Please fill in all fields.");
                return;
            }

            fetch(`/spots/reserve/${spotId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ car_name: carName, number_plate: numberPlate, owner_name: ownerName })
            })
            .then(response => response.json())
            .then(data => alert(data.message || data.error))
            .then(() => location.reload());
        }

        function releaseSpot(spotId) {
            fetch(`/spots/release/${spotId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => alert(data.message || data.error))
                .then(() => location.reload());
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Render the main page."""
    return render_template_string(HTML_TEMPLATE, spots=parking_spots)

@app.route('/spots', methods=['GET'])
def get_parking_spots():
    """Get list of parking spots and their status."""
    return jsonify(parking_spots)

@app.route('/spots/<int:spot_id>', methods=['GET'])
def get_spot(spot_id):
    """Get specific parking spot by ID."""
    spot = next((s for s in parking_spots if s['id'] == spot_id), None)
    if spot is not None:
        return jsonify(spot)
    return jsonify({"error": "Spot not found"}), 404

@app.route('/spots/reserve/<int:spot_id>', methods=['POST'])
def reserve_spot(spot_id):
    """Reserve a parking spot with car details."""
    spot = next((s for s in parking_spots if s['id'] == spot_id), None)
    if spot is None:
        return jsonify({"error": "Spot not found"}), 404
    if spot['is_occupied']:
        return jsonify({"error": "Spot is already reserved"}), 400
    
    data = request.get_json()
    car_name = data.get('car_name')
    number_plate = data.get('number_plate')
    owner_name = data.get('owner_name')

    spot['is_occupied'] = True
    spot['car_name'] = car_name
    spot['number_plate'] = number_plate
    spot['owner_name'] = owner_name
    return jsonify({"message": f"Spot {spot_id} reserved successfully for {car_name} ({number_plate})."}), 200

@app.route('/spots/release/<int:spot_id>', methods=['POST'])
def release_spot(spot_id):
    """Release a reserved parking spot."""
    spot = next((s for s in parking_spots if s['id'] == spot_id), None)
    if spot is None:
        return jsonify({"error": "Spot not found"}), 404
    if not spot['is_occupied']:
        return jsonify({"error": "Spot is not reserved"}), 400
    
    spot['is_occupied'] = False
    spot['car_name'] = None  # Clear the car name
    spot['number_plate'] = None  # Clear the number plate
    spot['owner_name'] = None  # Clear the owner name
    return jsonify({"message": f"Spot {spot_id} released successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
