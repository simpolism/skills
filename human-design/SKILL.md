---
name: human-design
description: Compute and interpret Human Design bodygraphs (Type, Strategy, Authority, Profile, Incarnation Cross, defined/undefined centers, channels, gates) from birth date/time/place, single or two-person partnership. Returns dense, LLM-readable bodygraph text. Use when someone asks for their Human Design chart, Type, Strategy, Authority, or HD compatibility. Calls a hosted endpoint — no server, no Node, no install; pure Python stdlib. For astrology (zodiac/planets/aspects), use the astrology skill instead.
when_to_use: User asks for their Human Design chart or bodygraph, their Type (Generator/Manifestor/Projector/Reflector/Manifesting Generator), Strategy, Authority, Profile, Incarnation Cross, centers/channels/gates, or HD partnership/compatibility. NOT for zodiac astrology (Sun sign, houses, planetary aspects) — that's the separate astrology skill.
---

# Human Design — bodygraph + reading

Human Design is a synthesis system (astrology + I Ching + Kabbalah + chakras) that
produces a **bodygraph**: a person's Type, Strategy, Authority, Profile, defined vs.
undefined energy centers, channels, and gates. This skill computes the bodygraph and
gives you the framework to read it. The report is **data, not a reading** — compute
it, then *you* do the reading.

## How it works

```
place ──geocode──▶ lat/lng ──Swiss Ephemeris──▶ personality + design positions ──chart2txt──▶ bodygraph text
```

HD uses *two* sets of positions: the **personality** (conscious, at birth) and the
**design** (unconscious, ~88° of solar arc before birth — roughly 3 months prior).
The endpoint computes both and derives the bodygraph. All server-side at
`https://simple-astro-api.netlify.app/api/chart`. The skill ships one small client,
`scripts/chart.py`, that is **pure Python stdlib** — no Node, no npm, no pip, no bash
— so it runs identically on Windows, macOS, and Linux. Public/free, no API key.

## Quickstart

```bash
python scripts/chart.py --name "Jake" --date 1990-05-15 --time 14:30 --place "Brooklyn, New York"
```

(Use `python3` if that's what your platform calls it. On Windows, `python scripts\chart.py ...`.)
This script defaults to Human Design — no `--type` needed.

### Partnership (two people)

Add a second person with the `*2` flags. The `[PARTNERSHIP]` section covers channel
electromagnetics (attraction), compromise, and dominance between the two bodygraphs.

```bash
python scripts/chart.py \
  --name "A" --date 1990-05-15 --time 14:30 --place "New York, New York" \
  --name2 "B" --date2 1988-11-02 --time2 08:15 --place2 "Los Angeles, California"
```

## Flags

| Flag | Meaning |
|------|---------|
| `--name` / `--date` / `--time` / `--place` | Person 1's birth data. All three of date/time/place needed (see below). |
| `--name2` / `--date2` / `--time2` / `--place2` | Person 2 (partnership). |
| `--time` | `HH:MM` or `HH:MM:SS`, 24-hour, **local time at the birthplace**. **Required for HD.** |
| `--place` | `"City, State"` (US) or `"City, Country"`. See gotchas. |
| `--json` | Print the raw `{personality, design, metadata}` response instead of the text report. |

## Gathering birth data

HD needs **all three**, and **the time is non-negotiable**:

1. **Date** of birth.
2. **Time** of birth (local clock time at the birthplace). Unlike astrology, HD has
   no useful "unknown time" mode — the personality/design split, the Profile, and
   center definitions all shift with the time. If the user doesn't know their birth
   time, tell them an HD chart can't be computed reliably; don't fake it.
3. **Place** of birth (city + state/country).

## The Rule of Truth (read this before interpreting)

Adapted from Jake's chart2ai system prompt:

> **Only refer to data present in the provided bodygraph.** Do not infer Type,
> Authority, channels, or gate activations from memory or assumption. If a center
> isn't listed as defined, treat it as undefined. If a channel isn't printed, it
> isn't formed. Confirm every claim against the report before stating it.

The report is the sole source of HD fact. Your craft is synthesis, not recall.

## Reading the output

The bodygraph report sections, in interpretive order:

- **[TYPE]** — the spine of the reading. Contains:
  - **Type** — the aura mechanic and how the person is built to engage life.
  - **Strategy** — the correct way *for that Type* to make decisions / engage.
  - **Authority** — the inner decision-making mechanism to trust (overrides the mind).
  - **Profile** — two numbers (e.g. 1/3), the conscious/unconscious life-theme pairing.
  - **Incarnation Cross** — the overarching life purpose/theme (four gates).
  - **Definition** — how the defined centers connect (Single, Split, Triple Split, etc.).
- **[CENTERS]** — **Defined** centers = consistent, reliable energy the person radiates. **Undefined/open** centers = where they take in and amplify others' energy, and where conditioning/"not-self" pressure lives.
- **[CHANNELS]** — the defined connections between centers; each is a specific life-force/gift. Named (e.g. "1-8 Inspiration").
- **[GATES]** — individual activations (Personality = conscious, Design = unconscious). Hanging gates (half a channel) show what the person seeks to complete in others.

### The five Types (the load-bearing distinction)

- **Generator** (Sacral defined) — life-force/work energy; Strategy: **respond** (wait for something to respond to, don't initiate from the mind). Signature: satisfaction; not-self: frustration.
- **Manifesting Generator** (Sacral defined + a motor to the Throat) — Generator that can also initiate; Strategy: **respond, then inform**. Fast, multi-passionate.
- **Manifestor** (a motor to the Throat, Sacral undefined) — initiator; Strategy: **inform before acting**. Signature: peace; not-self: anger.
- **Projector** (no motor to Throat, Sacral undefined) — guide/seer of others' energy; Strategy: **wait for the invitation** (for the big things: relationship, work, place). Signature: success; not-self: bitterness.
- **Reflector** (no defined centers) — mirror of community/environment; Strategy: **wait a lunar cycle** before major decisions. Signature: surprise; not-self: disappointment.

### Authorities (in rough hierarchy)

Emotional (Solar Plexus) > Sacral > Splenic > Ego/Heart > Self/G > Mental/environmental
> Lunar (Reflectors). Emotional authority = "wait out the emotional wave, no decision
in the moment." Sacral = gut yes/no in the now. Splenic = quiet, spontaneous, one-time
intuition. Lead the reading with **Type + Strategy + Authority** — that trio is the
practical core of how the person is designed to live.

## Reading voice

The same three registers from chart2ai's astrology prompts transfer to HD — default
to **standard** (warm, accessible, ground the mechanics in lived terms), or shift to
**professional** (precise HD terminology, named center/channel mechanics) or
**mystical** (archetypal, the bodygraph as a map of the soul's design) if the user
signals that register. Whatever the voice: frame undefined centers as places of
*potential wisdom*, not deficiency, and emphasize Strategy + Authority as agency, not
fate.

## Gotchas

- **Birth time is required and matters more than in astrology.** No `--unknown-time`
  mode — decline to compute if the time is unknown rather than emit a wrong bodygraph.
- **Geocoding** happens server-side, but your *input* matters. **Pass `"City, State"`
  (US) or `"City, Country"` elsewhere.** Bare "Brooklyn, USA" → Brooklyn, *Ohio*; pass
  "Brooklyn, New York". **Check the `[BIRTHDATA]` line** echoes the intended place.
- **Time is local clock time at the birthplace**, not UTC. The endpoint resolves the timezone from lat/lng.
- **Two charts auto-triggers partnership mode** (no flag needed); one chart is a single bodygraph.

## Stack provenance (Jake's repos)

- `simple-astro-api` — the Netlify deployment serving `/api/chart` (with `type=humandesign`). Computes the personality+design split server-side via Swiss Ephemeris, then renders with chart2txt's `humandesign2txt` / `humandesignPartnership2txt`.
- `chart2txt` — TS lib (npm, MIT). The bodygraph derivation (Type/Authority/centers/channels/gates) + text formatter.
- `chart2ai` — the full product app (which also supports Human Design). The reading-voice registers and Rule of Truth above are distilled from its prompt library.
