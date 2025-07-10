from app.db import Neo4jConnection
from datetime import datetime

class ReviewService:
    def __init__(self):
        self.db = Neo4jConnection()

    def create_review(self, user_id: str, product_id: str, rating: int, comment: str):
        query = """
        MERGE (u:User {id: $user_id})
        MERGE (p:Product {id: $product_id})
        CREATE (r:Review {
            id: randomUUID(),
            rating: $rating,
            comment: $comment,
            created_at: datetime()
        })
        MERGE (u)-[:WROTE]->(r)
        MERGE (r)-[:REVIEWS]->(p)
        RETURN r.id AS review_id, r.rating AS rating, r.comment AS comment, r.created_at AS created_at
        """
        result = self.db.execute_write(query, {
            "user_id": user_id,
            "product_id": product_id,
            "rating": rating,
            "comment": comment
        })

        if result:
            review = result[0]
            review["created_at"] = review["created_at"].isoformat()
            return review
        else:
            return None