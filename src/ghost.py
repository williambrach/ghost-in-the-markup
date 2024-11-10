import os
from typing import Callable, Union

from bs4 import BeautifulSoup
from litellm import completion

from src.html import parse_from_file, transform
from src.models import ContentType, Result


# TODO add caching
def extract(
    prompt: str,
    response_object: dict,
    api_key: str,
    base_url: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> dict:
    try:
        response = completion(
            model=model,
            base_url=base_url,
            api_key=api_key,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_object,
        )
        return Result(
            response=response_object.model_validate_json(
                response.choices[0].message.content
            ),
            usage=response.usage,
            content=None,
            prompt=prompt,
        )

    except Exception as e:
        print(e)
        raise ValueError(f"Failed to extract from html: {e}")


def predict(
    html: Union[BeautifulSoup, str],
    prompt: str,
    response_object: dict,
    api_key: str,
    base_url: str,
    model: str = "gpt-4o-mini",
    transformation: ContentType = "html",
) -> Result:
    if html is None:
        raise ValueError(f"html [{type(html)}] must be provided.")

    if (
        not isinstance(html, BeautifulSoup)
        and isinstance(html, str)
        and os.path.exists(html)
    ):
        html = parse_from_file(html)

    content = transform(html, transformation)

    prompt = prompt.format(content=content)

    response = extract(
        prompt=prompt,
        response_object=response_object,
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0
    )
    response.content = content
    return response


def compare(
    true_html: Union[BeautifulSoup, str],
    modified_html: Union[BeautifulSoup, str],
    prompt: str,
    response_object: dict,
    api_key: str,
    base_url: str,
    eval_func: Callable,
    transformation: ContentType = "html",
    model: str = "gpt-4o-mini",
) -> dict:
    true = predict(
        html=true_html,
        prompt=prompt,
        response_object=response_object,
        api_key=api_key,
        base_url=base_url,
        model=model,
        transformation=transformation,
    )
    pred = predict(
        html=modified_html,
        prompt=prompt,
        response_object=response_object,
        api_key=api_key,
        base_url=base_url,
        model=model,
        transformation=transformation,
    )

    return eval_func(true, pred)
