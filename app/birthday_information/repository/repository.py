from typing import Any

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult

class BirthdayRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_birth(self,user_id, input: dict[str, Any]) -> Any:
        payload = {
            "birthday": input["birthday"],
            "birth_time": input["birth_time"],
            "location": input["location"],
            "user_id": ObjectId(user_id)
            
        }
        insert_result: InsertOneResult = self.database["birthdayInformation"].insert_one(payload)
        return insert_result.inserted_id
    def get_inf_by_user_id(self, user_id: str) -> dict | None:
        inf = self.database["birthdayInformation"].find_one(
            {
                "user_id": ObjectId(user_id),
            }
        )
        return inf
    

    def update_birth(self, user_id: str, input: dict[str, Any]) -> UpdateResult:
        filter = {"user_id": ObjectId(user_id)}
        update = {
            "$set": {
                "birthday": input["birthday"],
                "birth_time": input["birth_time"],
                "location": input["location"],
            }
        }
        return self.database["birthdayInformation"].update_one(filter, update)
