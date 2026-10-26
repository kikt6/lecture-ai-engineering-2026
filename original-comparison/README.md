# Original model comparison preparation

Status: **Four real UI runs recorded on 2026-10-26. Course compliance and final submission remain unverified.** See [OBSERVATIONS.md](OBSERVATIONS.md) and [observed-results.json](observed-results.json).

This independent, standard-library Python tool records real responses obtained separately. It does not call any API, use credentials, validate course requirements, or represent a completed assignment. Four responses were subsequently obtained through Google AI Studio's UI without selecting an API key. No lecture slides, distributed notebooks, or assignment text were used to create this work.

## Use

1. Write one original question in `question.local.txt`. Do not use restricted course materials or secrets.
2. Initialize the record:

```sh
python3 compare.py init --question-file question.local.txt
```

3. In an authorized service that explicitly supports model and temperature selection, run the exact same question for each chosen setting. Keep other settings constant and record repetitions where useful. A chat interface without temperature control cannot establish a temperature comparison. Obtain approval before paid API use or credential setup.
4. Save an actual response, unchanged, to `response.local.txt`. Record the actual model identifier, actual temperature, and a non-secret source/request reference:

```sh
python3 compare.py record --question-file question.local.txt --model ACTUAL_MODEL_ID --temperature 0.5 --output-file response.local.txt --evidence 'Non-secret source and actual run time'
python3 compare.py show
```

The example temperature is illustrative; use the value actually set, within the provider's supported range. This recorder accepts values from 0 to 2. It rejects a changed question and preserves response text. Source evidence is user-reported and not independently authenticated. Results and response files stay local by default; do not publish them without review. Do not store API keys in any file here.

## Verification

```sh
python3 -m unittest -v
```

Tests use explicitly synthetic fixtures in temporary directories. Test fixtures are not model outputs or experiment results.

## Remaining work

- Review the four recorded UI outputs and the factual observations supplied separately.
- Personally inspect the outputs and add only your own truthful reflection, if required.
- Personally check the course instructions and submission requirements. Final submission has not occurred.
