# The Daily Line Video Engine — V-21 Multi-Sport / Multi-Platform Scaling V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Ensure MLB, NFL, NCAAF, NBA, NCAAB, NHL, soccer, and future sports can share the engine without TDLA/DLVE acquiring sport-specific prediction logic.

## 2. Generic core

The video engine understands generic content primitives:
- matchup/entity labels;
- market/pick labels supplied by source;
- numeric/stat facts;
- approved explanation blocks;
- time/context facts;
- result/audit facts;
- visual emphasis tags;
- disclosure requirements.

Sport-specific semantics remain upstream.

## 3. Sport presentation packs

A sport may provide presentation metadata only, such as:
- sport label/icon;
- terminology mapping;
- preferred generic background classes;
- team abbreviation display policy;
- sport-safe templates;
- pronunciation lexicon extensions.

These packs cannot compute predictions or reinterpret sport facts.

## 4. Platform profiles

Platform differences are isolated in profile contracts: dimensions, limits, safe zones, caption/post metadata, cover behavior, and publication handoff. Templates remain semantic; platform layouts can adapt declaratively.

## 5. Account/channel policy

The same platform may have multiple Daily Line accounts/channels. Account policy controls branding, allowed sports, cadence, disclosures, language, and publishing windows without forking renderer code.

## 6. Queue isolation

Resource/concurrency policy prevents one sport/slate or long render from starving other time-sensitive content. Priority is policy-driven and observable.

## 7. Capacity planning

Forecast candidate volume by sport/calendar, variants per story, output profiles, render duration, asset generation, and analytics polling. Capacity planning uses measured p50/p95/p99 stage latency and cost.

## 8. Degraded modes

During major slates, the engine may prefer lower-cost/faster data-only templates while preserving content/QC standards. Degraded presentation is explicit metadata.

## 9. Tests

- one renderer with MLB/NFL/NCAAF synthetic facts;
- sport pack cannot add derived prediction;
- simultaneous slates/fair scheduling;
- multiple platform profiles;
- multiple accounts;
- locale expansion;
- load/concurrency tests.

## 10. Definition of done

V-21 is implementation-ready when adding a sport requires upstream contract conformance plus presentation metadata, not new orchestration or prediction branches inside DLVE.