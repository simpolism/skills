#!/usr/bin/env python3
"""chart.py — query the unified endpoint for a Human Design bodygraph and print
the chart2txt report. Pure Python stdlib (urllib + json); no Node, no npm, no pip,
no bash. Runs identically on Windows, macOS, and Linux.

This copy defaults to --type humandesign. The same endpoint also serves astrology
charts (natal/synastry/transit) — see the separate `astrology` skill for those.

All the work (geocode -> Swiss Ephemeris -> personality/design split -> chart2txt)
happens server-side. This wrapper builds the query, calls /api/chart, and prints
the `text` field (or raw JSON with --json).

Usage (single bodygraph):
  python chart.py --name "Jake" --date 1990-05-15 --time 14:30 --place "Brooklyn, New York"

Partnership (two people) — add a second person with the *2 flags:
  python chart.py \
    --name "A" --date 1990-05-15 --time 14:30 --place "New York, New York" \
    --name2 "B" --date2 1988-11-02 --time2 08:15 --place2 "Los Angeles, California"

Human Design REQUIRES a known birth time (the personality/design split depends on it).

Override the endpoint with the ASTRO_API_BASE env var (default below).
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

DEFAULT_BASE = "https://simple-astro-api.netlify.app"


def main() -> int:
    p = argparse.ArgumentParser(add_help=True, description="Unified astrology / Human Design chart endpoint client.")
    # person 1
    p.add_argument("--name")
    p.add_argument("--date")
    p.add_argument("--place")
    p.add_argument("--time")
    # person 2 (synastry / HD partnership)
    p.add_argument("--name2")
    p.add_argument("--date2")
    p.add_argument("--place2")
    p.add_argument("--time2")
    # mode + options
    p.add_argument("--type", default="humandesign", help="humandesign (default). The endpoint also accepts natal|synastry|transit — see the astrology skill.")
    p.add_argument("--house-system", dest="house_system", default="W", help="P|W|E|O (default W)")
    p.add_argument("--transit-date", dest="transit_date")
    p.add_argument("--transit-time", dest="transit_time")
    p.add_argument("--transit-place", dest="transit_place")
    p.add_argument("--unknown-time", dest="unknown_time", action="store_true",
                   help="planets only, no houses/angles (astrology only)")
    p.add_argument("--json", action="store_true", help="print raw JSON instead of the text report")
    args = p.parse_args()

    if not args.date or not args.place:
        p.error("--date and --place are required (and usually --time)")

    # For transits with no explicit transit moment, default to "now" (UTC).
    # (HD doesn't use transits, but this keeps the wrapper identical to the
    # astrology skill's copy so the two don't drift.)
    if args.type == "transit" and not args.transit_date:
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc)
        args.transit_date = now.strftime("%Y-%m-%d")
        if not args.transit_time:
            args.transit_time = now.strftime("%H:%M:%S")
        sys.stderr.write(
            f"(transit defaulted to now: {args.transit_date} {args.transit_time} UTC)\n"
        )

    # Build query params; only include what's set.
    params = {
        "name": args.name,
        "date": args.date,
        "time": args.time,
        "place": args.place,
        "name2": args.name2,
        "date2": args.date2,
        "time2": args.time2,
        "place2": args.place2,
        "type": args.type,
        "house_system": args.house_system,
        "transit_date": args.transit_date,
        "transit_time": args.transit_time,
        "transit_place": args.transit_place,
    }
    if args.unknown_time:
        params["unknown_time"] = "1"
    if args.json:
        params["format"] = "json"
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})

    base = os.environ.get("ASTRO_API_BASE", DEFAULT_BASE).rstrip("/")
    url = f"{base}/api/chart?{query}"

    req = urllib.request.Request(url, headers={"User-Agent": "astrology-skill-chart.py"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        # The endpoint returns JSON {error: ...} even on 4xx/5xx.
        body = e.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"request failed: {e}\n")
        return 1

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        sys.stderr.write("non-JSON response from endpoint:\n" + body + "\n")
        return 1

    if isinstance(data, dict) and "error" in data:
        sys.stderr.write(f"API error: {data['error']}\n")
        return 1

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(data.get("text", json.dumps(data, indent=2, ensure_ascii=False)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
