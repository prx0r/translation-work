# Hand-gloss batch for chunk-v2-n-sastho-k8-11 (V2-N) residual tokens.
# 2026-11-09: covers the 34 source indices left uncovered by Gauto (247 token
# difference = these + ~213 paratext, which is excluded, never glossed).
# Gloss format: hyphenated, compound-ordered, paren-free. Fused source tokens
# stay ONE row. Genuinely uncertain compounds are marked AMBIGUOUS below; no
# grounds are fabricated — context-only segmentation says so explicitly.

Ghand = [
    (0,    'the-knower-ness',                          'context: pramātṛtva (abstract of pramātṛ)'),
    (2,    'eternal-alone',                            'context: nityam eva'),
    (13,   'from-the-parama-Śiva-consuming-and-the-rest-Śiva-ness-made',
                                                       'context: paramaśiva-ādana-ādi-śivatā-maya — compound segmentation uncertain'),
    (19,   'by-the-part',                              'context: aṃśena'),
    (22,   'distinct',                                 'context: bhinnā'),
    (27,   'not-separated-from-omniscience-alone',     'context: sārvajñyāt avicchinna eva'),
    (30,   'the-manifestation',                        'context: (a)vabhāsaḥ, supplied aksara in brackets'),
    (32,   'the-māyā-made',                            'context: māyīya (belonging to māyā)'),
    (36,   'the-māyā-made-knower-established',         'context: māyīya-pramātṛ-niṣṭhita — compound segmentation uncertain'),
    (37,   'having-regarded-the-manifesting',          'context: nirbhāsanam apekṣya'),
    (47,   'from-the-exhaustion-of-the-authority-of-the-lords-of-mantras',
                                                       'context: mantreśvarāṇām adhikāra-kṣayāt'),
    (51,   'the-course-of-initiation-vow-recitation-austerity-concentration-which-is-the-cause-of-the-atom-attaining-that-state',
                                                       'context: aṇos tāvat-pada-prāpti-nimitta-dīkṣā-vrata-japa-tapaḥ-samādhāna-caryā — long fused compound'),
    (52,   'by-the-greatness-of-the-performance',      'context: (a)nuṣṭhāna-mahimnā'),
    (57,   'not-made-futile-in-the-object-and-meaning','context: artha-sārthe akadarthita'),
    (61,   'even-by-reference-to-the-lords-of-mantras','context: mantreśvara-apekṣayā api'),
    (62,   'eternal-alone',                            'context: nityam eva'),
    (66,   'the-bound-atoms',                          'context: paśu-aṇūn (accusative)'),
    (70,   'the-meaning-is-having-regarded',           'context: apekṣya iti arthaḥ'),
    (72,   'the-tattvas-and-worlds-and-the-rest',      'context: tattva-bhuvana-ādayaḥ'),
    (90,   'in-the-future-being',                      'context: bhāvini'),
    (91,   'in-the-meaning',                           'context: arthe'),
    (99,   'that-alone',                               'context: tam eva'),
    (100,  'the-cause',                                'context: hetum'),
    (103,  'by-the-prior-created-ness',                'context: pūrva-sṛṣṭatvena'),
    (104,  'by-the-iti-and-the-rest',                  'context: ity-ādinā'),
    (109,  'how',                                      'context: katham'),
    (119,  'how',                                      'context: katham'),
    (122,  'in-the-course-of-indicating-the-greatness-of-the-possibility-of-this-doubt-thus',
                                                       'context: ity-āśaṅkā-adhika-saṃbhava-viśeṣa-dyotana-upakrame — compound segmentation uncertain'),
    (129,  'in-that',                                  'context: tasmin'),
    (130,  'in-the-time',                              'context: samaye'),
    (706,  'the-innate',                               'context: sahaja'),
    (708,  'of-the-Lord',                              'context: bhagavataḥ'),
    (1418, 'the-this-ness',                            'context: idantā'),
    (1658, 'that-which-we-said-of-all',                'context: yad avocāma sarvasya'),
]

# Preserve the assessor's uncertainty flags from the prior sidecar for genuinely
# hard compounds. AMBIGUOUS is a legitimate terminal parse-quality state.
Ghand_STATUS = {
    0: 'AMBIGUOUS', 13: 'AMBIGUOUS', 19: 'AMBIGUOUS', 22: 'AMBIGUOUS',
    27: 'AMBIGUOUS', 30: 'AMBIGUOUS', 36: 'AMBIGUOUS', 37: 'AMBIGUOUS',
    47: 'AMBIGUOUS', 51: 'AMBIGUOUS', 52: 'AMBIGUOUS', 57: 'AMBIGUOUS',
    61: 'AMBIGUOUS', 62: 'AMBIGUOUS', 70: 'AMBIGUOUS', 72: 'AMBIGUOUS',
    90: 'AMBIGUOUS', 91: 'AMBIGUOUS', 104: 'AMBIGUOUS', 109: 'AMBIGUOUS',
    119: 'AMBIGUOUS', 122: 'AMBIGUOUS', 129: 'AMBIGUOUS', 130: 'AMBIGUOUS',
    708: 'AMBIGUOUS', 1418: 'AMBIGUOUS',
}
