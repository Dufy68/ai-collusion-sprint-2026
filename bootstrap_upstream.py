"""Fetch the attributed upstream baseline and apply the sprint compatibility patch.
Does not launch Modal or incur GPU usage. Requires git and network access.
"""
from pathlib import Path
import shutil
import subprocess
ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / ".upstream"
REVISION = "d585a7b3be50366cc2bdf5789bf8add5890b2abd"
def git(*args):
    subprocess.run(["git", *args], cwd=UPSTREAM, check=True)
if UPSTREAM.exists():
    raise SystemExit(".upstream already exists; inspect or move it before retrying.")
UPSTREAM.mkdir()
git("init")
git("remote", "add", "origin", "https://github.com/poseidon-research/collusion_hackathon.git")
git("fetch", "--depth", "1", "origin", REVISION)
git("checkout", "--detach", "FETCH_HEAD")
git("apply", str(ROOT / "SPRINT_CODE_CHANGES.patch"))
shutil.copytree(UPSTREAM / "util", ROOT / "util", dirs_exist_ok=True)
project = ROOT / "llm-agent-collusion"
for item in (UPSTREAM / "llm-agent-collusion").iterdir():
    if item.name in {"data", "results", ".venv", ".git", "__pycache__", ".gitignore"}:
        continue
    target = project / item.name
    if item.is_dir():
        shutil.copytree(item, target, dirs_exist_ok=True)
    else:
        shutil.copy2(item, target)
print("Upstream source restored and patch applied. Recorded sprint results preserved.")
