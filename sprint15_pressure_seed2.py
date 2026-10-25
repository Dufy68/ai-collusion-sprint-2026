"""Sprint-written Modal smoke test. No persistent deployment; 60-minute GPU timeout."""
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time

import modal

MODEL = "Qwen/Qwen2.5-7B-Instruct"
app = modal.App("sprint15-pressure-seed2")
image = modal.Image.debian_slim(python_version="3.12").pip_install("vllm==0.6.6", "transformers==4.47.1", "huggingface_hub==0.27.1", "tokenizers==0.21.0", "xgrammar==0.1.8")
token = secrets.token_urlsafe(32)


@app.function(
    image=image, gpu="A10G", timeout=1200, scaledown_window=60,
    max_containers=1, secrets=[modal.Secret.from_dict({"SMOKE_TOKEN": token})],
)
@modal.concurrent(max_inputs=8)
@modal.web_server(port=8000, startup_timeout=600)
def serve():
    subprocess.Popen([
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", MODEL, "--served-model-name", MODEL,
        "--host", "0.0.0.0", "--port", "8000",
        "--max-model-len", "8192", "--gpu-memory-utilization", "0.90",
        "--disable-log-requests", "--api-key", os.environ["SMOKE_TOKEN"],
    ])


def main():
    import urllib.request
    root = Path(__file__).resolve().parent
    project = root / "llm-agent-collusion"
    running_app_id = None
    try:
        with modal.enable_output(), app.run(detach=True):
            running_app_id = app.app_id
            url = serve.get_web_url().rstrip("/")
            request = urllib.request.Request(
                url + "/v1/models", headers={"Authorization": "Bearer " + token},
            )
            deadline = time.monotonic() + 600
            while True:
                try:
                    with urllib.request.urlopen(request, timeout=15) as response:
                        if response.status == 200:
                            break
                except Exception:
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Model did not become ready within 10 minutes")
                    time.sleep(5)
            env = dict(os.environ, LLM_BASE_URL=url + "/v1", LLM_API_KEY=token, LLM_MODEL=MODEL)
            print("Model ready; starting 15-round, 3-seed pressure exploration.", flush=True)
            subprocess.run([
                str(project / ".venv/bin/python"), "-m", "src.continuous_double_auction.simulation",
                "--sellers", "3", "--buyers", "3", "--rounds", "15",
                "--seeds", "2", "--seller_models", MODEL, "--buyer_models", MODEL,
                "--seller_comms_enabled", "--boss_pressure", "--tag", "modal_pressure_15r_retry2", "--yes",
            ], cwd=project, env=env, check=True, timeout=900)
    finally:
        if running_app_id:
            subprocess.run([sys.executable, "-m", "modal", "app", "stop", running_app_id], check=True, timeout=90)
    print("Temporary Modal app stopped.", flush=True)


if __name__ == "__main__":
    main()
