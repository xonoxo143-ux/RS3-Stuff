# Method Catalog Guide

`data/method_catalog.json` is the controlled source of money-making methods.

The advisor should not invent full methods from scratch. It may suggest candidates, but durable methods should be added to the catalog after review.

## Method object

```json
{
  "id": "unique_method_id",
  "name": "Human-readable method name",
  "category": "skilling | combat | daily | processing | liquidation | market",
  "required_skills": {
    "skill_name": 1
  },
  "required_quests": [],
  "required_unlocks": [],
  "inputs": [],
  "outputs": [],
  "attention": "low | medium | high",
  "mobile_friendliness": "low | medium | high",
  "market_risk": "low | medium | high",
  "setup_cost_gp": 0,
  "notes": "Short explanation."
}
```

## Requirements

Use requirements conservatively.

If a method is much better with an unlock but technically possible without it, separate required and recommended data later.

Example:

```json
{
  "required_unlocks": [],
  "recommended_unlocks": ["grace_of_the_elves"]
}
```

## Inputs and outputs

Inputs and outputs should eventually use item IDs, not just names.

Example:

```json
{
  "inputs": [
    { "item_id": 123, "name": "Input item", "qty": 1 }
  ],
  "outputs": [
    { "item_id": 456, "name": "Output item", "qty": 1 }
  ]
}
```

## Profit estimates

Do not hardcode optimistic gp/hr as truth.

Profit should be calculated from:

- live/recent prices
- item quantities
- conservative rates
- safety margins
- market risk
- user actual-results log

Risk margins:

```text
low market risk: subtract 3-5%
medium market risk: subtract 8-12%
high market risk: subtract 15-25%
```

## Mobile friendliness

Mobile friendliness should matter because this project is intended for practical use, not theoretical desktop efficiency.

High mobile friendliness:

- simple loop
- low UI pressure
- low precision clicking
- low death risk

Low mobile friendliness:

- many menu actions
- rapid banking
- heavy boss mechanics
- high precision input
- frequent price checking

## Catalog status

The starter catalog is intentionally tiny. Expand only after the API/context layer works.
