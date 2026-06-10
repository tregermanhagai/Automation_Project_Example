import pytest
from pathlib import Path
from datetime import datetime


# Anchor to the folder where conftest.py lives — not the CWD
SHOTS = Path(__file__).parent / "test-results"
SHOTS.mkdir(parents=True, exist_ok=True)
RESULTS = []   # collected rows for the final table


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Runs after each test phase. We care about the 'call' phase (the test body)."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return  # ignore setup/teardown phases

    # Try to grab the live `page` fixture so we can screenshot it.
    page = item.funcargs.get("page")
    shot_path = ""
    if page is not None:
        safe_name = item.name.replace("/", "_").replace("[", "_").replace("]", "")
        shot_path = SHOTS / f"{safe_name}.png"
        try:
            page.screenshot(path=str(shot_path), full_page=True)
        except Exception as e:
            shot_path = f"(screenshot failed: {e})"

    note = ""
    if report.failed:
        # first line of the error is usually the most useful note
        note = str(report.longrepr).splitlines()[-1][:120]

    RESULTS.append({
        "test": item.name,
        "status": "PASS" if report.passed else "FAIL",
        "note": note,
        "snapshot": str(shot_path),
    })


def pytest_sessionfinish(session, exitstatus):
    """Print the results table to console AND write it to a file."""
    if not RESULTS:
        return

    lines = []
    lines.append("=" * 70)
    lines.append(f"TEST RESULTS  ({datetime.now():%Y-%m-%d %H:%M})")
    lines.append("=" * 70)
    lines.append(f"{'TEST':<35} {'STATUS':<6} NOTE")
    lines.append("-" * 70)
    for r in RESULTS:
        lines.append(f"{r['test']:<35} {r['status']:<6} {r['note']}")
    lines.append("-" * 70)
    passed = sum(1 for r in RESULTS if r["status"] == "PASS")
    lines.append(f"{passed}/{len(RESULTS)} passed.  Snapshots in: {SHOTS.resolve()}")
    lines.append("=" * 70)

    report_text = "\n".join(lines)
    print("\n\n" + report_text)

    # Ensure the folder exists right before writing (the fix)
    SHOTS.mkdir(parents=True, exist_ok=True)
    report_file = SHOTS / "results.txt"
    report_file.write_text(report_text, encoding="utf-8")
    print(f"\nResults written to: {report_file.resolve()}")