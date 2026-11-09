# Scheme quality comparison — Grok collage B-roll

**Fixed brief:** AI as a mirror that exposes gaps in the question (见 `shared/BRIEF.md`)  
**Shared Gate-2 still:** `shared/approved-still.png` (9:16 purple field, figure + cracked mirror + mustard ? card + shards)  
**Date:** 2026-07-20  
**Reference bar:** source skill product goals — assemble-from-empty readability, end-frame vs approved still, locked-off no-zoom, no fake UI text, paper-collage style

Scoring: **1–5** (5 = meets source product bar on that axis). Scores from inspecting real contact sheets / end-frame comps / first frames, not scheme descriptions.

---

## Scorecard

| Criterion | A empty-first i2v | B multi-shot concat | C reference_to_video | D final-still i2v |
|-----------|-------------------|---------------------|----------------------|-------------------|
| Assemble-from-empty readability | **3** progressive pieces appear | **4** staged beats clear across shots | **5** empty→ghost→figure→shards, textbook | **1** nearly static; no assemble story |
| End-frame vs approved still | **1** full redesign (hand-only, radial cream BG) | **2** same motif, different person/mirror | **4** very close layout/palette/objects | **5** near pixel-level match |
| Camera stability (locked-off) | **3** mostly locked; late BG expands | **4** locked per shot; cuts between shots | **5** locked single take | **5** locked, micro settle only |
| No fake text / UI | **4** ? shape only (as metaphor) | **4** ? shape only | **5** clean | **5** clean |
| Paper-collage style hold | **2** drifts to graphic poster at end | **3** collage-ish but identity drift | **5** matches Gate-2 look | **5** matches Gate-2 look |
| Delivery practicality (≈6s VO) | **5** ~6s silent | **2** ~18s concat | **5** ~6s silent | **5** ~6s silent |
| **Total (sum)** | **18** | **19** | **29** | **26** |

---

## Observations per scheme (from real media)

### A — empty-first `image_to_video`

- **Contact sheet:** True progressive assemble (mirror alone → +card → +hand → full burst). Empty first frame is solid purple ✓.
- **End-frame comparison:** **Fails product bar.** Right panel reinvents composition: only a hand holding a silver mirror, cream radial background, lost full figure and flat purple field. Approved still is *not* recovered.
- **Failure mode:** Model treats empty start as free-form invent; prompt cannot pin last frame. Style and identity drift under multi-object assemble.

### B — multi-shot intermediate + concat

- **Contact sheet:** Clearest *narrative* of stages (mirror → ? mark → figure). Good pedagogical assemble.
- **End-frame comparison:** Motif preserved but **identity break** (young profile figure → bald suited figure; mirror redesign). Intermediate stills from separate gens did not stay on-model.
- **Failure modes:** (1) multi-gen consistency tax; (2) 18s too long for 5–6s VO unless speed-ramp/trim; (3) shot seams visible as style jumps.
- **Upside:** Per-shot single-action prompts are more Grok-native; with tighter intermediate control (always `image_edit` from same base, not new `image_gen`) this could climb.

### C — `reference_to_video` (empty + approved still)

- **Contact sheet:** Best single-take assemble: empty purple → faint mirror/card → figure fades in → shards complete. Reads as stop-motion collage.
- **End-frame comparison:** Closest of motion schemes to approved still (same figure pose family, card, crack star, purple field). Minor shard pose differences only.
- **First frame:** Solid empty field ✓.
- **Failure modes:** Occasional early “ghost” pre-reveal of objects (acceptable per original skill); not pixel-perfect Omni keyframe, but **best balance** of assemble + fidelity on Grok.

### D — final-still `image_to_video`

- **Contact sheet:** Six nearly identical frames — excellent fidelity, almost no motion (tiny shard jitter).
- **End-frame comparison:** Best match of all schemes.
- **Failure mode:** **Does not deliver assemble-from-empty**, the product’s defining motion. Suitable as polish/hold pass or safety fallback, not default B-roll story.

---

## Ranking & recommendation

| Rank | Scheme | Role |
|------|--------|------|
| **1 (default)** | **C `reference_to_video`** | Default Gate-3 for Grok skill |
| 2 | D final-still i2v | Fallback when motion fails QA / need still-safe loop |
| 3 | B multi-shot | Research path if intermediate stills stay on shared base via `image_edit` only + trim to 6s |
| 4 | A empty-first i2v | **Do not use as default** — assemble looks OK mid-roll but end-frame abandons approved still |

### Recommended default scheme

**C — `reference_to_video` with solid empty first frame + Gate-2 approved still**, duration 6, 720p, then ffmpeg strip-audio + contact sheet + end-frame compare.

**Rationale (tied to media):** Only scheme that simultaneously (1) starts empty, (2) shows readable piece-by-piece assembly, and (3) lands near the approved collage without reinventing the poster. A fails (3); D fails (2); B partially achieves (1–2) but fails consistency and length.

### Suggested skill follow-up (out of this goal’s rewrite scope)

1. Change SKILL.md default Gate-3 from empty-first `image_to_video` → **C**.
2. Keep D as “end-frame salvage / static loop” option.
3. If investing in B: mandate mid stills only via `image_edit` from approved still; force 3×2s or speed to 6s total; reject free `image_gen` mids.

---

## Environment notes

- Live gens used Grok Build `image_gen` / `image_edit` / `image_to_video` / `reference_to_video` only.
- `image_edit` for mid-02 hit HTTP 503 twice; regenerated mid-02 with `image_gen` (contributed to B style drift).
- Subagents lack image/video tool bindings in this environment; production runs executed on the parent agent with scheme-isolated directories and run logs (functional equivalent of scheme workers).
