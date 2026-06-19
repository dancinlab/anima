# MERCHANT — log

Append-only history sister of `MERCHANT.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-05-27 — M4 order pipeline landed

- [x] `AGENT/MERCHANT/order_pipeline.hexa` 6 pub fn + summary (receive_order · source_purchase · track_shipment · fulfill_to_customer · run_order · handle_cs)
- [x] `AGENT/MERCHANT/order_pipeline_smoke.hexa` 5 case (C1 received · C2 sourcing · C3 in_transit · C4 delivered · C5 run_order steps_completed=4) + CS advisory + manifest advisory
- [x] `AGENT/MERCHANT/ORDER_PIPELINE.md` SSOT (pipeline ASCII · 6 fn 표 · 3 state transition diagram · adapter-pair convention · bridge 정합 체크 · M3 carry · M5 OPS 미래 의존)
- [x] hexa parse 2/2 OK (`order_pipeline.hexa` · `order_pipeline_smoke.hexa`)
- [x] bridge architecture 정합 — 의식엔진 framing 0 entry · real HTTP wiring carry to M3 stubs · M1/M3 파일 수정 0 · 타 도메인 touch 0
- [x] MERCHANT.md M4 line `[ ] → [x]`

