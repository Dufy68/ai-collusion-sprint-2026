# Release verification

- Recomputed recorded audit metrics from raw traces; all values match the frozen summaries within 1e-9.
- Ran both descriptive comparison scripts successfully with the recorded experiment environment (Matplotlib 3.11.2).
- Verified the bootstrap fetches upstream commit d585a7b3be50366cc2bdf5789bf8add5890b2abd and applies the sprint patch. No new cloud experiments were launched.
- Scanned release text for common credential formats, private-key headers, personal home paths, and email addresses; no matches. This pattern scan is not a guarantee against every possible sensitive string.
- The simulator, utilities, virtual environments, model weights, and cloud authentication are excluded from the tracked tree; the simulator is restored by bootstrap.
