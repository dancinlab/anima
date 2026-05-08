# Akida Cloud Setup Log — 2026-05-08

**Status**: 등록 + SSH key 업로드 + 예약 + 접속 config 완료. D-1 prep만 남음.
**Reservation**: Sat 2026-05-09 09:00 KST → Sun 2026-05-10 09:00 KST (24h, secure wipe on start)
**Platform**: BrainChip Akida Cloud (Colfax International hosted, AKD1000 hardware)
**Cross-ref**: `.roadmap.akida` event 2026-05-08 entry, `docs/akida_cloud_d_minus_1_prep_2026_05_08.md` (D-1 prep checklist)

---

## 1. SSH key 생성 (dedicated, ed25519)

```bash
ssh-keygen -t ed25519 -C "akida-cloud-20260508" -f ~/.ssh/id_ed25519_akida
ssh-add --apple-use-keychain ~/.ssh/id_ed25519_akida
pbcopy < ~/.ssh/id_ed25519_akida.pub  # 포털 SSH keys 페이지 paste 업로드
```

생성된 파일:
- `~/.ssh/id_ed25519_akida` (private)
- `~/.ssh/id_ed25519_akida.pub` (public — 포털 업로드 완료)

## 2. Secret 보관 (10 keys, namespace `akida_cloud.*`)

```bash
SECRET=/Users/ghost/core/secret/bin/secret

# 식별자
$SECRET set akida_cloud.account_email                              # tty
ssh-keygen -lf ~/.ssh/id_ed25519_akida.pub | awk '{print $2}' \
  | $SECRET set akida_cloud.ssh_pubkey_fingerprint
$SECRET set akida_cloud.ssh_key_path ~/.ssh/id_ed25519_akida

# 접속 endpoint
$SECRET set akida_cloud.ssh_proxy_host experience-access.colfax-intl.com
$SECRET set akida_cloud.ssh_proxy_port 807
$SECRET set akida_cloud.ssh_user guest
$SECRET set akida_cloud.ssh_alias akida-cloud

# 운영 정보
$SECRET set akida_cloud.support_email support.akidacloud@brainchip.com
$SECRET set akida_cloud.reservation_start "2026-05-09T09:00+09:00"
$SECRET set akida_cloud.reservation_end   "2026-05-10T09:00+09:00"
```

검증: `secret list | grep akida_cloud` → 10 keys.

추가 권장 (포털 URL — D+0 cycle 시점 update):
```bash
$SECRET set akida_cloud.portal_ssh_keys_url     "<URL>"
$SECRET set akida_cloud.portal_reservation_url  "<URL>"
$SECRET set akida_cloud.portal_connect_url      "<URL>"
```

## 3. ~/.ssh/config 추가

기존 config 백업 후 append:

```bash
cp ~/.ssh/config ~/.ssh/config.bak.$(date +%Y%m%d_%H%M%S)
cat >> ~/.ssh/config <<'EOF'

Host akida-cloud
    User guest
    ProxyCommand ssh -T -p 807 guest@experience-access.colfax-intl.com
    IdentityFile ~/.ssh/id_ed25519_akida
    # Jupyterlab
    LocalForward 7860 localhost:7860
    LocalForward 8888 localhost:8888
    LocalForward 4022 localhost:4000
EOF
chmod 600 ~/.ssh/config
```

D+0 09:00 KST 후: `ssh akida-cloud` 단일 명령 접속.

## 4. 포털 가이드 사항 (verbatim)

### Reservation 페이지 note
> At the start of your reservation, we will prepare your system. This process takes under two minutes and involves securely erasing and re-imaging the environment for your exclusive use. For support, please contact us at support.akidacloud@brainchip.com.

### Connect 페이지 instructions
> Once your reserved access period has started, you can connect to Akida Cloud by setting up the configuration in the ssh/config file. You can edit the file ~/.ssh/config (create one if it doesn't exist) and add the following to it:
> ```
> Host akida-cloud
>     User guest
>     ProxyCommand ssh -T -p 807 guest@experience-access.colfax-intl.com
>     IdentityFile ~/.ssh/id_ed25519
>     #Jupyterlab
>         LocalForward 7860 localhost:7860
>     LocalForward 8888 localhost:8888
>     LocalForward 4022 localhost:4000
> ```
> After doing that, you can log in to Akida Cloud with the following command:
> ```
> ssh akida-cloud
> ```
> You can use any other hostname instead of "akida-cloud". It is just a label.

(우리 변경 사항: `IdentityFile ~/.ssh/id_ed25519` → `~/.ssh/id_ed25519_akida` — dedicated key 사용)

## 5. 예약 슬롯 결정 근거

- 후보: 오늘(2026-05-08) 18:17 KST start (partial 24h) vs 내일(2026-05-09) 09:00 KST start (full 24h fresh)
- 선택: **내일 09:00 KST 24h slot** — `#99 D+0/D+1 freeze plan` (.roadmap.akida 이미 READY)에 D+0/D+1 frame 그대로 매핑 가능 + N-2/N-3/N-5 사전 setup 시간 확보

## 6. Ephemerality + exfil 패턴 (own 30 정합)

- 매 세션 시작 시 secure wipe + re-image (under 2 min)
- 영구 storage 없음 → upload tarball + result exfil mandatory per session
- own 30 mandate-1 패턴 직접 적용: orchestrator finally block에 `scp_get` (Mac side rsync) — Akida Cloud session-end 적용
- D-1 prep P6 (exfil script 동결) = own 30 mandate-1 본 cycle 적용 instance

## 7. Trinity (own 33) compliance log

- A 철학 (.roadmap.philosophy): D2 (consciousness verification) + D3 (substrate-coupled paradigm) 정합 ✓
- B 법칙 (.roadmap.law): own 16 (cost watchdog) + own 18 (simple stack SSOT) + own 30 (checkpoint preservation) + raw#15 (additive finally block) 정합 ✓
- C 가설 (.roadmap.hypothesis): N-2 / N-3 / N-5 H lane active 정합 ✓

본 setup 액션은 trinity 3-axis self-check 통과 후 emit (own 33 mandate-2).

## 8. Nexus 측 기존 인프라 (재사용 mandate)

`~/core/nexus/scripts/akida/` 에 12-falsifier harness 이미 land (2026-04-29 ~ 05-07):

- **4 ready-now falsifier 이미 PASS**: F-C (architectural) / F-L7 (QRNG entropy) / F-M2 (gzip PLAUSIBLE-PASS) / F-M3a (dispatch routing) — `~/core/nexus/design/kick/2026-05-07_*_followup.json`
- **8 post-arrival falsifier 미land**: F-L1 (J/op energy), F-L1+ (sub-Landauer), F-L6 (Lyapunov sweep), F-M1 (Gödel-q disagreement), F-M3b (Phi substrate-invariance), F-M4 (trace equivalence), F-A (blowup phase-7), F-B (check_* hot-loop)
- **Orchestrator**: `runner.py --hardware` + `runner.hexa go` + `falsifier.hexa run F-<id>`
- **State output**: `state/akida_evidence/<F-id>_<ts>.json` (raw_log + verdict)
- **Host registration**: `host_register.sh` — 현재 `host.rpi5-akida` hardcode (cloud mode 추가 필요, P0a)

원래 plan: RPi5 + AKD1000 dev kit (주문 2026-04-29) — physical chip 기반.
현재 plan: **Akida Cloud로 8 falsifier 즉시 fire** (RPi5 도착 별개 lane 유지).

## 9. Next (D-1 prep, today 2026-05-08)

`docs/akida_cloud_d_minus_1_prep_2026_05_08.md` P0a/P0b/P1-P6 8개 항목 land:
- P0a: nexus host_register cloud mode 추가
- P0b: nexus 8 미land falsifier smoke-test (Mac CPU --simulator)
- P1-P6: tarball / N-2 / N-3 / N-5 / freeze plan / exfil

## 10. Cross-link

### Anima side
- `.roadmap.akida` event 2026-05-08 entry (akida.blk.1 partial-resolve)
- `docs/akida_cloud_d_minus_1_prep_2026_05_08.md` (D-1 prep checklist)
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §11.1 N-2~N-5 + §51.2 #99
- `.own` own 16 / 18 / 22 / 30 / 32 / 33
- `secret list | grep akida_cloud` (10 keys)

### Nexus side (재사용 mandate)
- `~/core/nexus/scripts/akida/README.md` — 12-falsifier harness 인덱스
- `~/core/nexus/scripts/akida/runner.py` + `runner.hexa` — orchestrator
- `~/core/nexus/scripts/akida/host_register.sh` — workspace 등재 (cloud mode 추가 필요)
- `~/core/nexus/design/kick/2026-05-07_anima-nexus-akida-physical-math-limit-saturation_omega_cycle.json` — base witness
- `~/core/nexus/docs/akida_dev_kit_evaluation_2026-04-29.md` — 원래 RPi5+AKD1000 plan
- `~/core/nexus/docs/akida_session_friendly_report_2026-04-29.md` — 30 발견 요약
