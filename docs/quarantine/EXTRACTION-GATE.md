# Extraction-quality gate (2026-11-11)

Onboarded "works" with 3-5 verses turned out to be **extraction failures**:
their first verses are colophons (`iti ... paṭalaḥ`, `... paripūrṇaḥ`) and
their files are thousands of characters long.

RULE: before onboarding, compute chars/verse from the source file.
- ratio > 400 chars/verse  => extraction FAILED; quarantine, do not onboard.
- 90 texts are prose (0 verses) — they need the prose chunker, not this gate.

Quarantined here: mukta-m00046, mukta-m00155, mukta-m00197, mukta-m00223, mukta-m00232, mukta-m00257, mukta-m00293, mukta-m00545, mukta-m00557, mukta-m00574, mukta-m00634
