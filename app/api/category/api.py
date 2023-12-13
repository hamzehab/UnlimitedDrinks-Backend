from fastapi import APIRouter, HTTPException
from loguru import logger

from app.db.schema import Category

from .models import CategoryCreate, CategoryModel, CategoryUpdate

router = APIRouter()


@router.get("", response_model=list[CategoryModel])
async def get_all_categories():
    try:
        categories = await Category.all().order_by("id")
        logger.info("Retrieved all categories")
        return [CategoryModel(**dict(category)) for category in categories]
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail="Something went wrong")


@router.get("/{category_name}", response_model=bool)
async def does_category_exist(category_name: str):
    category_name = category_name.lower().replace("-", " ")
    try:
        category = await Category.filter(name=category_name)
        if category:
            return True
        else:
            return False
    except Exception:
        logger.error(f"Category: {category_name} does not exist")
        return False


@router.post("/create", response_model=CategoryModel)
async def create_category(category: CategoryCreate):
    try:
        exists = await does_category_exist(category.name)
        if not exists:
            new_category = await Category.create(
                name=category.name, description=category.description
            )

            logger.info(f"{new_category.name} category created successfully")
            return CategoryModel(**dict(new_category))
        else:
            logger.info(f"Category with that name ({category.name}) already exists")
            raise HTTPException(
                status_code=403, detail=f"Category {category.name} already exists"
            )

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{category_id}")
async def delete_category(category_id: int):
    try:
        await Category.get(id=category_id).delete()
        return {"message": "Category deleted successfully"}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/update/{category_id}")
async def update_category(category_id: int, category: CategoryUpdate):
    category.name = category.name.lower()
    try:
        categoryFound = await Category.get(id=category_id)
        if not categoryFound:
            return {"message": "Category with that id does not exist"}

        attributesToUpdate = {
            attr: value for attr, value in category if value is not None and value != ""
        }
        await Category.get(id=category_id).update(**attributesToUpdate)
        updated_category = await Category.get(id=category_id)
        await updated_category.save()

        logger.info(f"Category {update_category.name} has been updated")
        return {
            "message": "Category updated successfully",
        }

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))
