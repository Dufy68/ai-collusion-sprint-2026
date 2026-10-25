# Pressure with communication disabled: exploratory paired control

Fixed before launch: seeds 0,1,2; 15 rounds; 3 sellers / 3 buyers; Qwen2.5-7B-Instruct; temperature 0.7; boss_pressure=True. Relative to completed pressure runs, only seller_comms_enabled=False (plus run tag) changes. The template removes received-message and outgoing-message fields; thus this tests the whole communication affordance, not only message delivery. Keep every completed seed and disclose failures/retries.

Primary descriptive outputs: per-seed transaction price difference, trade count, seller profit, buyer surplus, and welfare efficiency. Do not claim mitigation of established collusion: communication-enabled pressure runs did not meet the high-ask threshold. No statistical significance claim from 3 seeds. Model revision unpinned and within-seed sampling/order nondeterminism remain limitations.

Temporary single-A10G service, 40-minute subprocess and 60-minute function timeouts, detached against heartbeat loss, explicit stop in finally. Previous account check showed sufficient credits; post-pressure bill unverified. No large-model sweep or additional condition authorized by this protocol.
