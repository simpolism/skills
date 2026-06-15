---
name: astrology
description: Compute astrological charts (natal, synastry, transit) and Human Design bodygraphs from birth date/time/place and get dense, LLM-readable chart text. Use when someone asks for their birth chart, an astrology reading, compatibility between two people, current transits, or a Human Design chart/Type/Strategy/Authority. Calls a hosted endpoint — no server, no Node, no install; pure Python stdlib.
when_to_use: User asks for a natal/birth chart, an astrology reading, synastry/compatibility between two people, current transits, or a Human Design chart (Type/Strategy/Authority/Profile/centers/channels/gates, single or partnership). Also when you need precise planetary positions, houses, aspects, dispositor trees, or aspect patterns (stelliums, T-squares, grand trines, yods) for a given moment and place.
---

# Astrology — date/time/place → chart text

This skill turns birth data into the dense, structured chart report that `chart2txt`
produces (signs, houses, aspects, dignities, dispositor trees, aspect patterns,
element/modality/polarity distributions). That report is designed for an LLM to read
and interpret — it is **data, not a reading**. You compute the chart, then *you* do
the interpretation in conversation.

## How it works

```
place ──geocode──▶ lat/lng ──Swiss Ephemeris──▶ raw positions ──chart2txt──▶ report text
```

All of this runs **server-side** at a hosted endpoint
(`https://simple-astro-api.netlify.app/api/chart`). The skill ships one small
client, `scripts/chart.py`, that builds the query, calls the endpoint, and prints
the report. It is **pure Python stdlib** — no Node, no npm, no pip, no bash — so it
runs identically on Windows, macOS, and Linux. The endpoint is public and free; no
API key.

## Quickstart

```bash
python scripts/chart.py --name "Jake" --date 1990-05-15 --time 14:30 --place "Brooklyn, New York"
```

(Use `python3` if that's what your platform calls it. On Windows, `python scripts\chart.py ...`.)

### Synastry (two people / compatibility)

Add a second person with the `*2` flags. The cross-aspect grid (A's planets to
B's planets) is appended automatically.

```bash
python scripts/chart.py --type synastry \
  --name "A" --date 1990-05-15 --time 14:30 --place "New York, New York" \
  --name2 "B" --date2 1988-11-02 --time2 08:15 --place2 "Los Angeles, California"
```

### Transit (natal chart + current sky)

```bash
python scripts/chart.py --type transit \
  --name "Jake" --date 1990-05-15 --time 14:30 --place "Brooklyn, New York" \
  --transit-date 2026-06-15 --transit-time 12:00
```

### Human Design (single, or partnership with two people)

A different system from astrology (bodygraph: Type, Strategy, Authority, Profile,
Incarnation Cross, defined/undefined centers, channels, gates). Same birth-data
flags. Add a second person (`*2` flags) for a partnership analysis
(electromagnetic/compromise/dominance channel dynamics).

```bash
# single
python scripts/chart.py --type humandesign \
  --name "Jake" --date 1990-05-15 --time 14:30 --place "Brooklyn, New York"

# partnership
python scripts/chart.py --type humandesign \
  --name "A" --date 1990-05-15 --time 14:30 --place "New York, New York" \
  --name2 "B" --date2 1988-11-02 --time2 08:15 --place2 "Los Angeles, California"
```

### Or just curl it directly

The wrapper is a convenience; the endpoint is a plain GET. Useful if you want the
raw response or aren't in a shell with the script handy:

```bash
curl -sS --get "https://simple-astro-api.netlify.app/api/chart" \
  --data-urlencode "name=Jake" --data-urlencode "date=1990-05-15" \
  --data-urlencode "time=14:30" --data-urlencode "place=Brooklyn, New York"
# -> {"text": "[METADATA]\nchart_type: natal\n..."}
```

## Flags

| Flag | Meaning |
|------|---------|
| `--name` / `--date` / `--time` / `--place` | Person 1's birth data. |
| `--name2` / `--date2` / `--time2` / `--place2` | Person 2 (synastry / HD partnership). |
| `--date` | Birth date, `YYYY-MM-DD`. Required. |
| `--time` | Birth time, `HH:MM` or `HH:MM:SS`, 24-hour, **local time at the birthplace**. |
| `--place` | Birthplace. Use `"City, State"` (US) or `"City, Country"`. See gotchas. Required. |
| `--type` | `natal` (default), `synastry`, `transit`, or `humandesign` (`hd` alias). |
| `--house-system` | `P` Placidus, `W` Whole Sign (default), `E` Equal, `O` Porphyry. Astrology only. |
| `--transit-date` / `--transit-time` / `--transit-place` | The "current sky" moment for `--type transit`. Place defaults to person 1's place. |
| `--unknown-time` | Birth time unknown: planets only, no Ascendant/houses/angles. Astrology only — HD requires a known time. |
| `--json` | Print the raw chart object(s) / API response instead of the text report. |

Override the endpoint with the `ASTRO_API_BASE` env var (e.g. for a local
`netlify dev` instance).

## Gathering birth data from the user

To compute a real chart you need three things — ask for any that are missing:

1. **Date** of birth.
2. **Time** of birth (local clock time at the birthplace). This is the big one:
   the Ascendant and all house placements depend on it. If they don't know it,
   use `--unknown-time` and tell them you can still read sign placements and
   planet-to-planet aspects, just not houses or rising sign.
3. **Place** of birth (city + state/country).

## Reading the output (interpreting it well)

The report sections, roughly in order of interpretive weight:

- **[ANGLES]** — Ascendant (rising sign / self-presentation) and Midheaven (vocation/public role). Only present with a known time.
- **[PLANETS]** — each planet's sign, degree, dignity (Domicile/Detriment/Exaltation/Fall/Ruler), and house. The Sun/Moon/Ascendant are the core trio.
- **[DISPOSITOR TREE]** — chains of "who rules whom"; final dispositors and cycles show where the chart's power concentrates.
- **[ELEMENT/MODALITY/POLARITY DISTRIBUTION]** — temperament balance. A heavy element or a missing one is interpretively loud.
- **[ASPECTS]** — geometric relationships, grouped by orb tightness. Tighter orb = stronger. `applying` aspects are intensifying, `separating` are waning.
- **Aspect patterns** (when present): stellium, T-square, grand trine, yod, etc.
- **[SYNASTRY: A-B]** (two-person) — cross-aspects between the two people's planets; the heart of compatibility analysis.
- **Human Design**: `[TYPE]` (Type/Strategy/Authority/Profile/Incarnation Cross), `[CENTERS]` (defined vs undefined), `[CHANNELS]`, `[GATES]`. For partnerships, the `[PARTNERSHIP]` section covers channel electromagnetics.

Interpret in conversation. The report is the ephemeris a human astrologer would read
from; your job is the reading. Lead with the angles + luminaries, then let tight
aspects and concentrations of element/dignity guide what's salient.

## Gotchas

- **Geocoding is the fragile step** (it happens server-side, but the *input* you
  send matters). The endpoint expands abbreviated country tokens (`USA→United
  States`, `UK→United Kingdom`), filters to populated places, and ranks city > town
  > village rather than taking the first fuzzy hit — but ambiguous names still
  resolve to the wrong place. **Best practice: pass `"City, State"` for US places
  and `"City, Country"` elsewhere.** Bare "Brooklyn, USA" resolves to Brooklyn,
  *Ohio* (a `city`, which outranks the NYC borough); pass "Brooklyn, New York".
  **Always sanity-check the `[BIRTHDATA]` line** echoes the place the user meant;
  if it geocoded wrong, re-run with a more specific place.
- **Time is local clock time at the birthplace**, not UTC. The endpoint resolves
  the timezone from the lat/lng and converts.
- **No time → no houses.** Without a birth time, the Ascendant, Midheaven, and house
  placements are meaningless. Use `--unknown-time` so the report omits them rather
  than emitting a noon-based fiction.
- **Default house system is Whole Sign** (`W`). If the user is used to Western
  pop-astrology apps, they may expect Placidus (`P`); offer to switch.
- **Human Design requires a known birth time** (the design/personality split and
  the whole bodygraph depend on it) and ignores `--house-system`.

## Stack provenance (Jake's repos)

- `simple-astro-api` — the Netlify deployment serving `/api/chart` (and the lower-level
  `/api/positions`, `/api/positions-with-design`). Swiss Ephemeris (`sweph`) +
  geocoding + chart2txt rendering, all server-side. The `/api/chart` route is the
  unified endpoint this skill calls.
- `chart2txt` — TypeScript lib (npm, MIT). The analysis engine + text formatter that
  produces the report; runs inside the endpoint.
- `AstroMCP` — the same integration as an MCP server (`get_chart` tool). An alternative
  to this skill if you'd rather expose it as a native Hermes MCP tool.
- `chart2ai` — the full product app (Expo/React Native) built on the same core.

> This skill is a worked instance of the `wrapping-a-service-as-a-skill` pattern.
> Note the distribution lesson: the first version vendored an npm package and shelled
> to Node, which made the skill non-portable (needed Node + `npm install` on every
> machine). Moving the logic behind a hosted HTTP endpoint and shipping a pure-stdlib
> client is what makes a skill genuinely drop-in across OSes.
