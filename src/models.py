from typing import Optional, Union, List
from pydantic import BaseModel, Field


## Base result object
# ----------------
class Result(BaseModel):
    content: object = Field(None)
    prompt: object = Field(None)
    response: object = Field(None)
    usage: object = Field(None)


# ----------------


## CONTENT TYPE ENUM for HTML transformation
# ----------------
class ContentType:
    HTML = "html"
    TEXT = "text"
    MARKDOWN = "markdown"


# ----------------


## RECIPE SCHEMA
# ----------------
class IngredientItem(BaseModel):
    item: str = Field(
        None,
        description="Name of the ingredient (e.g., 'All-purpose flour', 'Fresh basil')",
    )
    amount: Optional[float] = Field(
        None,
        description="Numerical quantity of the ingredient. Leave empty for 'to taste' items",
    )
    unit: Optional[str] = Field(
        None,
        description="Unit of measurement (e.g., 'g', 'cups', 'tbsp'). Leave empty for countable items",
    )


class InstructionStep(BaseModel):
    description: str = Field(
        None,
        description="Clear, actionable description of what to do in this step",
        example="Whisk together flour and salt in a large bowl until well combined",
    )


class Recipe(BaseModel):
    title: str = Field(
        None, description="Name of the recipe", example="Classic Chocolate Chip Cookies"
    )
    ingredients: List[IngredientItem] = Field(
        ...,
        description="List of all ingredients needed for the recipe, including optional garnishes",
    )
    instructions: List[InstructionStep] = Field(
        ..., description="Step-by-step preparation instructions in chronological order"
    )


# ----------------
