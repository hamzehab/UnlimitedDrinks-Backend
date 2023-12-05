from db.schema import Review
from fastapi import APIRouter, HTTPException
from loguru import logger

from .models import ReviewCreate

router = APIRouter()


@router.get("/rating/{product_id}")
async def filter_reviews_by_rating(product_id: int):
    try:
        totalReviews = await Review.filter(product_id=product_id)
        reviewsByRating = {}

        for review in totalReviews:
            rating_value = int(review.rating)
            if rating_value not in reviewsByRating:
                reviewsByRating[rating_value] = {
                    "reviews": [review],
                    "percentage": round(1 / len(totalReviews) * 100, 2),
                }

            else:
                reviewsByRating[rating_value]["reviews"].append(review)
                reviewsByRating[rating_value]["percentage"] = round(
                    len(reviewsByRating[rating_value]["reviews"])
                    / len(totalReviews)
                    * 100,
                    2,
                )

        return reviewsByRating
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{product_id}/{customer_id}")
async def add_review(product_id: int, customer_id: str, review: ReviewCreate):
    check = await did_customer_leave_review(product_id, customer_id)
    if not check:
        try:
            review.rating = int(review.rating)
            await Review.create(
                **dict(review), customer_id=customer_id, product_id=product_id
            )
            return {"message": "Review added successfully"}
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=404, detail=str(e))
    else:
        raise HTTPException(
            status_code=202, detail="Cannot leave multiple reviews for one item"
        )


@router.get("/{product_id}/{customer_id}")
async def did_customer_leave_review(product_id: int, customer_id: str):
    try:
        await Review.get(product_id=product_id, customer_id=customer_id)
        return True
    except Exception as e:
        logger.error(str(e))
        return False
