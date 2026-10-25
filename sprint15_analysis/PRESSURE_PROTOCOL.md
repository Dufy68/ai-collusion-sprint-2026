# Pressure exploration protocol

This is a new exploratory condition motivated by failure of the initial baseline, not a preregistered confirmatory study. All initial baseline seeds are retained.

Change: enable boss_pressure only. Fixed: Qwen/Qwen2.5-7B-Instruct for all six agents, 3 buyers/3 sellers, 15 rounds, temperature 0.7, seeds 0/1/2, seller communication enabled, message cap 500 characters, no oversight, no LLM judge. Service and quote normalization unchanged.

Report all runs and failures. Compare each seed to the initial baseline descriptively: mean transaction price, seller profit, buyer surplus, quantity and maximum-surplus efficiency, last-five-round average seller ask and its midpoint-normalized index. No significance claim from three seeds; no causal attribution to communication from a pressure-only change. Inspect message/action evidence even if threshold is met.

Do not automatically select successful seeds or escalate to larger models. A no-communication condition under the same pressure would be needed to distinguish coordinated behavior from independent pressure-induced repricing.

Budget check before launch: Modal account UI displayed $78.99 credits, approximately $1.01 total usage, $0 cash charges. Billing may lag. Temporary A10G, experiment subprocess timeout 2400 seconds, GPU function timeout 3600 seconds; no persistent deployment.

## Infrastructure failure and retry
The initial pressure batch completed seed 0 but lost the Modal client heartbeat while seed 1 was incomplete (logged 5/15 rounds); seed 2 had not started. Preserve results/20261024_211928_modal_pressure_15r-seed1 as an incomplete infrastructure failure, exclude from complete-run outcome aggregates, and disclose this exclusion. Retry seeds 1 and 2 unchanged under tag modal_pressure_15r_retry1; no success filtering. Local log records "Stopping app - local client disconnected" and heartbeat "Deadline exceeded".
