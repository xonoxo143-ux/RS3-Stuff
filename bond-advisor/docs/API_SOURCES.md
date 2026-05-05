# API Sources

This project should treat APIs as fallible sources. Every fetched value should record source, status, and confidence.

## Core sources

### RS3 Hiscores Lite

Purpose:

- skill ranks
- skill levels
- skill XP
- activity scores where available

Use for requirement checks based on skill levels.

Expected confidence: high when the player appears on the selected hiscores table.

Failure cases:

- player name not found
- player is on a different account mode table
- endpoint format changes

### RuneMetrics profile

Purpose:

- total skill
- total XP
- combat level
- quest count summary
- recent activity if public
- skill values when public

Expected confidence: high if public and valid.

Failure cases:

- profile private
- malformed/empty response
- endpoint unavailable

### RuneMetrics quests

Purpose:

- quest titles
- quest status
- difficulty
- membership flag
- quest point data
- eligibility data where returned

Expected confidence: high if public and valid.

Failure cases:

- endpoint returns empty response
- profile private
- data shape changes

Fallback:

- use `manual_profile.json` unlock flags
- ask user to add missing quest/unlock facts manually

### RuneScape Wiki Prices API

Purpose:

- latest market data
- short-window price averages if available
- item mapping
- price time series if available

Expected confidence: medium-high.

Important limitation:

- price APIs do not guarantee instant buy/sell margin on the Grand Exchange

### Jagex ItemDB

Purpose:

- official guide price
- item detail page data
- historical graph data
- GE update timing

Expected confidence: medium-high.

Important limitation:

- guide prices lag real trade behavior
- low-volume items may be misleading

### RuneScape Wiki / MediaWiki

Purpose:

- item pages
- method requirements
- quest requirements
- skilling formulas
- money-making guide references
- boss/drop information

Expected confidence: medium-high for requirements, medium for gp/hr claims.

## Source tagging pattern

Use this shape in generated context:

```json
{
  "field_name": {
    "value": "example",
    "source": "source_name",
    "status": "available",
    "confidence": "high",
    "notes": []
  }
}
```

## Do not use as core sources

- user login/session-only endpoints
- password-based flows
- screen-reading overlays
- third-party rare-price claims as primary truth
- old/deprecated avatar or ranking endpoints
