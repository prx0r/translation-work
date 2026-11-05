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


if __name__ == '__main__':
    unittest.main()
