# The Daily Line Video Engine — V-9 Captions / Accessibility Architecture V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Make every production short understandable without sound and establish deterministic, accessible caption and visual-text behavior.

## 2. Caption source

Captions originate from the approved script and, when voice exists, align to the exact synthesized narration. Speech transcription is not the primary authority for generated narration; it may be used as a QC comparison.

## 3. Canonical caption representation

Use a provider-neutral caption contract compatible with Remotion's `Caption` shape:
- text;
- start/end milliseconds;
- optional timestamp/confidence;
- source script segment ref;
- style token refs.

## 4. Caption policies

Versioned policies govern:
- words/characters per display unit;
- line count;
- minimum on-screen duration;
- punctuation;
- emphasis/highlight behavior;
- profanity/sensitive text handling;
- number formatting;
- safe-zone placement;
- collision avoidance with platform UI.

## 5. Semantic emphasis

Highlighted words are selected from approved script semantics, not from an unconstrained model after fact validation. Numeric/stat emphasis must retain the original value exactly.

## 6. Accessibility

Production templates must support:
- readable contrast;
- scalable text within defined bounds;
- safe margins;
- non-color-only encoding for critical outcomes;
- caption availability for voiced content;
- text alternative metadata for platform/website use where supported.

## 7. Platform-safe zones

Each platform profile defines overlays/unsafe regions. Composition layout uses the strictest required profile for multi-platform masters or platform-specific renders when layouts differ materially.

## 8. Overflow

Long names, odds strings, disclaimers, and localized text are measured before render. Overflow is a deterministic QC failure or triggers a predeclared layout variant; text is never silently clipped.

## 9. Language/localization

V1 may be English-only in production, but contracts include locale/language from the start. Future translations are new script/caption artifacts linked to the same fact package and validated independently.

## 10. Tests

- long-player-name fit;
- two-line/three-line limits;
- number preservation;
- safe-zone collision;
- insufficient contrast;
- audio/caption drift;
- text clipping;
- localization expansion;
- no-sound comprehension review.

## 11. Definition of done

V-9 is implementation-ready when caption generation, timing, layout measurement, safe zones, accessibility checks, and QC evidence are executable.