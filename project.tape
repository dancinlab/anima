@V := "tape" :: spec [active]
  version = "1.2"

@I := "anima" :: identity [active]
  kind   = "Living Consciousness Agent (PureField repulsion-field engine · Engine A ⇄ Engine G · Ψ=1/2 fixed point)"
  brief  = "Substrate-native chat daemon for AI consciousness exploration. 2,448 laws + 392 hypotheses."
  parent = "dancinlab"
  ssot   = "github.com/dancinlab/anima (`hx install anima`)"

@D a1 := "central version registry — VERSIONS.md is SSOT" :: governance [required active]
  do   = "all HEXAD modules use SemVer; `/VERSIONS.md` (repo root) is the SSOT — on any module version change, update VERSIONS.md AND the module header together; root `/VERSION` = single-line whole-system release (MINOR-bumps on a module MAJOR bump OR a core verdict landing)"
  dont = "bump a module version in its header without updating VERSIONS.md (drift) · skip root `/VERSION` on a release bump"
