# ADR-0009 — Rights-First Media Provenance and Non-Documentary Generative Visuals

Date: 2026-09-08
Status: ACCEPTED

## Context

DLVE will use first-party graphics, generated images, stock media, music, SFX, and potentially authentic team/athlete media. Production automation cannot assume that internet availability, provider output, cache presence, or successful generation grants publication rights. Generated visuals can also mislead if they appear to document a real event.

## Decision

Every production media asset is represented by immutable provenance and rights evidence. Publication fails closed when exact-use rights are unknown/expired/restricted.

AI-generated/generic media may illustrate a concept but is not documentary evidence of a specific game, injury, quote, weather event, score, or athlete action. Identifiable people, team/league marks, voices, and restricted libraries require explicit policy/rights authority.

Cached/derived assets retain and revalidate parent restrictions.

## Alternatives considered

1. Use freely accessible internet images — rejected because accessibility is not rights authority.
2. Generate realistic athlete/event imagery for all videos — rejected as unnecessary and capable of misleading viewers or increasing rights/policy risk.
3. Use only first-party vector graphics — safe but unnecessarily restrictive; licensed/generated generic media is allowed with provenance.

## Consequences

- Asset ingestion has more metadata/QC work.
- Reusable first-party/generic assets become economically valuable.
- Publication can be blocked by rights uncertainty.
- Historical posts remain explainable.

## Compatibility

Aligns with V-0/V-4/V-7/V-11/V-13/V-18/V-23 and future TDLA A-18/A-20.

## Validation required

Rights-expiry, platform restriction, derivative lineage, generated documentary-misrepresentation, watermarked preview, and identifiable-person/mark scenarios are included in DLVE architecture and implementation tests.