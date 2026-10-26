"""Offline recorder for real, independently obtained model responses. No API calls."""
import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


def initialize(path, question):
    if not question.strip():
        raise ValueError('Question must not be empty')
    data = {'question': question, 'question_sha256': hashlib.sha256(question.encode()).hexdigest(), 'runs': []}
    with Path(path).open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record(path, question, model, temperature, output, evidence):
    p = Path(path)
    data = json.loads(p.read_text(encoding='utf-8'))
    if question != data['question']:
        raise ValueError('Question differs from the experiment question')
    if not math.isfinite(temperature) or not 0 <= temperature <= 2:
        raise ValueError('Temperature must be finite and between 0 and 2; also check provider limits')
    if not all(s.strip() for s in [model, output, evidence]):
        raise ValueError('Actual model name, response and evidence/source are required')
    data['runs'].append({'model': model, 'temperature': temperature, 'output': output,
                         'evidence': evidence, 'recorded_at_utc': datetime.now(timezone.utc).isoformat()})
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--question-file', required=True)
    init.add_argument('--results', default='results.local.json')
    add = sub.add_parser('record')
    add.add_argument('--question-file', required=True)
    add.add_argument('--results', default='results.local.json')
    add.add_argument('--model', required=True)
    add.add_argument('--temperature', required=True, type=float)
    add.add_argument('--output-file', required=True)
    add.add_argument('--evidence', required=True)
    show = sub.add_parser('show')
    show.add_argument('--results', default='results.local.json')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            initialize(args.results, Path(args.question_file).read_text(encoding='utf-8'))
            print('Initialized; zero model calls and zero observations.')
        elif args.command == 'record':
            record(args.results, Path(args.question_file).read_text(encoding='utf-8'), args.model,
                   args.temperature, Path(args.output_file).read_text(encoding='utf-8'), args.evidence)
            print('Recorded supplied response; provenance is user-reported, not independently verified.')
        else:
            print(Path(args.results).read_text(encoding='utf-8'))
    except (ValueError, OSError, KeyError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
