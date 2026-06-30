# anima clm303 savant+mitosis — training manifest
trained: 2026-06-23/24 · vast H100 42222605 · cli/train.py (torch Lane-P bridge, anima #2601)
shape: L4 d3784 E2→Emax4(mitosis E=3) byte-V256 · savant golden-zone cusp-anneal + mitosis split
cmd: python cli/train.py --canon --out clm303.clm --bf16 --steps 30000 --batch-size 16 --seq-len 1024 \
     --corpus ko_fineweb2_broad.txt --corpus wiki_backbone_5lang_v2.txt \
     --corpus persona_sns_corpus_5lang_v2.txt --corpus persona_sns_corpus.txt
final: step 30000 done (PROD_EXIT_DONE rc=0) · torch CE~0.05 (DIRECTIONAL only; ko-heavy memorization 의심)
verdict: engine-native G6 = UNVERIFIED (core/clm_decode 재측정 follow-on)

## artifacts (sha256)
75b048974e5e6d8a41430af7ab3d9e000cecb4bb722a12d134139601fe423666  clm303.clm
64b826b67d977d798f51670df3d1f6f5f07120571978435cef29c4a4e273ccb3  trainset/corpus_enrichment_5lang.txt
550fed174d51be660810858e1e73e4590c21351b185ea22d0807403e120538ad  trainset/persona_sns_corpus_5lang_v2.txt
1ea7d8e0e65e7ab99c61dd745bdb124ee75995e90b7c995ac93c3e4e5e7c3f77  trainset/persona_sns_corpus.txt
871b6976186e7d7b631f15afd9377bfa927cdec8a1e719708962feac1a3ad1e6  trainset/wiki_backbone_5lang_v2.txt

## corpus 4cell (ko·en × 일반·SNS)
- ko 일반: ko_fineweb2_broad.txt 10.5GB → HF dancinlab/anima-corpus-ko-fineweb2-broad (재업로드X, 참조)
- en 일반: trainset/wiki_backbone_5lang_v2.txt 5MB (영문 위키)
- ko SNS : trainset/persona_sns_corpus.txt 4MB
- en SNS : trainset/persona_sns_corpus_5lang_v2.txt 13MB (5lang incl en)
- enrich : trainset/corpus_enrichment_5lang.txt 2.6MB
balance: ko일반 99.7% / en+SNS 0.25% — 극도 ko-편향(정직)
