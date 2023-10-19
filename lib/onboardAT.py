from pymongo import MongoClient

class Onboarding:
    def __init__(self, db_url="mongodb://localhost:27017/", db_name="onboarding_db"):
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

if __name__ == "__main__":
    # Sample usage:
    ob = Onboarding()
    ob.register("5G", "Fifth generation mobile network", "v1.0")
    ob.register("LTE", "Long-Term Evolution", "v3.2")
