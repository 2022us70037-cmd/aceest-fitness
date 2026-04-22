from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
members = []
classes = [
    {"id": 1, "name": "Yoga", "trainer": "Anita", "slots": 10},
    {"id": 2, "name": "Zumba", "trainer": "Raj", "slots": 15},
    {"id": 3, "name": "CrossFit", "trainer": "Mike", "slots": 8},
]

@app.route('/')
def home():
    return jsonify({"message": "Welcome to ACEest Fitness & Gym!", "version": "1.0"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/members', methods=['GET'])
def get_members():
    return jsonify({"members": members, "count": len(members)}), 200

@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email required"}), 400
    member = {
        "id": len(members) + 1,
        "name": data['name'],
        "email": data['email'],
        "plan": data.get('plan', 'basic')
    }
    members.append(member)
    return jsonify({"message": "Member added", "member": member}), 201

@app.route('/classes', methods=['GET'])
def get_classes():
    return jsonify({"classes": classes}), 200

@app.route('/classes/<int:class_id>/book', methods=['POST'])
def book_class(class_id):
    gym_class = next((c for c in classes if c['id'] == class_id), None)
    if not gym_class:
        return jsonify({"error": "Class not found"}), 404
    if gym_class['slots'] <= 0:
        return jsonify({"error": "No slots available"}), 400
    gym_class['slots'] -= 1
    return jsonify({"message": f"Booked {gym_class['name']}!", "remaining_slots": gym_class['slots']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)