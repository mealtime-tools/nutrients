import json

from mealtime_nutrients.generate_json import JSON_PATH, render
from mealtime_nutrients.vocabulary import (
    API_FIELDS,
    API_NUTRIENTS,
    CORE_NUTRIENTS,
    NUTRIENTS,
)


def test_committed_json_is_not_stale():
    # Parsed content, not bytes: a formatter may reflow the arrays.
    message = "run: python -m mealtime_nutrients.generate_json"
    assert json.loads(JSON_PATH.read_text()) == json.loads(render()), message


def test_rendered_json_carries_the_wire_vocabulary():
    document = json.loads(render())
    assert document["nutrients"] == list(NUTRIENTS)
    assert document["coreNutrients"] == list(CORE_NUTRIENTS)
    assert document["unit"] == "g"
    assert document["energyUnit"] == "kcal"
    assert document["energyNutrient"] == "kcal"


def test_rendered_json_carries_the_mapping():
    document = json.loads(render())
    assert document["apiNutrients"] == API_NUTRIENTS
    assert document["apiFields"] == API_FIELDS


def test_rendered_json_routes_every_wire_name():
    # The same totality guarantee, checked on what plate actually reads.
    document = json.loads(render())
    routed = set(document["apiNutrients"]) | set(document["apiFields"])
    assert routed == set(document["nutrients"])


def test_render_is_deterministic():
    assert render() == render()
