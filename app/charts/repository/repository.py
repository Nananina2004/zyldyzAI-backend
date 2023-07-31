from typing import Any, Optional

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult

class BirthdayRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_inf_by_user_id(self, user_id: str) -> dict | None:
        inf = self.database["birthdayInformation"].find_one(
            {
                "user_id": ObjectId(user_id),
            }
        )
        return inf
    

    def create_svg(self,user_id, url) -> Any:
        payload = {
            "svg_url": url,
            "user_id": ObjectId(user_id)
            
        }
        insert_result: InsertOneResult = self.database["userNatalCharts"].insert_one(payload)
        return insert_result.inserted_id

    def get_svg_url(self, user_id: str) -> Optional[str]:
        query = {"user_id": ObjectId(user_id)}
        projection = {"_id": 0, "svg_url": 1} 

        result = self.database["userNatalCharts"].find_one(query, projection)

        if result:
            return result.get("svg_url")
        else:
            return None