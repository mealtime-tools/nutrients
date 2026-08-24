# nutrients

The nutrient vocabulary and energy constant shared by the mealtime tools
(pantry, recipes, eatout, nutrilog, plate).

A data package. No parsing, no validation, no dependencies, and no domain
logic — those belong in the tools that consume it.

## Install

```sh
uv add mealtime-nutrients
```

## Use

```python
from mealtime_nutrients import API_FIELDS, API_NUTRIENTS, NUTRIENTS

"fiber" in NUTRIENTS          # True — the wire name
API_NUTRIENTS["fiber"]        # "DIETARY_FIBER" — where it goes in the API
API_FIELDS["carbs"]           # "totalCarbohydrate" — a dedicated field
```

## The vocabulary

`NUTRIENTS` holds the **wire names**: the 41 names that appear in the JSON
these tools exchange, per [FORMAT.md](../FORMAT.md). It is not Google Health's
API spelling, because the two disagree — the format says `kcal`, `fat`, `carbs`
and `fiber` where the API says `energy`, `totalFat`, `CARBOHYDRATES` and
`DIETARY_FIBER`. A consumer that imported the API names would still need its
own wire list plus a translation layer.

`CORE_NUTRIENTS` is the four every tool treats as required (`kcal`, `protein`,
`fat`, `carbs`); nutrilog refuses a new entry without them.

Every nutrient is measured in **grams**. Google Health accepts no milligram or
microgram variant, not even for the trace minerals and vitamins whose labels
print mg or µg, so a record holding milligrams holds a figure a thousand times
too large. `ENERGY_NUTRIENT` (`kcal`) is the sole exception and is
kilocalories.

## The mapping

Google Health's nutrition log has two places to put a figure, so the mapping
has two halves:

| | wire → destination | goes to |
|---|---|---|
| `API_NUTRIENTS` | `saturated_fat` → `SATURATED_FAT` | the `nutrients` array |
| `API_FIELDS` | `carbs` → `totalCarbohydrate` | a dedicated log object |

Membership in `API_NUTRIENTS` is what "array-eligible" means. The mapping is
total (every wire name resolves), injective (no two names collide on one
destination), and surjective onto `NUTRIENT_TYPES` minus one documented
exception. Tests pin all three, and there is exactly one wire name per
nutrient — a second spelling would let one item declare the same figure twice.

Only four names are not a plain lowercasing of their destination:

- `kcal` → `energy` field, whose figure goes under a `kcal` key, not `grams`
- `carbs` → `totalCarbohydrate` field
- `fat` → `totalFat` field
- `fiber` → `DIETARY_FIBER` enum member

And one that is, but still surprises: `protein` → `PROTEIN`, a core macro that
nonetheless travels in the array unlike the other three. That asymmetry is
real, and comes from `MealLog.to_api_payload`.

The routing was read off nutrilog, not invented — `MealLog.to_api_payload` for
the split, `cli.STANDARD_NUTRIENTS` and `NutrientType.from_string` for the
non-identity spellings.

### The one unreachable nutrient

`UNREACHABLE_NUTRIENT_TYPES` is `{"CARBOHYDRATES"}`: the only enum member with
no wire name. `carbs` already carries carbohydrate to the dedicated
`totalCarbohydrate` field, and nutrilog matches the core four before consulting
the enum, so accepting `carbohydrates` as a second wire name would let one item
send 25 g to `totalCarbohydrate` **and** another 25 g to the `nutrients` array
— carbohydrate declared twice in one log. An unreachable member is the lesser
problem, because `carbs` still logs the nutrient.

`fat` and `kcal` cannot collide this way: Google Health publishes no total-fat
and no energy member. A test pins that, so a future enum addition cannot
silently reintroduce the double declaration.

The fat breakdowns are **not** this case and should not be "fixed" by symmetry.
`SATURATED_FAT` and its neighbours are subtypes of the `totalFat` field rather
than duplicates of it, and the overlap among them — `unsaturated_fat` covers
the same grams as `monounsaturated_fat` plus `polyunsaturated_fat` — is Google
Health's own, with real labels stating any of the three. All five stay
reachable.

## Energy

`KJ_PER_KCAL` is 4.184, the thermochemical definition. Use `kcal_from_kj` and
`kj_from_kcal` so the direction is unambiguous at the call site; do not
multiply by a rounded reciprocal such as `0.239006`, which disagrees with
`1 / 4.184` in the 7th significant figure.

## nutrients.json

`plate` is JavaScript and cannot import a Python module, so the vocabulary and
the mapping are also committed as `nutrients.json`. Regenerate after editing
the vocabulary:

```sh
uv run python -m mealtime_nutrients.generate_json
```

A test fails if the committed file and the generator disagree.

## Develop

```sh
uv run pytest
uv run ruff check src
```
