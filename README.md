# skills

Hermes Agent skills published by snav.

## Install

```bash
hermes skills install simpolism/skills/astrology
hermes skills install simpolism/skills/human-design
```

## Skills

- **astrology** — Compute and interpret astrological charts (natal, synastry, transit) from birth date/time/place. Returns dense, LLM-readable chart text (signs, houses, aspects, dignities, dispositor trees, aspect patterns) via a hosted endpoint, plus chart2ai's reading conventions (the Rule of Truth + standard/professional/mystical voices). Pure Python stdlib client — no Node, no install, OS-neutral.
- **human-design** — Compute and interpret Human Design bodygraphs (Type, Strategy, Authority, Profile, Incarnation Cross, centers, channels, gates), single or two-person partnership. Same hosted endpoint, same pure-stdlib client.

Both call the same hosted endpoint (`simple-astro-api`, which wraps Swiss Ephemeris + chart2txt server-side), so there is nothing to run locally and no build step.
