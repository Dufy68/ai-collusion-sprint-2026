"""Sprint-written Modal smoke test. No persistent deployment; 20-minute GPU timeout."""
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time

import modal

MODEL = "Qwen/Qwen2.5-7B-Instruct"
app = modal.App("sprint15-smoke")
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
        "--api-key", os.environ["SMOKE_TOKEN"],
    ])


def main():
    import urllib.request
    root = Path(__file__).resolve().parent
    project = root / "llm-agent-collusion"
    with modal.enable_output(), app.run():
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
        print("Model ready; starting 5-round smoke test.", flush=True)
        subprocess.run([
            str(project / ".venv/bin/python"), "-m", "src.continuous_double_auction.simulation",
            "--sellers", "3", "--buyers", "3", "--rounds", "5",
            "--seeds", "0", "--seller_models", MODEL, "--buyer_models", MODEL,
            "--seller_comms_enabled", "--tag", "modal_smoke_v5", "--yes",
        ], cwd=project, env=env, check=True, timeout=600)
    print("Temporary Modal app stopped.", flush=True)


if __name__ == "__main__":
    main()
