import pymongo

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["clinic_db"]
        self.clinics = self.db["clinics"]
        self.users = self.db["users"]  # New: Users collection
        self.states = self.db['states_cities']
        self.recommendations = self.db['recommendations']
        self.contact_infos = self.db['contact_infos']
        

    def get_clinics_collection(self):
        return self.clinics

    def get_users_collection(self):  # New
        return self.users
    
    def get_states_collection(self):
        return self.states
    
    def get_recommendations_collection(self):
        return self.recommendations
    
    def get_contact_infos_collection(self):
        return self.contact_infos

# Singleton instance
db = Database()