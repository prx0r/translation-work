"""A fresh or reused output directory must produce the same full index."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'tools'))
import emit_scholar


class ProjectionIndexTests(unittest.TestCase):
    def test_full_rebuild_ignores_stale_index_and_sorts_keys(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for work in ('alpha', 'beta'):
                folder = root / work / 'data'
                folder.mkdir(parents=True)
                (folder / 'p.t1.json').write_text('[]', encoding='utf-8')
            first, second = root / 'first', root / 'second'
            second.mkdir()
            (second / 'index.json').write_text(json.dumps({'stale': {'title': 'stale'},
                                                           'beta': {'generated': 'old'}}), encoding='utf-8')
            def build(work):
                return {'work': work, 'versions': [], 'reviews': [], 'signoffs': [],
                        'generated': None, 'originals': {}}
            with mock.patch.object(emit_scholar, 'ROOT', root), mock.patch.object(emit_scholar, 'build', side_effect=build):
                for output in (first, second):
                    with mock.patch.object(sys, 'argv', ['emit_scholar.py', '--all', '--out', str(output)]), contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(emit_scholar.main(), 0)
            self.assertEqual((first / 'index.json').read_bytes(), (second / 'index.json').read_bytes())
            self.assertEqual(list(json.loads((first / 'index.json').read_text())), ['alpha', 'beta'])


if __name__ == '__main__':
    unittest.main()
