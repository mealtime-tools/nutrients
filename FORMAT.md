# Food item JSON

Tools exchange one ordinary JSON object. JSON-mode commands wrap it as
`{"ok":true,"data":...}`; `--input` unwraps that envelope.

```json
{
  "name": "Protein bar",
  "grams": 90,
  "kcal": 335,
  "protein": 45.6,
  "fat": 7.9,
  "carbs": 4.9,
  "fiber": 0.9,
  "saturated_fat": 2.1
}
```

Nutrients describe the whole item. `grams` is optional; when it is
absent, the item is the 100 g fallback. There is no serving object or basis
enum.

## Which keys an item carries

`kcal`, `protein`, `carbs` and `fat` are always present. Every other nutrient
is written only when the item states a figure for it.

An absent key and an explicit `null` mean the same thing: nothing is known
about that nutrient. Readers must treat them identically, so a writer is free
to omit rather than spell out a null. Explicit zero is not absence -- it means
a source reported none of it, and it survives as `0`.

Nutrient names come from `mealtime-nutrients`, which mirrors what Google
Health accepts. Every nutrient is grams; energy is `kcal`. Kilojoules are
converted where a source states them and are not a key in this format.

A tool that logs intake may require kcal, protein, fat, and carbs before it
accepts a new entry. Some health backends omit an explicit zero when reading an
entry back, so a tool reading its own writes may render a missing core macro as
zero; nothing in this format infers a nutrient that was never stated.

## Keys this format does not define

A producer may carry its own alongside these: where an item came from, what it
costs today, the barcode the pack prints. A reader ignores any key it does not
recognise rather than refusing the item, which is what lets a producer add one
without a coordinated release.

Two rules for a writer. Such a key is never a nutrient, so nothing here infers
a figure from one. And it is never an identity a reader is expected to honour:
`name` and the nutrients are the whole of what this format promises.

Use `--input FILE|-` everywhere structured input is accepted. A tool that
stores or logs a piped item stores it unchanged and never rescales it: an
item's nutrients describe the weight it states, so changing that weight alone
would relabel them rather than convert them. Ask the producer for the weight
you mean instead.
