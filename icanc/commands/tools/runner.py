import tomllib
import difflib
import os
import subprocess

def run(bin_path, testcases_path):
    with open(testcases_path, "rb") as f:
        cases = tomllib.load(f).items()
        runs = []

        for name, case in cases:
            if "in" not in case or "out" not in case:
                runs.append({
                    "name": name,
                    "error": "invalid_case",
                })
                continue

            result = subprocess.run(
                bin_path,
                input=case.get("in"),
                capture_output=True,
                text=True,
                env=dict(os.environ, LIBC_FATAL_STDERR_="1")
            )

            if result.returncode != 0:
                runs.append({
                    "name": name,
                    "error": "runtime",
                    "stderr": result.stderr,
                })
                continue

            actual = result.stdout
            expected = case.get("out")
            if expected == actual:
                runs.append({
                    "name": name,
                    "error": None,
                })
            else:
                diff = difflib.unified_diff(expected.splitlines(), actual.splitlines(), fromfile="expected", tofile="received", lineterm="")
                line = next(diff, None)
                if line is None:
                    runs.append({
                        "name": name,
                        "error": "presentation",
                    })
                else:
                    fail_diff = [line]
                    for l in diff:
                        fail_diff.append(l)

                    runs.append({
                        "name": name,
                        "error": "wrong_answer",
                        "diff": fail_diff
                    })
        
        return runs
