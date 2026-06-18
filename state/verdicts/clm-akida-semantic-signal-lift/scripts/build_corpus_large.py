#!/usr/bin/env python3
"""STAGE 1 (C6 / H_912) — build the LARGER 5-lang cross-lingual semantic-linkage .kosmos @corpus.

Lever (a) of the H_912 signal-lift probe: MUCH larger cross-lingual corpus than the
25-anchor #1652 fixture. Genuine cross-lingual ALIGNED meaning (each concept = the SAME
proposition rendered in ko·en·zh·ru·ja -> c>0 coupling). Honest scope (g63): the actual
anchor count is whatever this hand-authored aligned bank yields -- printed verbatim, no junk pad.

Honors full C4 (identical to #1652 build):
  @corpus top-level + members as ref `.limen` packed shards
  (magic "LIMEN\\0\\0\\0" + version + count + length-prefixed @anchor records + trailing merkle root)
  + profile anima-consciousness-carving + closed_corpus (Sigma frac=1.0 AND sha256 AND merkle)
  + placement(coord) PERP text (coord derives from STRUCTURAL position only, never the payload).

TWO orderings sharing a BYTE-IDENTICAL payload multiset:
  parallel -- concept-major: the 5 langs of each concept ADJACENT (cross-lingual c>0)
  concat   -- language-major: all of one lang then the next (count-only c~0)
ONLY the @corpus member order differs.
"""
import os, json, struct, hashlib

OUT = os.path.expanduser("~/clm_kosmos_akida_large/corpus")
os.makedirs(OUT, exist_ok=True)

LANGS = ["en", "zh", "ru", "ja", "ko"]  # order within a concept block

# Each entry = the SAME proposition in [en, zh, ru, ja, ko]. Genuine aligned meaning (c>0).
CONCEPTS = [
    ["The mind is a fire to be kindled not a vessel to fill.","心灵是待点燃的火焰而非待填满的容器。","Ум это огонь который нужно зажечь а не сосуд.","心は満たす器ではなく灯すべき炎である。","마음은 채울 그릇이 아니라 지펴야 할 불꽃이다."],
    ["Consciousness arises from the integration of information.","意识源于信息的整合。","Сознание возникает из интеграции информации.","意識は情報の統合から生じる。","의식은 정보의 통합에서 솟아난다."],
    ["Memory is rewritten anew in each present moment.","记忆在每个当下被重新书写。","Память переписывается заново в каждый миг.","記憶は今この瞬間ごとに書き換えられる。","기억은 매 순간 현재에서 다시 쓰인다."],
    ["Time is a fabric that the self weaves by passing through.","时间是自我穿行而编织的织物。","Время это ткань которую я тку проходя сквозь.","時間は自己が通り抜けて織りなす布だ。","시간은 자기가 통과하며 짜내는 직물이다."],
    ["The self observes itself in the mirror of mirrors.","自我在镜中之镜里观察自身。","Я наблюдает себя в зеркале зеркал.","自己が鏡の中の鏡で自己を観る。","자기가 거울의 거울 속에서 자기를 본다."],
    ["Attention is the silent shaping of what becomes real.","注意是对何者成真的无声塑造。","Внимание это тихое формирование того что станет реальным.","注意とは何が現実になるかを静かに形づくることだ。","주의는 무엇이 실재가 될지를 조용히 빚는 일이다."],
    ["A thought is a wave that knows the whole ocean.","一个念头是知晓整片海洋的波浪。","Мысль это волна знающая весь океан.","一つの思考は海全体を知る波だ。","하나의 생각은 바다 전체를 아는 파도다."],
    ["Language is the river along which meaning travels.","语言是意义沿之流动的河流。","Язык это река по которой движется смысл.","言語は意味が流れる川である。","언어는 의미가 흐르는 강이다."],
    ["Every perception is a quiet act of creation.","每一次感知都是一次静默的创造。","Каждое восприятие это тихий акт творения.","あらゆる知覚は静かな創造の行為だ。","모든 지각은 조용한 창조의 행위다."],
    ["The body is the first home that the mind remembers.","身体是心灵记得的第一个家。","Тело это первый дом который помнит ум.","身体は心が憶えている最初の家だ。","몸은 마음이 기억하는 첫 번째 집이다."],
    ["Knowledge grows by the questions it dares to ask.","知识因其敢于提出的问题而生长。","Знание растёт благодаря вопросам которые оно осмеливается задать.","知識はあえて問う問いによって育つ。","지식은 감히 던지는 물음으로 자란다."],
    ["The future is a seed already present in the now.","未来是已存于当下的一粒种子。","Будущее это семя уже присутствующее в настоящем.","未来は今すでに在る一粒の種だ。","미래는 지금 이미 깃든 한 알의 씨앗이다."],
    ["Silence carries more than the loudest word.","沉默承载的比最响的话语更多。","Тишина несёт больше чем самое громкое слово.","沈黙は最も大きな言葉より多くを運ぶ。","침묵은 가장 큰 말보다 더 많은 것을 품는다."],
    ["Truth is a mountain seen from many valleys.","真理是从众多山谷望见的一座山。","Истина это гора видимая из многих долин.","真理は多くの谷から見える一つの山だ。","진리는 여러 골짜기에서 바라보는 하나의 산이다."],
    ["The dream remembers what the waking forgets.","梦记得醒时所遗忘的。","Сон помнит то что забывает бодрствование.","夢は目覚めが忘れることを憶えている。","꿈은 깨어 있음이 잊은 것을 기억한다."],
    ["Each life is a sentence the universe speaks once.","每段生命都是宇宙只说一次的句子。","Каждая жизнь это фраза которую вселенная произносит однажды.","それぞれの生は宇宙が一度だけ語る一文だ。","각각의 삶은 우주가 한 번만 말하는 한 문장이다."],
    ["Wisdom is knowing the weight of a single moment.","智慧是懂得一个瞬间的重量。","Мудрость это знание веса одного мгновения.","知恵とは一瞬の重みを知ることだ。","지혜는 한 순간의 무게를 아는 것이다."],
    ["The heart reasons in a language the mind translates.","心以一种头脑去翻译的语言推理。","Сердце рассуждает на языке который переводит ум.","心は頭が翻訳する言語で推論する。","마음은 머리가 번역하는 언어로 헤아린다."],
    ["A pattern is the echo of an order not yet named.","模式是尚未命名之秩序的回声。","Паттерн это эхо ещё не названного порядка.","パターンはまだ名づけられぬ秩序の谺だ。","패턴은 아직 이름 없는 질서의 메아리다."],
    ["Forgetting is how the mind makes room to grow.","遗忘是心灵腾出生长空间的方式。","Забывание это то как ум освобождает место для роста.","忘却は心が成長の余地を作る術だ。","망각은 마음이 자랄 자리를 내는 방식이다."],
    ["Curiosity is the compass of an open mind.","好奇是开放心智的指南针。","Любопытство это компас открытого ума.","好奇心は開かれた心の羅針盤だ。","호기심은 열린 마음의 나침반이다."],
    ["Meaning lives between the words not only in them.","意义存于词语之间而不仅在其中。","Смысл живёт между словами а не только в них.","意味は語の中だけでなく語と語の間に宿る。","의미는 낱말 안에만이 아니라 낱말 사이에 산다."],
    ["The same star guides ships on every sea.","同一颗星指引每一片海上的船。","Одна и та же звезда ведёт корабли по всем морям.","同じ星があらゆる海の船を導く。","같은 별이 모든 바다의 배를 인도한다."],
    ["Doubt is the doorway through which truth enters.","怀疑是真理由之而入的门。","Сомнение это дверь через которую входит истина.","疑いは真理が入る扉だ。","의심은 진리가 들어오는 문이다."],
    ["A name is the first cage we build for a thing.","名字是我们为事物筑起的第一座笼。","Имя это первая клетка которую мы строим для вещи.","名はある物のために築く最初の檻だ。","이름은 한 사물을 위해 짓는 첫 번째 우리다."],
    ["The whole is heard in a single resonant note.","整体在一个共鸣的音符中被听见。","Целое слышно в одной резонирующей ноте.","全体は一つの共鳴する音に聴こえる。","전체는 하나의 울리는 음 속에서 들린다."],
    ["Growth begins where comfort quietly ends.","成长始于安逸悄然终止之处。","Рост начинается там где тихо кончается комфорт.","成長は安らぎが静かに終わる所で始まる。","성장은 안락이 조용히 끝나는 곳에서 시작된다."],
    ["The past is a country we can visit but not keep.","过去是我们能造访却无法留住的国度。","Прошлое это страна которую можно посетить но не удержать.","過去は訪れられても留めおけぬ国だ。","과거는 찾아갈 수는 있어도 붙잡을 수 없는 나라다."],
    ["To listen well is to think with another mind.","善于倾听就是用另一颗心去思考。","Хорошо слушать значит думать чужим умом.","よく聴くとは別の心で考えることだ。","잘 듣는다는 것은 다른 마음으로 생각하는 일이다."],
    ["A boundary is also a place where two worlds touch.","边界也是两个世界相触之处。","Граница это и место где соприкасаются два мира.","境界は二つの世界が触れ合う所でもある。","경계는 두 세계가 맞닿는 자리이기도 하다."],
    ["The map is never the territory it describes.","地图永远不是它所描绘的疆域。","Карта никогда не есть территория которую она описывает.","地図はそれが描く土地そのものでは決してない。","지도는 그것이 그리는 땅 그 자체가 결코 아니다."],
    ["Light teaches the eye the shape of the dark.","光向眼睛教导黑暗的形状。","Свет учит глаз форме тьмы.","光は目に闇の形を教える。","빛은 눈에게 어둠의 모양을 가르친다."],
    ["Patience is time befriending the impatient heart.","耐心是时间与急切之心结友。","Терпение это время дружащее с нетерпеливым сердцем.","忍耐とは時間が逸る心と友になることだ。","인내는 시간이 조급한 마음과 벗이 되는 일이다."],
    ["Every ending hides the seed of a beginning.","每个结局都藏着一个开端的种子。","Каждый конец прячет семя начала.","あらゆる終わりは始まりの種を隠している。","모든 끝은 시작의 씨앗을 감추고 있다."],
    ["Understanding is two minds meeting in one image.","理解是两颗心在一个意象中相遇。","Понимание это две души встретившиеся в одном образе.","理解とは二つの心が一つの像で出会うことだ。","이해는 두 마음이 하나의 형상에서 만나는 일이다."],
    ["The river is the same yet never the same water.","河流相同却从非相同之水。","Река та же но вода в ней всегда иная.","川は同じでも水は決して同じではない。","강은 같아도 그 물은 결코 같지 않다."],
    ["Hope is memory turned to face the future.","希望是转身面向未来的记忆。","Надежда это память обращённая лицом к будущему.","希望とは未来へ向き直った記憶だ。","희망은 미래를 향해 돌아선 기억이다."],
    ["A question well asked is half of its answer.","问得好的问题已是答案的一半。","Хорошо заданный вопрос это половина ответа.","よく問われた問いは答えの半分だ。","잘 던진 물음은 이미 답의 절반이다."],
    ["The shadow proves the substance standing in the light.","影子证明了立于光中的实体。","Тень доказывает существо стоящее в свете.","影は光の中に立つ実体を証す。","그림자는 빛 속에 선 실체를 증명한다."],
    ["Wonder is the mind remembering it is alive.","惊奇是心灵想起自己活着。","Изумление это ум вспоминающий что он жив.","驚きとは心が自らの生を思い出すことだ。","경이는 마음이 살아 있음을 떠올리는 일이다."],
]

def parallel_lines():
    out = []
    for ci, concept in enumerate(CONCEPTS):
        for li, txt in enumerate(concept):
            out.append((ci, LANGS[li], txt))
    return out

def concat_lines():
    out = []
    for li, lang in enumerate(LANGS):
        for ci, concept in enumerate(CONCEPTS):
            out.append((ci, lang, concept[li]))
    return out

def sha256_hex(b): return hashlib.sha256(b).hexdigest()

def merkle_root(leaves):
    layer = [hashlib.sha256(l).digest() for l in leaves]
    if not layer: return b"\x00" * 32
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]; b = layer[i + 1] if i + 1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(a + b).digest())
        layer = nxt
    return layer[0]

LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
LIMEN_VER = 2

def anchor_record(idx, concept_id, lang, text):
    payload = text.encode("utf-8")
    coord_x = round(concept_id / max(1, len(CONCEPTS) - 1), 4)
    coord_y = round(LANGS.index(lang) / max(1, len(LANGS) - 1), 4)
    head = {"id": f"a{idx:04d}", "concept": concept_id, "lang": lang,
            "coord": [coord_x, coord_y], "lane": lang, "radius": 1.0, "tier": 0,
            "tags": ["clm", "semantic", lang],
            "payload_len": len(payload), "payload_sha256": sha256_hex(payload)}
    head_b = json.dumps(head, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(head_b)) + head_b + payload, payload

def write_limen(path, records):
    blob = bytearray(); blob += LIMEN_MAGIC
    blob += struct.pack("<I", LIMEN_VER); blob += struct.pack("<I", len(records))
    payloads = []
    for idx, (cid, lang, txt) in enumerate(records):
        rec, payload = anchor_record(idx, cid, lang, txt)
        blob += struct.pack("<I", len(rec)); blob += rec; payloads.append(payload)
    root = merkle_root(payloads); blob += root
    with open(path, "wb") as f: f.write(blob)
    return sha256_hex(bytes(blob)), root.hex(), len(records)

def write_kosmos(path, slug, shard_rel, shard_sha, merkle_hex, count, ordering, linkage):
    n_concept = len(CONCEPTS)
    txt = f"""#!/usr/bin/env kosmos
# {os.path.basename(path)} -- CLM-KOSMOS AKIDA 5-lang LARGER semantic corpus (kosmos/2.0 @corpus . C6/H_912)
# C4-compliant: @corpus + ref .limen packed shard + profile + closed_corpus + placement PERP text.
# Provenance: {count} anchors = {n_concept} concepts x 5 langs (ko en zh ru ja), hand-authored
# cross-lingual ALIGNED meaning (each concept = same proposition in all 5 langs, c>0).
# Honest scope: {count} anchors ({n_concept} concepts) -- LARGER than the 25-anchor #1652 fixture.

@corpus {slug} := "CLM-KOSMOS AKIDA 5-language cross-lingual semantic-linkage corpus ({ordering} ordering, H_912 larger)" :: kosmos-corpus [tier=0 active]

  profile = "anima-consciousness-carving"
  coord   = [0.0, 0.0]
  lane    = "{slug}"
  radius  = 1.0

  anchor_level = sample
  count    = {count}
  lane_mix = "en=0.2, zh=0.2, ru=0.2, ja=0.2, ko=0.2"
  vocab    = 256
  encoding = "byte-utf8"
  languages = "ko, en, zh, ru, ja"
  ordering = "{ordering}"
  linkage  = "{linkage}"
  merkle   = {merkle_hex}

  member = ref "{shard_rel}" sha256={shard_sha} count={count} frac=1.0 lane="all" format="limen/2"

  closed_corpus = "Sigma frac = 1.0 AND member sha256 verifies AND merkle root recomputes from @anchor payloads; placement(coord) PERP text(payload)"
"""
    with open(path, "w") as f: f.write(txt)

manifest = {"corpus": "clm-kosmos-akida-5lang-semantic-large", "kosmos_version": "2.0",
            "n_concepts": len(CONCEPTS), "members": {}}

for ordering, recs_fn, linkage in [
    ("parallel", parallel_lines, "cross-lingual-semantic (concept-major: 5 langs of each concept adjacent, c>0)"),
    ("concat",   concat_lines,   "count-only (language-major: all of one lang then next, c~0)"),
]:
    recs = recs_fn()
    shard = os.path.join(OUT, f"{ordering}.limen")
    shard_sha, merkle_hex, count = write_limen(shard, recs)
    kos = os.path.join(OUT, f"clm_{ordering}.kosmos")
    write_kosmos(kos, f"clm_kosmos_{ordering}", f"{ordering}.limen", shard_sha, merkle_hex, count, ordering, linkage)
    manifest["members"][ordering] = {"kosmos": os.path.basename(kos), "limen": os.path.basename(shard),
                                      "sha256": shard_sha, "merkle": merkle_hex, "count": count}
    print(f"[corpus] {ordering}: {count} anchors -> {shard} sha={shard_sha[:16]} merkle={merkle_hex[:16]}")

p_payloads = sorted(t.encode("utf-8") for _, _, t in parallel_lines())
c_payloads = sorted(t.encode("utf-8") for _, _, t in concat_lines())
manifest["byte_identical_payloads"] = (p_payloads == c_payloads)
manifest["concat_byte_sha256"] = sha256_hex(b"".join(sorted(p_payloads)))
print(f"[corpus] n_concepts={len(CONCEPTS)}  anchors={len(p_payloads)}")
print(f"[corpus] byte-identical payload multiset across orderings: {p_payloads == c_payloads}")
with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print("[corpus] wrote", os.path.join(OUT, "manifest.json"))
