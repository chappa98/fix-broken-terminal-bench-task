There is an Apache-style access log at `/app/access.log`. Parse it and write a
summary report to `/app/report.json`.

Success criteria:

1. `/app/report.json` exists and contains valid JSON.
2. The JSON object has exactly these keys:
   - `total_requests` (integer) — the number of non-empty lines in the log.
   - `unique_ips` (integer) — the number of distinct client IP addresses
     (first whitespace-separated field of each line).
   - `top_path` (string) — the request path (e.g. `/index.html`) that
     appears most often across all HTTP methods (GET, POST, PUT, DELETE,
     HEAD, PATCH). Ties may be broken arbitrarily.
3. All three values must be computed correctly from `/app/access.log` as it
   exists in the environment — not hardcoded.
