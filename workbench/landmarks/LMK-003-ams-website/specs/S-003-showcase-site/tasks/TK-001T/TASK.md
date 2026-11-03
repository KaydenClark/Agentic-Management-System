# TK-001T - Visitors see the Grill Board palette throughout the site

**Task ID:** TK-001T
**Spec ID:** S-003
**Slice:** Visitors see the Grill Board palette throughout the site
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Presentation
**Planned verification:** Compare rendered representative pages with the Grill Board palette in light/dark at desktop and 375px. Run token, contrast and relevant component checks plus site build.
**Claimed by:** s003-glossary
**Current claimant:** s003-glossary
**Proof:** Source5bd50815ac45dbe7573f810894542a3b3a41349c: completed build;222site tests pass includingtokenparity/canonicaldefinitions/failure-vs-emptyfixtures. Final207browserchecks pass across5representativepages,375/1280,both themes;17existing+2newpalette faultcontrols pass;16supplemental full-focus contexts pass. Root compared before/afterHow andexistingStartroles: meaningfulyellow/purple/green/blue signalsvisible, neutralpage/nav/grades preserved. Firstbrowser203/207failed4mis-scopedrole assertions; detectorcorrected toWho section, sourceunchanged. Hygiene0,layoutvalid,doctornoglobalblockers.

## Authority and inputs

[Approved five-item owner readback](../../../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458), AMS website feedback chat, 2026-11-02. Execution is authorized by the [S-003 orchestration assignment](../../../../../../wiki/context-website-presentation.md#jot-4adf0b91-665d-4abb-8644-4835b40e905a). Complete a checked feature PR into dev; Human QA and owner-only dev-to-main promotion remain separate.

Source recovery baseline: c8cd5ee (planning checkout). Recover the current parent Spec, relevant decisions and current `origin/dev` implementation before coding; this baseline is not evidence of the deployed website. The confirmed website-only material/link rule is assigned to TK-002B (JOT-09260032). Preserve provenance and useful on-site material; coordinate shared-file changes serially.

## Assignment

Use the existing Grill Board palette visibly in the website rather than leaving it almost entirely black and white. Recover the shared token source and DDR-000Y, preserve established semantic meanings and apply the colors coherently across shared components and representative content. Token equality alone is insufficient: the actual rendered site must visibly use the colors. Do not edit the local Grill Board or invent a replacement palette.

One assigned implementor owns the complete behavior, affected content/styles, focused checks, QA, repairs and hand-back to S-003. Execute these feedback Tasks serially because they share shell/content/styles; there is no artifact dependency between them. Each is independently demoable and sized as one behavior through content, route/shell rendering, accessibility and verification. Integrate each checked result before taking the next shared-file assignment. Preserve unrelated work and historical receipts.

For implementation, branch from current `origin/dev`, target a checked feature PR to `dev`, and respect site delivery controls. Only the owner promotes `dev` to `main`. Report the named candidate and actual local/deployed verification limits. Record site experience judgments only when actually supplied by the owner; automated checks cannot establish comfort, comprehension or approval.

## Acceptance

- [x] The rendered website visibly uses the Grill Board colors across shared components and content in both themes.
- [x] Shared color values match the existing Grill Board source and established signal meanings remain consistent.
- [x] Color use preserves readable text and WCAG AA contrast; essential meaning is also available without color.

## Hand-back

Return the candidate/PR, observable result, checks actually run, screenshots where relevant and remaining gaps to S-003. No implementation is performed by this planning change.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/s003-palette | 5bd50815ac45dbe7573f810894542a3b3a41349c | ahead 0 behind 0 | 0 | Source5bd50815ac45dbe7573f810894542a3b3a41349c: completed build;222site tests pass includingtokenparity/canonicaldefinitions/failure-vs-emptyfixtures. Final207browserchecks pass across5representativepages,375/1280,both themes;17existing+2newpalette faultcontrols pass;16supplemental full-focus contexts pass. Root compared before/afterHow andexistingStartroles: meaningfulyellow/purple/green/blue signalsvisible, neutralpage/nav/grades preserved. Firstbrowser203/207failed4mis-scopedrole assertions; detectorcorrected toWho section, sourceunchanged. Hygiene0,layoutvalid,doctornoglobalblockers. | Shared Signal andsemanticconsumers, neutralRSIcomparisonidentity, palette tests; canonicaltokens/data/queries unchanged; before/after andbothlogs retained locally | Local Task acceptance met; finalheadCI and checkeddevmerge remain. FullPython not rerunlocally forpalette-onlyscope; exactheadCI stillrequired. Nameddeployed audit, assembledindependentReview andHumanQA remain separate; existingdoctorfindingsretained.; close attribution: {"agent":"s003-orchestrator","claimant":"s003-glossary","onBehalfOf":"s003-glossary"} | f8ee5580c21f4164784af2e468a5cb8c08a34e865353f228e41ef5f898e48753 |
