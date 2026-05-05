# Safety Boundaries

This project is a RuneScape 3 planning assistant, not a gameplay automation tool.

## Allowed

The project may:

- fetch public RuneScape account data
- fetch public market data
- read user-provided JSON profile data
- calculate method eligibility and conservative profit estimates
- generate checklists and daily plans
- ask OpenAI to rank methods and explain tradeoffs

## Not allowed

The project must not:

- control the RuneScape client
- send clicks, taps, keyboard input, or gestures
- automate skilling, combat, trading, banking, or GE actions
- scrape screen pixels to make gameplay decisions
- bypass or modify the official client
- communicate directly with game worlds
- store user passwords or account credentials
- commit OpenAI API keys or secrets

## Design rule

Every output should be phrased as advice for the user to perform manually.

Good:

```text
Consider doing Method A for 45 minutes, then sell Item B if the price is above X.
```

Bad:

```text
Click here, wait 3 seconds, repeat until inventory is full.
```

## Confidence rule

If a field is missing or an API fails, the advisor should report uncertainty instead of assuming.

Example:

```json
{
  "quests": {
    "source": "runemetrics_quests",
    "status": "failed",
    "confidence": "low",
    "fallback": "manual_profile"
  }
}
```
