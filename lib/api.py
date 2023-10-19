from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# MongoDB Connection
client = MongoClient("mongodb://matric-mongo-1:27017/")
db = client["onboarding_db"]

class Onboarding:
    def __init__(self, db_url="mongodb://mongodb:27017/", db_name="onboarding_db"):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.access_technologies = self.db['access_technologies']

    def register(self, technology_name, description, version):
        """Register a new access technology."""
        if self._validate_input(technology_name, description, version):
            if self.access_technologies.find_one({"name": technology_name}):
                print(f"Access Technology '{technology_name}' is already registered.")
                return False
            else:
                technology_data = {
                    'name': technology_name,
                    'description': description,
                    'version': version
                }
                self.access_technologies.insert_one(technology_data)
                self._acknowledge_registration(technology_name)
                return True
        else:
            print("Validation failed.")
            return False

    def _validate_input(self, technology_name, description, version):
        """Validate technology details. (For simplicity, just checking if fields are not empty)"""
        return bool(technology_name) and bool(description) and bool(version)

    def _acknowledge_registration(self, technology_name):
        """Acknowledge the registration of the new access technology."""
        print(f"Access Technology '{technology_name}' has been successfully registered.")

# Initialize the Onboarding class
ob = Onboarding(db_url="mongodb://matric-mongo-1:27017/", db_name="onboarding_db")

@app.route('/access_technologies', methods=['GET'])
def get_access_technologies():
    technologies = list(db.access_technologies.find({}, {"_id": 0}))  # Excluding _id field for simplicity
    return jsonify(technologies)

@app.route('/register_technology', methods=['POST'])
def register_technology():
    try:
        # Extract the details from the request's JSON body
        data = request.json
        name = data["name"]
        description = data["description"]
        version = data["version"]

        # Use the register method from the Onboarding class
        success = ob.register(name, description, version)
        if success:
            return jsonify({"status": "success", "message": "Technology registered successfully!"}), 201
        else:
            return jsonify({"status": "error", "message": "Failed to register technology. It may already exist."}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
