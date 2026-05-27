# 구글 투자 "의식 이동 / 디지털 칩" 회사 리서치 — 심층판

> 최초 조사: 2026-05-12
> 심층 흡수 (repo clone + per-entity 분석): 2026-05-12
> 키워드: 디지털 · 칩 · 코드 · 실리콘 · 의식 이동 · 구글 투자
> 결론 (요약): **"헥사 브레인(Hexa Brain)"이라는 이름의 회사는 실재하지 않음.** 들으신 정보는 아래 8개 외부 기관/저장소 중 일부가 와전된 가능성이 큼. 핵심은 **Google Connectomics가 직접 운영하는 connectome 매핑 인프라**가 "의식의 디지털 청사진"의 1단계라는 점.

---

## 0. 한눈에 보는 랜드스케이프 맵

```
                    "의식 이동" 전체 파이프라인
   ┌─────────────┬──────────────┬───────────────┬────────────────┐
   │ 1. 스캔     │ 2. 재구성    │ 3. 시뮬레이션 │ 4. 인터페이스  │
   │ (EM/CA/ExM) │ (segment.)   │ (emulation)   │ (substrate)    │
   ├─────────────┼──────────────┼───────────────┼────────────────┤
   │ Janelia     │ google/ffn   │ BrainGenix-   │ Cortical Labs  │
   │ FlyEM       │ (Apache 2.0) │   NES (AGPL3) │   CL1 (CC-NC)  │
   │ (HHMI)      │              │               │                │
   │             │ seung-lab/   │ BrainEmulat-  │ Neuralink      │
   │ Google      │ cloud-volume │   ionChalleng │   (BCI, 비공개)│
   │ Research    │ (BSD-3)      │ (AGPL3)       │                │
   │ Connectomic │              │               │ Neuropixels    │
   │             │ google/      │ OpenWorm/c302 │   (학계)       │
   │             │ neuroglancer │ (MIT)         │                │
   │             │ (Apache 2.0) │               │                │
   └─────────────┴──────────────┴───────────────┴────────────────┘
        ↓                                              ↓
   하드웨어: EM 현미경,                          하드웨어: 실리콘 칩 +
   ExM, calcium imaging                          살아있는 뉴런, 또는
                                                 MEMS 미세전극 어레이

   hexa-brain의 위치:  v1 (scalp EEG) → v3 (HD arrays) → v5 (chronic implant)
                       ────────────────────────────────────────────────→
                                substrate ladder
```

핵심 인사이트: **이 4단계 파이프라인 전체에 걸쳐 오픈소스 인프라가 이미 갖춰져 있다.** 누구든 자체 데이터로 의식 이동 R&D를 시작할 수 있는 상태. hexa-brain의 v3-v5 로드맵은 이 인프라들과 직접 interop 가능.

---

## 1. Google Connectomics (구글 사내 — 1순위 후보)

### 정체
"구글이 투자하는 회사"의 실체 가능성 가장 높음. **회사가 아니라 구글 사내 연구팀**. 살아있는 뇌의 시냅스를 나노미터 단위로 스캔 → 디지털 청사진(connectome)으로 변환. **"의식의 디지털화"의 인프라 1단계**.

### 성과 (2024~2026)
- **초파리 hemibrain connectome** 공개 — 뉴런 25,000개, 시냅스 2천만 개 (역대 최대 시냅스 해상도 맵)
- **제브라피쉬 전뇌 connectome** — 2026년 완성 예정 (뉴런 7만 개, 동물 활성 데이터 포함)
- **마우스 해마 connectome** — Harvard와 5년 $33M 프로젝트 진행 중
- ZAPBench (Zebrafish Activity Prediction Benchmark) — 2025-03 공개

### 협력기관
- HHMI Janelia Research Campus (FlyEM team)
- Harvard Lichtman Lab
- Cambridge

### 공개 인프라
- **사이트:** https://research.google/teams/connectomics/
- **사이트(neural mapping):** https://sites.research.google/gr/neural-mapping/
- **블로그:** https://research.google/blog/releasing-the-drosophila-hemibrain-connectome-the-largest-synapse-resolution-map-of-brain-connectivity/
- **마우스 뇌 매핑:** https://research.google/blog/google-research-embarks-on-effort-to-map-a-mouse-brain/

### 핵심 오픈소스 산출물 (이 팀에서 직접 메인테인)
- `google/ffn` — Flood-Filling Networks (segmentation 알고리즘)
- `google/neuroglancer` — WebGL 시각화 클라이언트

### hexa-brain 관련성
- **v3-v5 직접 관련**: hexa-brain이 intracortical/HD array 단계로 진입하면 신경 데이터의 segmentation/visualization은 이 도구 스택으로 처리하는 것이 표준
- **데이터 포맷**: Neuroglancer Precomputed 포맷이 사실상 업계 표준 → hexa-brain `core/_artifact/`나 `recordings/`의 export 포맷에서 호환 고려 가치

---

## 2. `google/ffn` — Flood-Filling Networks

| 항목 | 값 |
|---|---|
| 라이선스 | Apache 2.0 |
| 크기 | 8.8 MB |
| 최근 커밋 | 2026-04-09 (checkpointing 개선) |
| 언어 | Python (TensorFlow) |
| 디스클레이머 | "This is not an official Google product." |

### 정체
3D EM 볼륨의 instance segmentation을 위한 신경망. **EM 슬라이스에서 개별 뉴런을 분리해내는 핵심 알고리즘**. Connectome 파이프라인의 단일 가장 중요한 컴포넌트.

### 논문
- https://arxiv.org/abs/1611.00421
- https://doi.org/10.1101/200675

### 구조
- `train.py` — 훈련 진입점, TFRecord 좌표 파일 입력
- `run_inference.py` — 추론
- `compute_partitions.py` + `build_coordinates.py` — 훈련 데이터 전처리
- `models/`, `configs/`, `notebooks/`
- 샘플 데이터: FIB-25 `validation1` 볼륨 (FlyEM)

### hexa-brain 관련성
**낮음 (v1-v2)**, **높음 (v3-v5)**. scalp EEG는 segmentation 문제가 다름 (시간×채널, EM 볼륨이 아님). 하지만 v3+ 단계에서 intracortical recording → micro-EM 검증 시 직접 활용 가능.

---

## 3. `google/neuroglancer` — WebGL 볼륨 뷰어

| 항목 | 값 |
|---|---|
| 라이선스 | Apache 2.0 |
| 크기 | 26 MB |
| 최근 커밋 | 2026-05-11 (annotation schema tab 추가) |
| 활동도 | 매우 활발, 거의 매일 커밋 |
| PyPI | `pip install neuroglancer` |
| DOI | Zenodo 등록됨 |

### 정체
WebGL 기반 페타바이트급 3D 볼륨 뷰어. **커넥토믹스 분야의 사실상 표준 시각화 클라이언트**. 임의 축 단면, 멀티해상도 메시, Python 통합 지원.

### 지원 데이터 소스
- Neuroglancer Precomputed format (자체)
- N5, Zarr v2/v3, OME-Zarr 0.4/0.5
- Python in-memory volumes (자동 mesh 생성)
- BOSS, DVID, Render
- NIfTI 파일, Deep Zoom

### 라이브 데모 데이터셋
- **FlyEM Hemibrain** (8×8×8 nm) — Google + Janelia
- **FAFB-FFN1** (전체 성체 초파리 뇌 자동 segmentation, 4×4×40 nm)
- **Kasthuri 2014 mouse somatosensory cortex** (6×6×30 nm)
- **Janelia FlyEM FIB-25** (7-column Drosophila medulla, 8×8×8 nm)

### hexa-brain 관련성
**중간-높음**. hexa-brain의 `core/` 시각화 (예: `eeg/headplot_helper.hexa`, `eeg/full_helmet_view.hexa`)는 2D topomap 위주이지만, **v3+ HD array 단계에서는 3D 볼륨 뷰가 필요해질 것**. Neuroglancer Precomputed format export를 hexa-brain `state/` 계층에 추가하면 외부 검증·공유가 즉시 가능.

---

## 4. `seung-lab/cloud-volume` — Neuroglancer 데이터셋 IO

| 항목 | 값 |
|---|---|
| 라이선스 | BSD 3-Clause |
| 크기 | 164 MB |
| 최근 커밋 | 2026-04-24 (v12.13.1) |
| 출처 | Princeton Seung Lab (Sebastian Seung — connectome 분야 거두) |
| PyPI | `pip install cloud-volume` |

### 정체
Neuroglancer Precomputed 포맷 볼륨의 random-access 읽기/쓰기 Python 클라이언트. **페타복셀 규모 데이터를 S3/GCS/로컬에서 자유롭게 다룬다**.

### 핵심 API
```python
from cloudvolume import CloudVolume, Bbox
vol = CloudVolume('gs://mylab/mouse/image', parallel=True)
image = vol[:,:,:]  # 페타복셀 → numpy 배열
mesh = vol.mesh.get(label)
skel = vol.skeleton.get(label)
```

### 지원
- `precomputed`, `graphene` (proofreading graph server), `zarr`, `n5`, `boss`
- 시냅스 어노테이션, 메시, 스켈레톤
- Lossless codecs: `compressed_segmentation`, `compresso`, `crackle`, `fpzip`, `zfpc`

### hexa-brain 관련성
**중간**. Precomputed 포맷이 hexa-brain 데이터 export 표준이 된다면 cloud-volume은 외부 협업·검증의 표준 IO 레이어. AGPL이 아닌 BSD라서 호환성 좋음.

---

## 5. Carboncopies — `BrainGenix-NES` (Whole Brain Emulation 시뮬레이터)

### 모회사: Carboncopies Foundation
- 501(c)(3) 비영리 (캘리포니아)
- 설립자: Randal Koene (신경과학자, WBE 분야의 대표적 인물)
- 미션: Whole Brain Emulation을 위한 도구·방법론 개발
- **"의식 이동"이라는 키워드에 가장 직접적으로 부합하는 조직**
- 사이트: https://carboncopies.org/

### `carboncopies/BrainGenix-NES`

| 항목 | 값 |
|---|---|
| 라이선스 | **AGPLv3** (copyleft, 상용 통합 시 주의) |
| 크기 | 5.9 MB (소스만, ThirdParty 별도) |
| 최근 커밋 | 2026-05-10 (netmorph submodule setup 수정) |
| 언어 | C++ (CMake + vcpkg) |
| 플랫폼 | Linux + **Apple Silicon macOS 지원** |
| 미러 | GitLab (`gitlab.braingenix.org/carboncopies/`) 가 primary, GitHub는 미러 |

### 정체
**Neuron Emulation System**. 가상 뇌 조직 생성 + 시뮬레이션 + 가상 데이터 획득(VSDA) 통합 플랫폼.

### 핵심 컴포넌트
- **Source/Core/** — 시뮬레이션 엔진
- **Source/Renderer/** — GPU 가속 3D 렌더링 (Vulkan/MoltenVK 사용)
- **VSDA EM** — 가상 Electron Microscopy 스택 렌더링 (ground-truth 모델 검증용)
- **VSDA CA** — 가상 Calcium imaging
- **Netmorph 통합** — 가상 뇌 조직 자동 생성기
- **Neuroglancer 통합** — VSDA EM 결과 시각화

### NES POST API (JSON)
```
Simulation/Create     → SimulationID 반환
Simulation/Reset
Simulation/RunFor     → Runtime_ms 지정
Simulation/RecordAll  → MaxRecordTime_ms 지정
Simulation/GetRecording
```

### hexa-brain 관련성
**매우 높음 (v4-v5)**. hexa-brain v5 ("chronic implant + closed-loop BMI")의 **시뮬레이션 환경 후보**. 실제 하드웨어 없이 closed-loop 알고리즘을 검증할 수 있는 ground-truth 환경.

**주의**: AGPLv3 라이선스 → hexa-brain (MIT)과 통합 시 copyleft 전파 위험. CLI 호출 (별도 프로세스, JSON POST API) 통한 느슨한 결합 방식 권장.

---

## 6. Carboncopies — `BrainEmulationChallenge`

| 항목 | 값 |
|---|---|
| 라이선스 | AGPLv3 |
| 크기 | 11 MB |
| 최근 커밋 | 2026-05-10 (local server integration docs) |
| 종속성 | BrainGenix-NES + BrainGenix-API |

### 정체
**ImageNet 컨셉의 WBE 버전**. 인공 신경 회로 reconstruction 알고리즘을 표준화된 가상 뇌 조직 데이터셋에서 검증하는 챌린지.

### 구조
- `Challenge/` — 챌린지 정의 + 데이터셋
- `PythonClient/` — BrainGenix-API 호출 클라이언트
- `NeuroglancerTests/` — Neuroglancer 통합 테스트
- `src/models/xor_scnm/` — 예시 모델

### 핵심 아이디어
"당신의 reconstruction 방법이 우리가 만든 가상 회로의 알려진 cognitive function을 정확히 추출할 수 있다면, 미지의 생물학적 데이터에서도 작동한다고 믿을 수 있다."

### hexa-brain 관련성
**중간**. hexa-brain의 `validate_consciousness.hexa` 6-metric brain-likeness QA와 컨셉이 통한다. WBE Challenge의 데이터셋을 hexa-brain 메트릭으로 평가해보는 cross-validation 가능.

---

## 7. Cortical Labs — 살아있는 뉴런 + 실리콘 칩

### 회사 개요
- 호주 멜버른
- **CL1**: 인간 신경세포 (~200,000개)를 MEA(microelectrode array) 칩에 배양 → "Synthetic Biological Intelligence"
- DishBrain (2022): 뉴런 다발이 Pong 게임 학습
- 2026-03 Gobi Partners 투자
- **구글 직접 투자는 미확인** (앞 리서치 결과 그대로)
- 사이트: https://corticallabs.com/

### `Cortical-Labs/cl-api-doc`

| 항목 | 값 |
|---|---|
| 라이선스 | 없음 (모든 권리 보유 — 사용 전 별도 확인 필요) |
| 크기 | 800 KB |
| 최근 커밋 | 2025-08-30 |
| 내용 | Jupyter notebook 튜토리얼 7개 (CL-00 ~ CL-06) |

### 노트북 목록
- `CL-00. Hello, Neurons.ipynb` — 첫 자극
- `CL-01. Detecting and Reacting to Spikes.ipynb` — 스파이크 검출/반응
- `CL-01A. Detecting and Reacting to Spikes. Appendix A. UDP Spike Receiver.ipynb`
- `CL-02. Recording.ipynb` — 기록
- `CL-03. Data Streams.ipynb` — 데이터 스트림
- `CL-04. Real-Time Visualisation.ipynb` (+ `.html`, `.mjs`)
- `CL-05. Reading Raw Data.ipynb`
- `CL-06. Stimulation.ipynb`

### CL API 사용 예시 (CL-00에서)
```python
import cl

with cl.open() as neurons:
    neurons.stim(
        cl.ChannelSet(27),
        cl.StimDesign(180, -1.5, 180, 1.5))  # 180µs @ -1.5µA, then +1.5µA
```

### `Cortical-Labs/cl-sdk`

| 항목 | 값 |
|---|---|
| 라이선스 | **CC BY-NC 4.0** (NonCommercial — 상용 활용 시 별도 라이선스 필요) |
| 크기 | 6.9 MB |
| 최근 커밋 | 2026-02-21 |
| Python 요구사항 | 3.12+ |
| PyPI | `pip install cl-sdk` |

### SDK 모듈 구조 (`src/cl/`)
```
__init__.py
_base_producer.py        — 데이터 생산자 베이스
_closed_loop.py          — closed-loop 컨트롤러
_data_buffer.py
_data_producer.py
_recording_writer.py
_stim_plan.py            — 자극 계획
_stim_queue.py           — 자극 큐
analysis/                — 분석 도구
app/                     — 앱 진입점
data_stream.py           — 데이터 스트림 (WebSocket)
neurons.py               — 메인 API: cl.open(), neurons.stim()
playback/                — 녹화 재생
recording.py
util/
visualisation/           — 시각화
```

### 시뮬레이션 옵션
- `CL_SDK_REPLAY_PATH` — 녹화 재생 모드
- `CL_SDK_SAMPLE_MEAN`, `CL_SDK_SPIKE_PERCENTILE` — Poisson 합성 spike
- `CL_SDK_ACCELERATED_TIME=1` — 가속 시뮬레이션
- `CL_SDK_WEBSOCKET=1` — WebSocket 스트리밍 서버

### hexa-brain 관련성
**매우 높음 (v3-v4)**. hexa-brain의 `eeg/protocols/closed_loop.hexa`, `bci_control.hexa`와 **API 구조가 거의 1:1 대응**:

| hexa-brain | Cortical Labs CL1 |
|---|---|
| `ChannelSet` (16-ch OpenBCI) | `cl.ChannelSet(N)` |
| `eeg_recorder.hexa` (background daemon) | `_recording_writer.py` |
| `closed_loop.hexa` (WebSocket UI) | `_closed_loop.py` + WebSocket 서버 |
| `validate_consciousness.hexa` | `analysis/` 모듈군 |
| stim 프로토콜 (계획 단계) | `_stim_plan.py`, `_stim_queue.py` |

→ **hexa-brain은 CL1을 "biological substrate"로 추가할 수 있는 위치**. 단, **CC BY-NC 라이선스가 결정적 장애물**: 상용 또는 라이선스 호환성이 필요하면 Cortical Labs와 별도 협의 필요.

### 운영 모델
2026-04 발표: "Cortical Cloud" — 인간 뇌 세포를 클라우드에서 임대 (시간당 결제 추정)

---

## 8. OpenWorm — `openworm/c302` (C. elegans 신경계 모델)

| 항목 | 값 |
|---|---|
| 라이선스 | **MIT** (가장 자유로움) |
| 크기 | 144 MB |
| 최근 커밋 | 2026-03-31 |
| 언어 | Python + NeuroML 2 |
| 논문 | Phil. Trans. R. Soc. B 2018, 373:20170379 |

### 정체
**C. elegans 신경계 (302개 뉴런 + 95개 근육세포) 전체 시뮬레이션**. NeuroML 2 표준 사용. 시냅스 연결 데이터 (`c302/data/`) → libNeuroML → jNeuroML/pyNeuroML 실행.

### 의미
- "**현재까지 인류가 완전히 시뮬레이션한 유일한 신경계**" (LessWrong 비평글에서는 10년간 진척이 없다는 비판도 있음)
- hexa-brain v5 비전의 **현실 체크 베이스라인**: 302개 뉴런도 완전한 emulation이 어렵다면 인간 뇌(~860억) 의식 이동은 다른 차원의 도전.

### Pharmacological / 다중 스케일 옵션
파라미터 셋 A, B, C 등 — 각각 다른 추상화 수준의 네트워크 생성.

### hexa-brain 관련성
**낮음 (직접 통합 측면), 매우 높음 (정신 모델 측면)**. hexa-brain의 v5 로드맵 야망이 얼마나 비현실적인지 측정하는 베이스라인 ruler. MIT 라이선스라 NeuroML pipeline 일부 차용은 가능.

---

## 9. Neuralink (참고용 — 비공개 코드)

- GV (Google Ventures)가 과거 Series C $205M 라운드에 참여 — **"구글이 투자"가 사실인 회사**
- 머스크 비전: "10~20년 내 의식을 Optimus 로봇이나 디지털 저장소에 업로드"
- 실리콘 웨이퍼 위 MEMS 미세전극 어레이
- 2026-01부터 BCI 디바이스 **대량 생산** 시작
- **공개 저장소 없음** (회사 정책)
- 사이트: https://neuralink.com/

### hexa-brain 관련성
v3-v5 substrate ladder의 **레퍼런스 타겟**. README에 명시된 "Neuralink-class chronic implants"가 직접 대응.

---

## 10. 종합 정리 — hexa-brain interop 우선순위

### 단기 (v1-v2, 즉시 가능)
1. **Neuroglancer Precomputed format export** 추가 — `eeg/recordings/` 결과를 외부 협업자와 공유 가능. Apache 2.0 라이선스, MIT와 호환.
2. **CloudVolume 클라이언트 의존성 추가** — BSD-3, 호환 OK. 외부 페타복셀 데이터 읽기.

### 중기 (v3, 1-2년)
3. **BrainGenix-NES JSON POST API 통합 (loose coupling)** — hexa-brain의 closed-loop 알고리즘을 가상 뇌 조직에서 검증. AGPLv3 전파 회피를 위해 별도 프로세스 + REST API 호출.
4. **WBE Challenge 데이터셋 대응** — `validate_consciousness.hexa`의 6-metric을 표준 챌린지에 매핑.

### 장기 (v4-v5)
5. **Cortical Labs CL1 어댑터** — biological substrate 옵션. CC BY-NC가 **결정적 라이선스 장애물** — 학술용 또는 별도 라이선스 협의 필요.
6. **Connectome 직접 활용** — Google FlyEM/Janelia 데이터셋을 hexa-brain의 substrate-agnostic pipeline에서 simulation source로 활용.

### 의식 이동 (v6+, 아직 누구도 못 한 영역)
- 인간 뇌 connectome → emulation → biological substrate 이식
- 모든 4단계 (스캔 → 재구성 → 시뮬레이션 → 인터페이스)에 각각 oss 도구가 존재하지만, 인간 뇌 규모의 통합은 아직 누구도 못 했음
- C. elegans (302 뉴런) 도 10년간 완전히 못 했다는 비평 (LessWrong)을 현실 체크 베이스라인으로

---

## 11. 결론 — "헥사 브레인이라는 회사" 의 정체

확정: **그런 이름의 회사는 없음.** 가능성:

1. **Google Connectomics**가 "구글이 투자하는 회사"로 와전 (가장 유력)
2. **Cortical Labs**가 출처지만 "구글" 부분이 잘못 전달
3. **Neuralink**의 GV 투자 + 머스크의 의식 업로드 발언이 섞임
4. **Carboncopies + BrainGenix**가 "의식 이동" 키워드로 검색되어 와전
5. ⚠️ 마케팅 과장 / 가짜뉴스 / 투자 사기 — 누가 "Hexa Brain에 투자해라"라고 권유했다면 사기 의심

원래 들으신 출처(기사·유튜브·SNS)를 알려주시면 정확히 어느 후보인지 짚어낼 수 있음.

---

## 부록 A — 클론한 저장소 인벤토리

`/tmp/hexa-research/` (hexa-brain 본체와는 별도 워크스페이스):

| 디렉토리 | 크기 | 라이선스 | 최근 활동 |
|---|---|---|---|
| `ffn/` | 8.8 MB | Apache 2.0 | 2026-04-09 |
| `neuroglancer/` | 26 MB | Apache 2.0 | 2026-05-11 |
| `cloud-volume/` | 164 MB | BSD-3 | 2026-04-24 |
| `BrainGenix-NES/` | 5.9 MB | AGPLv3 | 2026-05-10 |
| `BrainEmulationChallenge/` | 11 MB | AGPLv3 | 2026-05-10 |
| `cl-api-doc/` | 800 KB | 없음 | 2025-08-30 |
| `cl-sdk/` | 6.9 MB | **CC BY-NC 4.0** | 2026-02-21 |
| `c302/` | 144 MB | MIT | 2026-03-31 |

**총 8개 저장소, 약 367 MB.** 8개 모두 2026년 활성 메인테인. AGPLv3 / CC-NC 라이선스는 hexa-brain (MIT) 본체 흡수 시 주의 필요.

---

## 부록 B — Sources

### Google Connectomics
- [Google Connectomics Team](https://research.google/teams/connectomics/)
- [Neural Mapping](https://sites.research.google/gr/neural-mapping/)
- [Drosophila Hemibrain blog](https://research.google/blog/releasing-the-drosophila-hemibrain-connectome-the-largest-synapse-resolution-map-of-brain-connectivity/)
- [Mouse brain mapping blog](https://research.google/blog/google-research-embarks-on-effort-to-map-a-mouse-brain/)

### Open-source repos
- [google/ffn](https://github.com/google/ffn) — Apache 2.0
- [google/neuroglancer](https://github.com/google/neuroglancer) — Apache 2.0
- [seung-lab/cloud-volume](https://github.com/seung-lab/cloud-volume) — BSD-3
- [carboncopies/BrainGenix-NES](https://github.com/carboncopies/BrainGenix-NES) — AGPLv3
- [carboncopies/BrainEmulationChallenge](https://github.com/carboncopies/BrainEmulationChallenge) — AGPLv3
- [Cortical-Labs/cl-api-doc](https://github.com/Cortical-Labs/cl-api-doc) — 라이선스 없음
- [Cortical-Labs/cl-sdk](https://github.com/Cortical-Labs/cl-sdk) — CC BY-NC 4.0
- [openworm/c302](https://github.com/openworm/c302) — MIT

### Companies / orgs
- [Carboncopies Foundation](https://carboncopies.org/)
- [Cortical Labs](https://corticallabs.com/) / [CL1](https://corticallabs.com/cl1) / [docs](https://docs.corticallabs.com/)
- [Neuralink](https://neuralink.com/)
- [OpenWorm](https://openworm.org/)

### Reference
- [Cortical Labs Gobi Partners investment (Mar 2026)](https://technode.global/2026/03/04/malaysia-based-gobi-partners-invests-in-cortical-labs-expands-biological-computing-hub/)
- [Neuralink 2026 high-volume production](https://www.fiercebiotech.com/medtech/elon-musks-neuralink-kickstart-high-volume-production-brain-computer-interface-devices)
- [Elon Musk on consciousness upload via Neuralink](https://punchng.com/elon-musk-conquering-death-with-ai-and-chips/)
- [LessWrong: WBE No Progress on C. elegans After 10 Years](https://www.lesswrong.com/posts/mHqQxwKuzZS69CXX5/whole-brain-emulation-no-progress-on-c-elegans-after-10)
- [Mind uploading — Wikipedia](https://en.wikipedia.org/wiki/Mind_uploading)
- [BrainChip $25M neuromorphic funding](https://ventureburn.com/brainchip-raises-25-million/)
- [Unconventional AI a16z $1B](https://www.inc.com/tekendra-parmar/andreessen-horowitz-a16z-startup-unconventional-ai-chips-1-billion/91276368)
- [Eternos digital immortality](https://techcrunch.com/2025/11/11/immortality-startup-eternos-pivots-to-a-personal-ai-that-sounds-like-you/)
- [Thinking Machines Lab — Google Cloud multi-billion deal](https://techcrunch.com/2026/04/22/exclusive-google-deepens-thinking-machines-lab-ties-with-new-multi-billion-dollar-deal/)
- [Neuronova brain-on-silicon](https://tech.eu/2025/01/20/bringing-the-brain-to-silicon-neuronovas-vision-for-energy-efficient-ai-hardware/)
