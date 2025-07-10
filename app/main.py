from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.review_service import ReviewService

app = FastAPI(
    title="Create Review Service",
    description="Microservice to create product reviews using Neo4j and Python",
    version="1.0.0"
)

review_service = ReviewService()

class ReviewRequest(BaseModel):
    user_id: str = Field(..., example="user123")
    product_id: str = Field(..., example="product456")
    rating: int = Field(..., ge=1, le=5, example=4)
    comment: str = Field(..., example="Great toy!")

@app.post("/review/create", summary="Create a new product review")
def create_review(payload: ReviewRequest):
    result = review_service.create_review(
        user_id=payload.user_id,
        product_id=payload.product_id,
        rating=payload.rating,
        comment=payload.comment
    )

    if not result:
        raise HTTPException(status_code=500, detail="Failed to create review")

    return {
        "message": "Review created successfully",
        "data": result
    }
