#!/usr/bin/env python3
"""Multi-work span truth: every workcfg work resolves end-to-end.

For each registered work: source file exists, every song's verses parse and
sit inside source_spans, and the adapter resolves the first/last verse of
each song. No network, no fixtures. Slow parsers would fail here first.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import passage_adapter as adapter
import workcfg


class MultiWorkSpansTests(unittest.TestCase):
    def test_all_works_resolve(self):
        self.assertGreaterEqual(len(workcfg.WORKS), 1)
        checked = 0
        for work in sorted(workcfg.WORKS):
            src = Path(workcfg.WORKS[work]['source'])
            self.assertTrue(src.is_file(), f'{work} source missing: {src}')
            songs = workcfg.WORKS[work].get('songs', {})
            if not songs:
                continue
            verses_all = workcfg.source_spans(work)
            self.assertTrue(verses_all, f'{work} has no spans')
            for song in sorted(songs):
                verses = workcfg.song_verses(work, song)
                self.assertTrue(verses, f'{work}:{song} has no verses')
                self.assertTrue(set(verses).issubset(set(verses_all)),
                                f'{work}:{song} verses outside spans')
                for v in (verses[0], verses[-1]):
                    r = adapter.resolve(work, f'{song}-v{v}')
                    self.assertEqual(r['kind'], 'verse')
                    checked += 1
        self.assertGreater(checked, 0)

    def test_volume_manifests_cover_resolved_verses(self):
        # Every workcfg work (except pre-manifest segments kinds) records its
        # source bytes per verse block; spot-check the first span round-trip.
        import hashlib
        import json as _json
        import workcfg as _workcfg
        count = 0
        for work in sorted(_workcfg.WORKS):
            for path in sorted((ROOT / work / 'source' / 'volumes').glob('*.json')):
                m = _json.loads(path.read_text())
                self.assertEqual(m['format'], 'svatantrya-source-volume/1')
                self.assertTrue(m['spans'], path)
                self.assertTrue(m.get('source_file'), path)
                raw = (ROOT / m['source_file']).read_bytes()
                raw.decode('utf-8')
                first = m['spans'][0]
                seg = raw[first['start']:first['end']].decode('utf-8')
                self.assertTrue(seg.strip(), path)
                self.assertEqual(hashlib.sha256(seg.encode()).hexdigest(),
                                 first['text_sha256'], path)
                count += 1
        self.assertGreater(count, 30)


if __name__ == '__main__':
    unittest.main()
