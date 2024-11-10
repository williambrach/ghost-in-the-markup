from Levenshtein import distance

from src.models import IngredientItem, Result


def eval_recipes(true: Result, pred: Result) -> list[str, float]:
    def format_ingredient(ingredient: IngredientItem) -> str:
        return f"{str(ingredient.amount)} {ingredient.unit} {ingredient.item}".replace(
            "None", ""
        ).strip()

    def compare_lists(true_list: list[str], pred_list: list[str]) -> tuple[bool, float]:
        from statistics import mean

        is_match = len(true_list) == len(pred_list) and all(
            t == p for t, p in zip(true_list, pred_list)
        )
        avg_distance = (
            mean(distance(t, p) for t, p in zip(true_list, pred_list))
            if true_list
            else 0
        )
        return is_match, avg_distance

    true = true.response
    pred = pred.response

    # Compare titles
    scores = {
        "title_match": true.title == pred.title,
        "title_distance": distance(true.title, pred.title),
    }

    # Compare ingredients
    true_ingredients = [format_ingredient(i) for i in true.ingredients]
    pred_ingredients = [format_ingredient(i) for i in pred.ingredients]

    ingredients_match, ingredients_distance = compare_lists(
        true_ingredients, pred_ingredients
    )
    scores.update(
        {
            "ingredients_match": ingredients_match,
            "ingredients_distance": ingredients_distance,
        }
    )

    # Compare instructions
    true_instructions = [i.description for i in true.instructions]
    pred_instructions = [i.description for i in pred.instructions]

    instructions_match, instructions_distance = compare_lists(
        true_instructions, pred_instructions
    )
    scores.update(
        {
            "instructions_match": instructions_match,
            "instructions_distance": instructions_distance,
        }
    )

    return scores
