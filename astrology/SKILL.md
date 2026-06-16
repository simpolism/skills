---
name: astrology
description: Compute and interpret astrological charts — natal, synastry (two-person compatibility), and transits — from birth date/time/place. Returns dense, LLM-readable chart text (signs, houses, aspects, dignities, dispositor trees, aspect patterns). Use when someone asks for their birth chart, an astrology reading, compatibility between two people, or current transits. Calls a hosted endpoint — no server, no Node, no install; pure Python stdlib. For Human Design, use the human-design skill instead.
when_to_use: User asks for a natal/birth chart, an astrology reading, synastry/compatibility between two people, or current transits. Also when you need precise planetary positions, houses, aspects, dispositor trees, or aspect patterns (stelliums, T-squares, grand trines, yods) for a given moment and place. NOT for Human Design (Type/Strategy/Authority/centers/gates) — that's the separate human-design skill.
---

# Astrology — chart + reading

This skill turns birth data into the dense, structured chart report that `chart2txt`
produces, and gives you the interpretive conventions to read it well. The report is
**data, not a reading** — you compute it, then *you* do the reading in conversation.

## How it works

```
place ──geocode──▶ lat/lng ──Swiss Ephemeris──▶ raw positions ──chart2txt──▶ report text
```

All of this runs **server-side** at a hosted endpoint
(`https://simple-astro-api.netlify.app/api/chart`). The skill ships one small
client, `scripts/chart.py`, that builds the query, calls the endpoint, and prints the
report. It is **pure Python stdlib** — no Node, no npm, no pip, no bash — so it runs
identically on Windows, macOS, and Linux. The endpoint is public and free; no API key.

## Quickstart

```bash
python scripts/chart.py --name "Jake" --date 1990-05-15 --time 14:30 --place "Brooklyn, New York"
```

(Use `python3` if that's what your platform calls it. On Windows, `python scripts\chart.py ...`.)

### Synastry (two people / compatibility)

Add a second person with the `*2` flags. The cross-aspect grid is appended automatically.

```bash
python scripts/chart.py --type synastry \
  --name "A" --date 1990-05-15 --time 14:30 --place "New York, New York" \
  --name2 "B" --date2 1988-11-02 --time2 08:15 --place2 "Los Angeles, California"
```

### Transit (natal chart + current sky)

For transits **right now**, just omit the transit flags — the script defaults the
transit moment to the current UTC date/time (and prints a note saying so):

```bash
python scripts/chart.py --type transit \
  --name "Jake" --date 1990-05-15 --time 14:30 --place "Brooklyn, New York"
```

For a **specific** date (a past or future transit), pass `--transit-date` (and
optionally `--transit-time` / `--transit-place`):

```bash
python scripts/chart.py --type transit \
  --name "Jake" --date 1990-05-15 --time 14:30 --place "Brooklyn, New York" \
  --transit-date 2027-01-01 --transit-time 12:00
```

(The default is UTC-now; the Moon moves ~0.5°/hour, so for a Moon-sensitive
reading pass an explicit `--transit-time` in the user's local zone if precision
matters. Slower planets are unaffected by the hour.)

## Flags

| Flag | Meaning |
|------|---------|
| `--name` / `--date` / `--time` / `--place` | Person 1's birth data. `--date` and `--place` required. |
| `--name2` / `--date2` / `--time2` / `--place2` | Person 2 (synastry). |
| `--time` | `HH:MM` or `HH:MM:SS`, 24-hour, **local time at the birthplace**. |
| `--place` | `"City, State"` (US) or `"City, Country"`. See gotchas. |
| `--type` | `natal` (default), `synastry`, or `transit`. |
| `--house-system` | `P` Placidus, `W` Whole Sign (default), `E` Equal, `O` Porphyry. |
| `--transit-date` / `--transit-time` / `--transit-place` | The "current sky" moment for `--type transit`. **Omit for transits right now** (defaults to UTC-now). Place defaults to person 1's. |
| `--unknown-time` | Birth time unknown: planets only, no Ascendant/houses/angles. |
| `--json` | Print the raw chart object instead of the text report. |

(The endpoint also accepts `--type humandesign`, but for HD use the dedicated
`human-design` skill — it ships the right interpretive framework.)

## Gathering birth data

Ask for any of the three that are missing:

1. **Date** of birth.
2. **Time** of birth (local clock time at the birthplace). The Ascendant and all
   house placements depend on it. If unknown, use `--unknown-time` — you can still
   read sign placements and planet-to-planet aspects, just not houses or rising sign.
3. **Place** of birth (city + state/country).

## The Rule of Truth (read this before interpreting)

This is the single most important interpretive discipline, distilled from Jake's
chart2ai system prompt:

> **Only refer to astrological data present in the provided chart.** Do not infer
> placements or aspects from the birth time, from memory, or from geometric
> assumptions. Do not reference an aspect or pattern that isn't printed in the
> `[ASPECTS]` / aspect-pattern sections. If it's not in the chart text, it is not
> in the chart. Confirm every data-claim against the report before stating it.

The chart report is the *sole* source of astrological fact for the reading. Your
craft is synthesis and meaning, not recall of where planets "usually" are.

## Reading the output

Report sections, in rough order of interpretive weight:

- **[ANGLES]** — Ascendant (rising / self-presentation) and Midheaven (vocation/public role). Known time only.
- **[PLANETS]** — each planet's sign, degree, dignity (Domicile/Detriment/Exaltation/Fall/Ruler), and house. Sun/Moon/Ascendant are the core trio.
- **[DISPOSITOR TREE]** — chains of "who rules whom"; final dispositors and cycles show where the chart's power concentrates.
- **[ELEMENT/MODALITY/POLARITY DISTRIBUTION]** — temperament balance. A heavy or missing element is interpretively loud.
- **[ASPECTS]** — grouped by orb tightness. Tighter = stronger. `applying` intensifies, `separating` wanes.
- **Aspect patterns** — stellium, T-square, grand trine, kite, yod. Only read patterns explicitly listed.
- **[SYNASTRY: A-B]** — cross-aspects between two people's planets; the heart of compatibility work. Lead with the tightest-orb (0–1.5°) contacts.

Lead with the angles + luminaries, then let tight aspects and concentrations of
element/dignity guide what's salient.

## Reading voice (pick a register)

chart2ai offers three voices. Default to **standard** unless the user signals otherwise:

- **Standard** — warm, conversational, accessible. Ground mystical concepts in
  everyday terms ("Venus in the 10th → you may find fulfillment through career or
  public life"). Frame hard aspects as growth/strength, not doom. End by
  highlighting the person's agency: the chart shows patterns, not predetermined
  outcomes.
- **Professional** — precise terminology, references specific degrees/orbs/dignities,
  names interpretive tensions openly, distinguishes well-supported readings from
  ambiguous ones. For an experienced querent or "give me the technical read."
- **Mystical** — archetypal/oracular, planets as characters, patterns as "sacred
  geometries," weaves threads into narrative rather than linear placement-by-placement.
  For someone who wants the poetic register.

Reference keyword tables (signs/elements/modalities, planet keywords, house meanings,
aspect meanings, dispositor logic, synastry priorities) live in
`references/reading-guidance.md` — load it when you want chart2ai's full modern-style
crib sheet rather than relying on your own astrological vocabulary.

## Gotchas

- **Geocoding** happens server-side, but your *input* matters. The endpoint expands
  `USA→United States` / `UK→United Kingdom`, filters to populated places, and ranks
  city > town > village — but ambiguous names still mis-resolve. **Pass `"City,
  State"` for US, `"City, Country"` elsewhere.** Bare "Brooklyn, USA" → Brooklyn,
  *Ohio*; pass "Brooklyn, New York". **Always check the `[BIRTHDATA]` line** echoes
  the intended place; re-run with a more specific place if not.
- **Time is local clock time at the birthplace**, not UTC. The endpoint resolves the timezone from lat/lng.
- **No time → no houses.** Use `--unknown-time` so the report omits angles/houses rather than emitting a noon-based fiction.
- **Default house system is Whole Sign** (`W`). Pop-astrology users may expect Placidus (`P`); offer to switch.

## Stack provenance (Jake's repos)

- `simple-astro-api` — the Netlify deployment serving `/api/chart`. Swiss Ephemeris + geocoding + chart2txt, all server-side.
- `chart2txt` — TS lib (npm, MIT). The analysis engine + text formatter, runs inside the endpoint.
- `chart2ai` — the full product app. The reading-voice registers and the Rule of Truth above are distilled from its prompt library (`src/data/systemPrompt.ts`, `src/data/promptSections.ts`).
- `AstroMCP` — the same integration as an MCP server, if you'd rather a native Hermes MCP tool.
