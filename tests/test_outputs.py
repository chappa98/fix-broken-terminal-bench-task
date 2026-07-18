import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected():
    """Independently recompute the correct answer from the log, so this
    verifier checks real correctness rather than mere file presence."""
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(
                r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line
            )
            if m:
                paths[m.group(1)] += 1
    top = paths.most_common()
    top_count = top[0][1]
    top_candidates = {p for p, c in top if c == top_count}
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path_candidates": top_candidates,
    }


def test_criterion_1_report_exists_and_valid_json():
    """Verifies instruction.md criterion 1: /app/report.json exists and
    contains valid JSON."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    data = json.loads(REPORT_PATH.read_text())
    assert isinstance(data, dict), "report.json must contain a JSON object"


def test_criterion_2_has_required_keys():
    """Verifies instruction.md criterion 2: the JSON object has exactly
    the keys total_requests, unique_ips, and top_path."""
    data = json.loads(REPORT_PATH.read_text())
    required = {"total_requests", "unique_ips", "top_path"}
    missing = required - data.keys()
    assert not missing, f"report.json missing keys: {missing}"


def test_criterion_3_values_are_correct():
    """Verifies instruction.md criterion 3: total_requests, unique_ips,
    and top_path are all computed correctly from /app/access.log."""
    data = json.loads(REPORT_PATH.read_text())
    exp = _expected()

    assert data["total_requests"] == exp["total_requests"], (
        f"total_requests={data['total_requests']!r}, "
        f"expected {exp['total_requests']}"
    )
    assert data["unique_ips"] == exp["unique_ips"], (
        f"unique_ips={data['unique_ips']!r}, expected {exp['unique_ips']}"
    )
    assert data["top_path"] in exp["top_path_candidates"], (
        f"top_path={data['top_path']!r}, "
        f"expected one of {exp['top_path_candidates']}"
    )
