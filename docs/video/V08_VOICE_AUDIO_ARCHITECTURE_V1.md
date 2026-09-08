# The Daily Line Video Engine — V-8 Voice / Audio Architecture V1

Status: DOCUMENTED — REVIEW PENDING
Date: 2026-09-08

## 1. Purpose

Define production-safe narration, music, sound-effect, loudness, mixing, and fallback behavior.

## 2. Audio layers

- narration/voiceover;
- music bed;
- transition/brand SFX;
- data/UI SFX;
- optional ambient layer;
- optional source clip audio when rights permit.

## 3. VoiceProfile

A versioned `VoiceProfile` specifies:
- provider/engine family;
- voice identity reference;
- locale/language;
- speaking-rate bounds;
- pitch/style controls when supported;
- pronunciation dictionary version;
- disclosure/policy class;
- platform suitability;
- fallback voice profile.

Provider-native IDs are replaceable references, not canonical DLVE identity.

## 4. Pronunciation authority

Sports names, team abbreviations, stadiums, betting notation, and acronyms use a versioned pronunciation lexicon. User-visible text remains unchanged while phonetic hints are renderer/provider metadata.

## 5. AudioArtifact

Retain:
- script digest;
- voice profile/version;
- provider/model/version;
- synthesis request digest;
- audio hash;
- measured duration;
- sample rate/channels/codec;
- generation timestamp;
- moderation/result metadata;
- timing alignment evidence when available.

## 6. Music/SFX rights

All music and SFX require the V-7 rights gate. Platform-provided libraries may have platform-specific restrictions and cannot be assumed portable across TikTok, Instagram, YouTube, X, or website use.

## 7. Mixing policy

Narration intelligibility is primary. Music ducks under narration. Brand stings are short and cannot mask the hook or recommendation. Mix policy is versioned and testable.

## 8. Loudness / peaks

Production outputs use target loudness/true-peak ranges defined per platform profile. Exact numeric targets belong to versioned platform configuration because platform guidance may change.

## 9. No-voice fallback

A valid video may render without narration only when the selected template supports `caption_primary=true`. The fallback is explicit and receives a distinct creative/render variant identity.

## 10. Synthesis failure

Retry/fallback must preserve the same script authority. A voice provider failure cannot authorize script alteration or a different factual message.

## 11. Impersonation / voice cloning

No voice cloning or imitation of athletes, broadcasters, public figures, or other people without explicit rights/consent authority. Default voices are licensed synthetic voices or first-party recorded voices.

## 12. Synchronization

Voice timing is authoritative for caption timing when voiceover exists. Scene timing may adapt to measured narration duration within template constraints; factual content may not be dropped silently to fit.

## 13. Tests

- pronunciation lexicon;
- music ducking;
- clipping/peak detection;
- missing narration fallback;
- provider failover with identical script digest;
- rights-restricted music rejection;
- timing overflow rejection;
- voice-profile version provenance.

## 14. Definition of done

V-8 is implementation-ready when TTS abstraction, profile contracts, rights integration, audio QC, timing behavior, and fallback paths are implemented and certified.