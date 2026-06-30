#!/usr/bin/env python3
"""Lane A REAL-SCALE corpus (rung4) — 250 (→ optionally 500) genuine cross-lingual ALIGNED concepts, NOT synthetic.

EXTENDS AKIDA/build_corpus_real100.py. substrate-agnostic builder (the chip pipeline is byte-identical to
corpus_big / corpus_real100). a_scale_honest_scope. g63 honest, NO synthetic byte-pad.

3-TIER PROVENANCE (labelled EXPLICITLY in .verdicts/lane-a-corpus-real/CORPUS_CARD.md):
  Tier-1 (concepts   0.. 49) = the EXACT 50 FLORES cross-lingual parallel sentences deployed in corpus_big
                               (byte-preserved from corpus_real100[0:50]) — REAL GOLD news/factual translations
                               (en zh ru ja ko). NOT model-authored.
  Tier-2 (concepts  50.. 99) = the 50 hand-authored cross-lingual ALIGNED propositions already in
                               build_corpus_real100 (concepts 50..99: 40 authored aphorisms + 10 new authored).
                               human/model hand-authored aligned MEANINGS, deployed + verified at rung3 NC=100.
  Tier-3 (concepts 100..249) = NEW model-authored aligned propositions for THIS rung (rung4): genuine
                               cross-lingual aligned MEANINGS — a single fact/aphorism rendered FAITHFULLY in all
                               5 languages (en zh ru ja ko), translation-faithful, deduped, byte-length balanced.
                               LABELLED EXPLICITLY: "model-authored aligned (real-semantic, NOT FLORES-gold,
                               NOT synthetic)". This is the honest middle tier — real semantic content authored by
                               the model, distinct from Tier-1 gold and from any synthetic byte-pattern.
  => corpus_real250: 250 DISTINCT real aligned concepts x 5 langs = 1250 real anchors. PUSHES real NC past the
     prior NC=100 ceiling WITHOUT synthetic padding. (corpus_real500 is built ONLY if Tier-3 authoring quality
     holds for a further 250 concepts — see TIER3_EXT500 below; if not authored, real500 is skipped and the honest
     ceiling stays NC=250, a valid honest outcome per the rung4 milestone.)

LIMEN format byte-identical to build_corpus_real100.py; concept/lang headers match corpus_big so every harness
(which subsets by concept) consumes it UNCHANGED.
"""
import os, json, struct, hashlib, sys

# import the 100 verified concepts (Tier-1 FLORES 0..49 + Tier-2 authored 50..99) byte-for-byte
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_corpus_real100 import CONCEPTS as BASE100, LANGS

assert len(BASE100) == 100 and all(len(c) == 5 for c in BASE100)

# ---------------------------------------------------------------------------
# TIER-3 (concepts 100..249): 150 NEW model-authored aligned propositions.
# Each row = the SAME proposition rendered faithfully in [en, zh, ru, ja, ko].
# Real-semantic (a genuine aphorism/fact), translation-faithful, byte-length balanced. NOT FLORES-gold, NOT synthetic.
# ---------------------------------------------------------------------------
TIER3 = [
["A flame divides without diminishing itself.","火焰分予他者却不减损自身。","Пламя делится не убывая.","炎は分け与えても自らを減らさない。","불꽃은 나누어도 스스로 줄지 않는다."],
["The root works in darkness so the leaf may shine.","根在黑暗中劳作，好让叶得以发光。","Корень трудится во тьме чтобы лист сиял.","根は闇で働き葉を輝かせる。","뿌리는 어둠에서 일해 잎을 빛나게 한다."],
["A question outlives the answer that silences it.","问题比令其沉默的答案活得更久。","Вопрос переживает ответ что его заглушил.","問いはそれを黙らせた答えより長く生きる。","물음은 그것을 잠재운 답보다 오래 산다."],
["The clock measures time but never holds it.","钟测量时间却从不留住它。","Часы измеряют время но не удерживают его.","時計は時を測るが留めはしない。","시계는 시간을 재지만 붙잡지는 못한다."],
["A wall is also the shape of the room within.","墙也是其内房间的形状。","Стена это и форма комнаты внутри.","壁は内の部屋の形でもある。","벽은 그 안 방의 모양이기도 하다."],
["Frost writes its name on the morning glass.","霜在清晨的玻璃上写下其名。","Иней пишет своё имя на утреннем стекле.","霜は朝の硝子に名を記す。","서리는 아침 유리에 제 이름을 쓴다."],
["The first step already contains the whole road.","第一步已蕴含整条道路。","Первый шаг уже содержит всю дорогу.","最初の一歩は道全体を孕む。","첫걸음은 이미 길 전체를 품는다."],
["A debt of gratitude grows lighter when paid forward.","感恩之债在传递时变得更轻。","Долг благодарности легчает когда передан дальше.","感謝の負債は次へ送れば軽くなる。","감사의 빚은 다음으로 전할 때 가벼워진다."],
["Rain remembers the sea it will return to.","雨记得它将回归的海。","Дождь помнит море куда вернётся.","雨は還る海を憶えている。","비는 돌아갈 바다를 기억한다."],
["The scar is proof the wound chose to heal.","疤是伤口选择愈合的证据。","Шрам это знак что рана решила зажить.","傷跡は傷が癒えを選んだ証だ。","흉터는 상처가 낫기를 택한 증거다."],
["A key is useless until it meets its lock.","钥匙在遇到其锁前毫无用处。","Ключ бесполезен пока не встретит свой замок.","鍵は錠に出会うまで役立たない。","열쇠는 제 자물쇠를 만나기 전엔 쓸모없다."],
["The harvest repays the patience of the seed.","收成回报种子的耐心。","Урожай вознаграждает терпение семени.","収穫は種の忍耐に報いる。","수확은 씨앗의 인내에 보답한다."],
["A whisper can steer where a shout cannot.","低语能引导喊叫所不能之处。","Шёпот ведёт там где не может крик.","囁きは叫びの届かぬ所を導く。","속삭임은 외침이 못 닿는 곳을 이끈다."],
["The bridge fears no river it was built to cross.","桥不惧它为之而建以跨越的河。","Мост не боится реки которую призван перейти.","橋は渡るために架けられた川を恐れぬ。","다리는 건너려 놓인 강을 두려워 않는다."],
["A candle spends itself to lend its light.","蜡烛耗尽自身以借出其光。","Свеча тратит себя чтобы одолжить свет.","蝋燭は身を費やし光を貸す。","촛불은 제 몸을 써 빛을 빌려준다."],
["The mountain teaches by simply remaining.","山仅以常在而施教。","Гора учит просто оставаясь.","山はただ在ることで教える。","산은 그저 남아 있음으로 가르친다."],
["A word once freed belongs to every listener.","话语一经释放便属于每位听者。","Слово однажды отпущенное принадлежит каждому слушателю.","放たれた言葉は聴く者みなのものだ。","한번 풀린 말은 듣는 모두의 것이다."],
["Hunger sharpens the senses the feast dulls.","饥饿磨利盛宴所钝化的感官。","Голод обостряет чувства что притупляет пир.","飢えは饗宴が鈍らせる感覚を研ぐ。","굶주림은 잔치가 무디게 한 감각을 벼린다."],
["The shadow lengthens as the light grows low.","影随光低而拉长。","Тень удлиняется когда свет клонится.","影は光が傾くほど伸びる。","그림자는 빛이 기울수록 길어진다."],
["A vow is a road paved before it is walked.","誓言是行走之前就铺好的路。","Клятва это дорога мощённая до того как пройдена.","誓いは歩む前に敷かれた道だ。","맹세는 걷기 전에 깔린 길이다."],
["The river carves the canyon grain by grain.","河一粒一粒地刻出峡谷。","Река точит каньон по песчинке.","川は一粒ずつ峡谷を刻む。","강은 한 알씩 협곡을 깎는다."],
["A mirror keeps no memory of the faces it held.","镜不留它曾映之面容的记忆。","Зеркало не хранит память лиц что держало.","鏡は映した顔の記憶を留めぬ。","거울은 비춘 얼굴의 기억을 남기지 않는다."],
["Courage is fear that has said its prayers.","勇气是已作过祷告的恐惧。","Мужество это страх прочитавший молитвы.","勇気は祈りを終えた恐れだ。","용기는 기도를 마친 두려움이다."],
["The nest is woven from a thousand small returns.","巢由千次微小的归来编织而成。","Гнездо сплетено из тысячи малых возвращений.","巣は千の小さな帰還で編まれる。","둥지는 천 번의 작은 귀환으로 엮인다."],
["A door knows both the leaving and the welcome.","门同知离去与迎接。","Дверь знает и уход и встречу.","扉は去りと迎えを共に知る。","문은 떠남과 맞이함을 함께 안다."],
["Sand recalls the wave that smoothed it flat.","沙记得将其抚平的浪。","Песок помнит волну что его разгладила.","砂は均した波を憶えている。","모래는 자신을 고른 파도를 기억한다."],
["A promise kept builds the next one's bridge.","守住的承诺架起下一个的桥。","Сдержанное обещание строит мост для следующего.","守られた約束は次の橋を架ける。","지킨 약속은 다음 약속의 다리를 놓는다."],
["The forest breathes as one through many leaves.","森林透过众多叶子如一体般呼吸。","Лес дышит как один через множество листьев.","森は多くの葉を通し一つとして呼吸する。","숲은 많은 잎으로 하나처럼 숨 쉰다."],
["A coin shows two faces of one truth.","硬币展示同一真理的两面。","Монета являет два лица одной истины.","硬貨は一つの真理の二面を示す。","동전은 한 진리의 두 얼굴을 보인다."],
["Winter prunes the branch the spring will need.","冬修剪春日所需之枝。","Зима обрезает ветвь что нужна весне.","冬は春に要る枝を剪る。","겨울은 봄이 필요할 가지를 친다."],
["The anchor lets the ship rest without sinking.","锚让船歇息而不沉没。","Якорь даёт кораблю покой без потопа.","錨は船を沈めず憩わせる。","닻은 배를 가라앉히지 않고 쉬게 한다."],
["A name spoken in love outlasts the marble.","以爱说出的名比大理石长存。","Имя сказанное с любовью переживёт мрамор.","愛で呼ばれた名は大理石より残る。","사랑으로 부른 이름은 대리석보다 오래 간다."],
["The thread learns the shape of every knot.","线习得每个结的形状。","Нить узнаёт форму каждого узла.","糸は結び目ごとの形を覚える。","실은 매듭마다의 모양을 익힌다."],
["Dawn forgives the night without erasing it.","黎明宽恕黑夜却不抹去它。","Рассвет прощает ночь не стирая её.","暁は夜を消さず赦す。","새벽은 밤을 지우지 않고 용서한다."],
["A burden shared changes weight into bond.","分担的重负将重量化为纽带。","Разделённая ноша меняет вес на связь.","分け合う荷は重みを絆に変える。","나눈 짐은 무게를 인연으로 바꾼다."],
["The bell gives its sound and keeps its shape.","钟给出声音却保持其形。","Колокол отдаёт звук храня форму.","鐘は音を放ち形を保つ。","종은 소리를 내주고 모양을 지킨다."],
["A path appears only to the one who walks.","路只对行走者显现。","Путь является лишь идущему.","道は歩む者にのみ現れる。","길은 걷는 자에게만 나타난다."],
["The lamp does not argue with the dark.","灯不与黑暗争辩。","Лампа не спорит с тьмой.","灯は闇と論じない。","등불은 어둠과 다투지 않는다."],
["A pearl is grief the oyster learned to wear.","珍珠是牡蛎学会佩戴的悲伤。","Жемчуг это горе что устрица научилась носить.","真珠は牡蛎が纏うを学んだ悲しみだ。","진주는 굴이 두르기를 배운 슬픔이다."],
["The compass needle trusts a star it cannot see.","罗盘针信任它看不见的星。","Стрелка компаса верит звезде что не видит.","羅針盤の針は見えぬ星を信じる。","나침반 바늘은 보이지 않는 별을 믿는다."],
["A field rests one season to feed the next.","田休耕一季以养下一季。","Поле отдыхает сезон чтобы кормить следующий.","畑は一季休み次を養う。","밭은 한 철 쉬어 다음 철을 먹인다."],
["The echo is the cliff learning to speak.","回声是悬崖学习说话。","Эхо это утёс учащийся говорить.","谺は崖が話すを学ぶことだ。","메아리는 절벽이 말하기를 배우는 일이다."],
["A gift withheld becomes a quiet kind of theft.","扣下的礼物成为一种无声的偷窃。","Удержанный дар становится тихой кражей.","惜しまれた贈り物は静かな盗みになる。","아껴 둔 선물은 조용한 도둑질이 된다."],
["The kiln gives the clay a memory of fire.","窑给予黏土火的记忆。","Печь дарит глине память огня.","窯は粘土に火の記憶を授ける。","가마는 흙에 불의 기억을 준다."],
["A truth half-told leans toward a lie.","半说的真理向谎言倾斜。","Полуправда клонится ко лжи.","半ば語られた真理は嘘へ傾く。","반만 말한 진실은 거짓으로 기운다."],
["The tide keeps no grudge against the shore.","潮不对岸怀恨。","Прилив не таит обиды на берег.","潮は岸に恨みを抱かぬ。","조수는 기슭에 원한을 품지 않는다."],
["A song outgrows the throat that gave it birth.","歌长大超越生它的喉咙。","Песня перерастает горло что её родило.","歌はそれを生んだ喉を超え育つ。","노래는 그를 낳은 목을 넘어 자란다."],
["The plow honors the field by breaking it.","犁以破开田地来尊崇它。","Плуг чтит поле разрывая его.","鍬は畑を裂くことで敬う。","쟁기는 밭을 가름으로 그것을 기린다."],
["A friend is a mirror that also remembers.","朋友是亦能记忆的镜。","Друг это зеркало что ещё и помнит.","友は憶えもする鏡だ。","벗은 기억까지 하는 거울이다."],
["The arrow forgets the bow once it flies.","箭一旦飞出便忘了弓。","Стрела забывает лук едва взлетит.","矢は飛べば弓を忘れる。","화살은 날면 활을 잊는다."],
["A house keeps the warmth its people leave.","屋子留住其人离去时的温暖。","Дом хранит тепло что оставляют люди.","家は人が残す温もりを保つ。","집은 사람이 남긴 온기를 간직한다."],
["The moon borrows light and gives back calm.","月借来光，还回宁静。","Луна берёт свет и возвращает покой.","月は光を借り静けさを返す。","달은 빛을 빌려 고요를 돌려준다."],
["A law unjust is a wall built on sand.","不公的法是建于沙上的墙。","Несправедливый закон это стена на песке.","不正な法は砂上の壁だ。","불의한 법은 모래 위에 쌓은 벽이다."],
["The chrysalis trusts a wing it has not grown.","蛹信任它尚未长出的翅膀。","Куколка верит крылу что ещё не отрастила.","蛹はまだ生えぬ翅を信じる。","번데기는 아직 돋지 않은 날개를 믿는다."],
["A market knows the price but not the worth.","市场知道价格却不知价值。","Рынок знает цену но не ценность.","市場は値段を知るが価値は知らぬ。","시장은 값은 알아도 가치는 모른다."],
["The well gives more the deeper it is dug.","井挖得越深给得越多。","Колодец даёт больше чем глубже копан.","井戸は深く掘るほど多く与える。","우물은 깊이 팔수록 더 준다."],
["A grudge is a coal that burns the holder.","怨恨是烧灼持有者的炭。","Обида это уголь жгущий держащего.","恨みは持つ者を焼く炭だ。","원한은 쥔 자를 태우는 숯이다."],
["The vineyard rewards the years of waiting.","葡萄园回报等待的岁月。","Виноградник вознаграждает годы ожидания.","葡萄畑は待つ年月に報いる。","포도밭은 기다린 세월에 보답한다."],
["A child's question can topple an old certainty.","孩子的问题能推翻陈旧的确信。","Вопрос ребёнка валит старую уверенность.","子の問いは古い確信を覆す。","아이의 물음은 낡은 확신을 무너뜨린다."],
["The loom turns scattered threads into one cloth.","织机将散乱的线化为一块布。","Ткацкий станок сводит нити в единое полотно.","機は散る糸を一枚の布にする。","베틀은 흩어진 실을 한 천으로 만든다."],
["A summit reveals the valleys it rose above.","峰顶显露它所超越的谷。","Вершина открывает долины над которыми встала.","頂は越えた谷を露わにする。","정상은 자신이 넘어선 골짜기를 드러낸다."],
["The seed of doubt waters the tree of thought.","怀疑的种子浇灌思想之树。","Семя сомнения поит древо мысли.","疑いの種は思考の樹を潤す。","의심의 씨앗은 사유의 나무를 적신다."],
["A storm clears the air it first disturbs.","风暴先扰乱后澄清空气。","Буря очищает воздух что прежде смутила.","嵐はまず乱した空気を澄ます。","폭풍은 먼저 흐린 공기를 맑게 한다."],
["The blacksmith bends iron by giving it fire.","铁匠以火赋之而弯铁。","Кузнец гнёт железо даруя ему огонь.","鍛冶は火を与え鉄を曲げる。","대장장이는 불을 주어 쇠를 굽힌다."],
["A boundary names two freedoms at once.","边界一次命名两种自由。","Граница называет сразу две свободы.","境界は二つの自由を一度に名づける。","경계는 두 자유를 한꺼번에 이름 짓는다."],
["The orchard outlives the hand that planted it.","果园比种它的手活得长。","Сад переживает руку что его посадила.","果樹園は植えた手より長く生きる。","과수원은 심은 손보다 오래 산다."],
["A silence between friends needs no filling.","朋友间的沉默无需填补。","Молчание меж друзей не нужно заполнять.","友の間の沈黙は埋めずともよい。","벗 사이의 침묵은 채울 필요가 없다."],
["The glacier moves though the eye sees stone.","冰川移动，纵使眼见为石。","Ледник движется хоть глаз видит камень.","氷河は石に見えても動く。","빙하는 눈엔 돌 같아도 움직인다."],
["A spark respects no size when wind arrives.","风至时火星不顾大小。","Искра не чтит размер когда приходит ветер.","風来れば火花は大小を問わぬ。","바람이 오면 불꽃은 크기를 가리지 않는다."],
["The hand that gives is the first to receive.","施予的手最先得到。","Рука дающая первой и получает.","与える手が最初に受け取る。","주는 손이 가장 먼저 받는다."],
["A page turned still belongs to the book.","翻过的一页仍属于书。","Перевёрнутая страница всё ещё книги.","めくられた頁もなお書のものだ。","넘긴 페이지도 여전히 책의 것이다."],
["The owl reads the night the day cannot.","猫头鹰读得懂白昼读不懂的夜。","Сова читает ночь что не дано дню.","梟は昼に読めぬ夜を読む。","올빼미는 낮이 못 읽는 밤을 읽는다."],
["A craft is patience taught to the hands.","技艺是教给双手的耐心。","Ремесло это терпение преподанное рукам.","技は手に教えた忍耐だ。","기예는 손에 가르친 인내다."],
["The cliff and the wave are old companions.","悬崖与浪是旧伴。","Утёс и волна давние спутники.","崖と波は古い連れだ。","절벽과 파도는 오랜 동무다."],
["A flag remembers the wind that lifted it.","旗记得举起它的风。","Флаг помнит ветер что его поднял.","旗は掲げた風を憶えている。","깃발은 자신을 띄운 바람을 기억한다."],
["The stitch holds because it yields a little.","针脚因略微让步而牢固。","Стежок держит ибо слегка уступает.","縫い目は少し譲るゆえ持つ。","바늘땀은 조금 양보하기에 버틴다."],
["A vow of silence can shout the loudest.","沉默之誓能喊得最响。","Обет молчания кричит громче всех.","沈黙の誓いが最も大きく叫ぶ。","침묵의 맹세가 가장 크게 외친다."],
["The acorn argues nothing with the oak.","橡果与橡树无所争辩。","Жёлудь ни о чём не спорит с дубом.","団栗は樫と何も論じない。","도토리는 참나무와 다툴 것이 없다."],
["A grief unspoken still rearranges the heart.","未言之悲仍重排心房。","Невысказанное горе всё же перестраивает сердце.","語られぬ悲しみも心を組み替える。","말 못한 슬픔도 마음을 다시 배열한다."],
["The kite is freest while the string holds.","风筝在线牵着时最自由。","Воздушный змей свободнее всего на нитке.","凧は糸が保つ間こそ最も自由だ。","연은 줄이 잡고 있을 때 가장 자유롭다."],
["A map drawn in fear marks the wrong dangers.","在恐惧中画的地图标错危险。","Карта из страха метит ложные опасности.","恐れで描く地図は誤った危険を記す。","두려움으로 그린 지도는 틀린 위험을 표시한다."],
["The spring does not boast of the flood.","泉不夸耀洪流。","Родник не хвалится половодьем.","泉は洪水を誇らない。","샘은 홍수를 자랑하지 않는다."],
["A teacher plants what he will not harvest.","老师种下他不会收割之物。","Учитель сажает то что не пожнёт.","師は刈らぬものを植える。","스승은 거두지 않을 것을 심는다."],
["The ember waits longer than the flame.","余烬比火焰等得更久。","Тлеющий уголь ждёт дольше пламени.","熾火は炎より長く待つ。","잉걸불은 불꽃보다 오래 기다린다."],
["A wound names the place where growth begins.","伤口标记成长开始之处。","Рана называет место где начинается рост.","傷は成長の始まる場を名づける。","상처는 성장이 시작되는 자리를 가리킨다."],
["The shepherd counts by the ones that stray.","牧人以走失者来计数。","Пастух считает по тем что отбились.","羊飼いは逸れた者で数える。","목자는 길 잃은 것으로 헤아린다."],
["A lantern shared halves no one's light.","共享的灯笼不减任何人的光。","Разделённый фонарь не убавляет ничьего света.","分けた提灯は誰の光も減らさぬ。","나눈 등불은 누구의 빛도 줄이지 않는다."],
["The cocoon is patience wearing the shape of stillness.","茧是身着静止之形的耐心。","Кокон это терпение в облике покоя.","繭は静の形を纏う忍耐だ。","고치는 고요의 모습을 한 인내다."],
["A boundary crossed in kindness builds a road.","以善意跨越的边界筑成路。","Граница перейдённая с добром строит дорогу.","優しさで越えた境界は道を築く。","친절로 넘은 경계는 길을 놓는다."],
["The tree gives shade to those who throw stones.","树为投石者也献荫。","Дерево даёт тень и тем кто бросает камни.","木は石を投げる者にも陰を与える。","나무는 돌 던지는 이에게도 그늘을 준다."],
["A flame in the wind learns to lean and live.","风中之火学会倾斜而活。","Пламя на ветру учится клониться и жить.","風中の炎は傾いて生きるを学ぶ。","바람 속 불꽃은 기울어 사는 법을 배운다."],
["The brook sings loudest over the stones.","溪在石上唱得最响。","Ручей поёт громче всего над камнями.","小川は石の上で最も歌う。","시내는 돌 위에서 가장 크게 노래한다."],
["A wise word fits the ear it enters.","智慧之言契合它进入的耳。","Мудрое слово впору уху в которое входит.","賢い言葉は入る耳に合う。","지혜로운 말은 들어가는 귀에 맞는다."],
["The desert hides its rivers underground.","沙漠把河流藏于地下。","Пустыня прячет реки под землёй.","砂漠は川を地下に隠す。","사막은 강을 땅속에 감춘다."],
["A grudge forgiven returns as quiet strength.","被宽恕的怨恨化作静默的力量归来。","Прощённая обида возвращается тихой силой.","赦された恨みは静かな力で還る。","용서된 원한은 조용한 힘으로 돌아온다."],
["The hinge serves by yielding to both sides.","铰链以顺从两侧而效力。","Петля служит уступая обеим сторонам.","蝶番は両側に譲り仕える。","경첩은 양쪽에 양보하며 섬긴다."],
["A first frost teaches the leaf to let go.","初霜教叶放手。","Первый иней учит лист отпускать.","初霜は葉に手放すを教える。","첫 서리는 잎에 놓아주기를 가르친다."],
["The drum is hollow so the sound can live.","鼓中空，故声能存活。","Барабан полый чтобы звук мог жить.","太鼓は虚ろゆえ音が生きる。","북은 비어 있어 소리가 살 수 있다."],
["A lie told often wears the coat of truth.","常说的谎披上真理的外衣。","Ложь частая надевает плащ истины.","繰り返す嘘は真理の衣を纏う。","자주 한 거짓말은 진리의 외투를 두른다."],
["The harbor is patient with every late ship.","港对每艘迟来的船都有耐心。","Гавань терпелива к каждому опоздавшему судну.","港は遅れる船ごとに辛抱強い。","항구는 늦는 배마다 참을성이 있다."],
["A coal remembers the forest it once was.","煤记得它曾是的森林。","Уголь помнит лес которым был.","石炭はかつての森を憶えている。","석탄은 한때 숲이었음을 기억한다."],
["The needle leads but the thread does the binding.","针引路，线行缝合。","Игла ведёт но связывает нить.","針が導き糸が結ぶ。","바늘이 이끌고 실이 묶는다."],
["A truth grows roots in the soil of doubt.","真理在怀疑的土壤里生根。","Истина пускает корни в почве сомнения.","真理は疑いの土に根を張る。","진리는 의심의 흙에 뿌리내린다."],
["The wave that breaks still feeds the deep.","碎裂的浪仍滋养深海。","Разбившаяся волна всё же кормит глубь.","砕ける波もなお深みを養う。","부서지는 파도도 여전히 깊음을 먹인다."],
["A small mercy can outvote a great wrong.","小小的怜悯能胜过大错。","Малая милость может перевесить большое зло.","小さな慈悲は大きな過ちに勝りうる。","작은 자비가 큰 잘못을 이길 수 있다."],
["The trellis lends the vine a way to climb.","棚架借藤一条攀爬之路。","Шпалера одалживает лозе путь вверх.","棚は蔓に登る道を貸す。","격자는 덩굴에 오를 길을 빌려준다."],
["A name forgotten is a door quietly closing.","被遗忘的名是悄然合上的门。","Забытое имя это тихо затворяемая дверь.","忘れられた名は静かに閉じる扉だ。","잊힌 이름은 조용히 닫히는 문이다."],
["The sun asks nothing for the warmth it gives.","太阳为它所予的温暖一无所求。","Солнце ничего не просит за своё тепло.","太陽は与える温もりに何も求めぬ。","태양은 주는 온기에 아무것도 청하지 않는다."],
["A promise broken cracks more than one heart.","破碎的承诺裂的不止一颗心。","Нарушенное обещание трескает не одно сердце.","破られた約束は一つ以上の心を割る。","깨진 약속은 한 마음 이상을 쪼갠다."],
["The reed bends and so survives the gale.","芦苇弯折，故能熬过狂风。","Тростник гнётся и тем переживает шквал.","葦は撓み嵐を生き延びる。","갈대는 휘어 돌풍을 견뎌낸다."],
["A spark of envy dims the brightest gift.","一丝嫉妒使最亮的天赋黯淡。","Искра зависти гасит ярчайший дар.","嫉妬の火花は最も輝く才を曇らす。","질투의 불씨는 가장 밝은 재능을 흐린다."],
["The bridge remembers both banks at once.","桥同时记得两岸。","Мост помнит оба берега разом.","橋は両岸を同時に憶える。","다리는 두 기슭을 동시에 기억한다."],
["A long road shrinks beneath a willing foot.","漫漫长路在甘愿的脚下缩短。","Долгая дорога съёживается под охотной ногой.","長い道は厭わぬ足の下で縮む。","먼 길은 기꺼운 발 아래에서 줄어든다."],
["The lantern fears no wind it cannot see.","灯笼不惧它看不见的风。","Фонарь не боится ветра что не видит.","提灯は見えぬ風を恐れぬ。","등불은 보이지 않는 바람을 두려워 않는다."],
["A garden is an argument the seasons win.","花园是季节赢得的论辩。","Сад это спор который выигрывают сезоны.","庭は季節が勝つ論争だ。","정원은 계절이 이기는 논쟁이다."],
["The flame teaches by what it leaves unburnt.","火焰以其未烧之物施教。","Пламя учит тем что оставляет несгоревшим.","炎は焼き残すもので教える。","불꽃은 태우지 않은 것으로 가르친다."],
["A debt of silence is the hardest to repay.","沉默之债最难偿还。","Долг молчания тяжелее всего вернуть.","沈黙の負債は最も返し難い。","침묵의 빚은 갚기가 가장 어렵다."],
["The mountain stream forgets it was once snow.","山溪忘了它曾是雪。","Горный ручей забывает что был снегом.","山の流れは雪だったを忘れる。","산 시내는 한때 눈이었음을 잊는다."],
["A kind lie still bruises the truth beneath.","善意的谎仍伤及其下的真理。","Добрая ложь всё же ушибает истину под ней.","優しい嘘も下の真理を痛める。","선의의 거짓말도 아래 진실을 멍들게 한다."],
["The pendulum finds rest only at the center.","摆唯有在中心才得安息。","Маятник находит покой лишь в центре.","振り子は中心でのみ安らぐ。","추는 오직 중심에서만 쉼을 얻는다."],
["A bird sings before it sees the dawn.","鸟在见到黎明之前歌唱。","Птица поёт прежде чем увидит рассвет.","鳥は暁を見る前に歌う。","새는 새벽을 보기 전에 노래한다."],
["The chisel reveals what the stone already held.","凿子揭示石头早已蕴含之物。","Резец открывает то что камень уже хранил.","鑿は石が既に宿すものを露わにする。","끌은 돌이 이미 품은 것을 드러낸다."],
["A wound dressed in haste reopens at night.","匆忙包扎的伤口在夜里重裂。","Рана наскоро перевязанная вскрывается ночью.","急ぎ手当ての傷は夜に開く。","급히 싸맨 상처는 밤에 다시 터진다."],
["The river accepts the rain without counting drops.","河接纳雨而不数滴。","Река принимает дождь не считая капель.","川は雨を滴数えず受け入れる。","강은 비를 방울 세지 않고 받아들인다."],
["A whisper of hope outlasts a roar of fear.","一缕希望的低语胜过恐惧的咆哮。","Шёпот надежды переживает рёв страха.","希望の囁きは恐れの轟きより残る。","희망의 속삭임은 두려움의 포효보다 오래 간다."],
["The lighthouse stays though the ships forget it.","灯塔常在，纵使船只忘了它。","Маяк стоит хоть корабли его забыли.","灯台は船が忘れても立つ。","등대는 배들이 잊어도 서 있다."],
["A grain of salt remembers the whole sea.","一粒盐记得整片海。","Крупица соли помнит целое море.","一粒の塩は海全体を憶えている。","소금 한 알은 바다 전체를 기억한다."],
["The cart waits on the patience of the ox.","车依赖牛的耐心。","Телега ждёт терпения вола.","荷車は牛の忍耐に待つ。","수레는 소의 인내에 기댄다."],
["A gate is judged by what it lets through.","门以它所放行之物受评判。","Ворота судят по тому что пропускают.","門は通すものによって量られる。","문은 통과시키는 것으로 평가된다."],
["The frost flowers vanish at the first kind sun.","霜花在初阳和煦时消逝。","Морозные узоры тают при первом ласковом солнце.","霜の花は最初の優しい日に消える。","서리꽃은 첫 따스한 해에 사라진다."],
["A word of thanks plants more than it spends.","一句谢意所种多于所费。","Слово благодарности сеет больше чем тратит.","感謝の一言は費やすより多く蒔く。","감사의 한마디는 쓰는 것보다 많이 심는다."],
["The anvil is shaped by every blow it bears.","铁砧由它承受的每一击塑形。","Наковальня формуется каждым ударом что несёт.","金床は受ける打撃ごとに形作られる。","모루는 견디는 매질마다 형태가 잡힌다."],
["A path of fear circles back to its start.","恐惧之路绕回起点。","Путь страха возвращается к началу.","恐れの道は始まりへ巡り戻る。","두려움의 길은 시작으로 되돌아온다."],
["The candle and the dark agree on the room.","烛与黑暗就房间达成一致。","Свеча и тьма согласны о комнате.","蝋燭と闇は部屋について合意する。","촛불과 어둠은 방에 대해 합의한다."],
["A song half-remembered still finds the heart.","半记得的歌仍能触及心。","Песня полузабытая всё же находит сердце.","半ば憶えた歌もなお心に届く。","반쯤 기억한 노래도 마음을 찾는다."],
["The vine repays the wall that held it up.","藤回报扶持它的墙。","Лоза вознаграждает стену что держала её.","蔓は支えた壁に報いる。","덩굴은 받쳐 준 벽에 보답한다."],
["A truth shouted loses the ear it sought.","被吼出的真理失去它所求的耳。","Истина прокричанная теряет искомое ухо.","叫ばれた真理は求めた耳を失う。","외쳐진 진리는 찾던 귀를 잃는다."],
["The mountain keeps its snow for the summer thirst.","山为夏日之渴存其雪。","Гора хранит снег для летней жажды.","山は夏の渇きに雪を蓄える。","산은 여름 갈증을 위해 눈을 간직한다."],
["A door half-open invites both wind and word.","半开的门同邀风与言。","Полуоткрытая дверь зовёт и ветер и слово.","半開きの扉は風と言葉を招く。","반쯤 연 문은 바람과 말을 함께 부른다."],
["The seed does not fear the dark it grows in.","种子不惧它生长其中的黑暗。","Семя не боится тьмы в которой растёт.","種は育つ闇を恐れぬ。","씨앗은 자라는 어둠을 두려워 않는다."],
["A bridge of words spans a silence of years.","言语之桥跨越数年的沉默。","Мост слов перекрывает молчание лет.","言葉の橋は歳月の沈黙を渡す。","말의 다리는 여러 해의 침묵을 잇는다."],
["The flame remembers each hand it warmed.","火焰记得它温暖过的每只手。","Пламя помнит каждую руку что согрело.","炎は温めた手ごとを憶える。","불꽃은 데워 준 손마다를 기억한다."],
["A patient hour outweighs a hasty year.","耐心的一小时胜过仓促的一年。","Терпеливый час весомее поспешного года.","忍耐の一時は性急の一年に勝る。","인내의 한 시간이 성급한 한 해보다 무겁다."],
["The harbor lamp burns for ships not yet seen.","港灯为尚未望见的船燃烧。","Огонь гавани горит для ещё невидимых судов.","港の灯はまだ見えぬ船に燃える。","항구의 등불은 아직 안 보이는 배를 위해 탄다."],
["A small kindness can reroute a whole day.","小小的善意能改变一整天的走向。","Малая доброта может перенаправить весь день.","小さな親切は一日丸ごとを変えうる。","작은 친절이 하루 전체를 바꿀 수 있다."],
["The oak recalls the storm that bent it young.","橡树记得幼时弯它的风暴。","Дуб помнит бурю что согнула его юным.","樫は若い頃撓めた嵐を憶える。","참나무는 어릴 때 휘게 한 폭풍을 기억한다."],
["A vow whispered binds as tight as one cried.","低声的誓言束缚得如喊出的一般紧。","Клятва шёпотом вяжет как тесно крикнутая.","囁いた誓いは叫んだものと同じく縛る。","속삭인 맹세는 외친 것만큼 단단히 묶는다."],
["The mill turns only while the water gives.","磨坊只在水流给力时转动。","Мельница вертится лишь пока вода даёт.","水車は水が与える間だけ回る。","물레방아는 물이 줄 때만 돈다."],
["A question kept warm hatches into wisdom.","保温的问题孵化成智慧。","Вопрос хранимый в тепле выводит мудрость.","温め続けた問いは知恵に孵る。","따뜻이 품은 물음은 지혜로 부화한다."],
["The shore reshapes itself for every tide.","岸为每一次潮汐重塑自身。","Берег переформуется под каждый прилив.","岸は潮ごとに己を作り直す。","기슭은 조수마다 스스로를 다시 빚는다."],
]

assert all(len(c) == 5 for c in TIER3), "TIER3 row not 5-lang aligned"
assert len(set(c[0] for c in TIER3)) == len(TIER3), "duplicate Tier-3 EN proposition"
_base_en = set(c[0] for c in BASE100)
assert not (_base_en & set(c[0] for c in TIER3)), "Tier-3 collides with base concept"

# corpus_real500 Tier-3 extension (concepts 250..499). Author ONLY if quality holds; if left empty the honest
# ceiling stays NC=250 (a valid honest outcome per the rung4 milestone — NO synthetic padding).
TIER3_EXT500 = []   # intentionally empty: honest NC ceiling = 250 (see CORPUS_CARD.md rationale)

LANGS_LOCAL = LANGS

def build(target_nc, tier3_rows):
    concepts = BASE100 + tier3_rows
    assert len(concepts) == target_nc, (len(concepts), target_nc)
    assert all(len(c) == 5 for c in concepts)
    assert len(set(c[0] for c in concepts)) == target_nc, "duplicate EN concept overall"
    return concepts

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

LIMEN_MAGIC = b"LIMEN\x00\x00\x00"; LIMEN_VER = 2
def anchor_record(idx, concept_id, lang, text, n_concepts):
    payload = text.encode("utf-8")
    coord_x = round(concept_id / max(1, n_concepts - 1), 4)
    coord_y = round(LANGS_LOCAL.index(lang) / max(1, len(LANGS_LOCAL) - 1), 4)
    head = {"id": f"a{idx:04d}", "concept": concept_id, "lang": lang,
            "coord": [coord_x, coord_y], "lane": lang, "radius": 1.0, "tier": 0,
            "tags": ["clm", "semantic", lang],
            "payload_len": len(payload), "payload_sha256": sha256_hex(payload)}
    head_b = json.dumps(head, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(head_b)) + head_b + payload, payload

def write_limen(path, concepts):
    n_concepts = len(concepts)
    records = []
    for ci, concept in enumerate(concepts):
        for li, txt in enumerate(concept):
            records.append((ci, LANGS_LOCAL[li], txt))
    blob = bytearray(); blob += LIMEN_MAGIC
    blob += struct.pack("<I", LIMEN_VER); blob += struct.pack("<I", len(records))
    payloads = []
    for idx, (cid, lang, txt) in enumerate(records):
        rec, payload = anchor_record(idx, cid, lang, txt, n_concepts)
        blob += struct.pack("<I", len(rec)); blob += rec; payloads.append(payload)
    root = merkle_root(payloads); blob += root
    with open(path, "wb") as f: f.write(blob)
    return sha256_hex(bytes(blob)), root.hex(), len(records)

def byte_len_stats(concepts, tier_ranges):
    """per-tier mean byte-length of payloads + pairwise L1 separation of byte-length histograms. numpy-free."""
    import math
    NBINS = 20; LO_EDGE = 0.0; HI_EDGE = 800.0; W = (HI_EDGE - LO_EDGE) / NBINS
    out = {}; dists = {}
    for name, (lo, hi) in tier_ranges.items():
        lens = []
        for ci in range(lo, hi):
            for li in range(5):
                lens.append(len(concepts[ci][li].encode("utf-8")))
        n = len(lens); mean = sum(lens) / n
        var = sum((x - mean) ** 2 for x in lens) / n
        out[name] = {"n_anchors": n, "mean_bytes": round(mean, 2),
                     "sd_bytes": round(math.sqrt(var), 2), "min": min(lens), "max": max(lens)}
        h = [0.0] * NBINS
        for x in lens:
            b = int((x - LO_EDGE) / W)
            if b < 0: b = 0
            if b >= NBINS: b = NBINS - 1
            h[b] += 1.0
        s = sum(h) or 1.0
        dists[name] = [v / s for v in h]
    l1 = {}; names = list(dists.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            d = sum(abs(dists[names[i]][b] - dists[names[j]][b]) for b in range(NBINS))
            l1[f"{names[i]}__vs__{names[j]}"] = round(d, 4)
    return out, l1

def emit(target_nc, tier3_rows, out_dir, label):
    OUT = os.path.expanduser(out_dir); os.makedirs(OUT, exist_ok=True)
    concepts = build(target_nc, tier3_rows)
    shard = os.path.join(OUT, "parallel.limen")
    sha, merkle, count = write_limen(shard, concepts)
    tier_ranges = {"tier1_flores_gold": (0, 50), "tier2_authored_prior": (50, 100),
                   "tier3_model_authored_new": (100, target_nc)}
    stats, l1 = byte_len_stats(concepts, tier_ranges)
    manifest = {"corpus": f"clm-kosmos-akida-{label}", "kosmos_version": "2.0",
                "n_concepts": target_nc, "n_anchors": count, "langs": LANGS_LOCAL,
                "tiers": {
                    "tier1_flores_gold": {"concepts": "0..49", "count": 50,
                        "provenance": "FLORES parallel sentences, byte-preserved from corpus_big/corpus_real100 — REAL GOLD, NOT model-authored"},
                    "tier2_authored_prior": {"concepts": "50..99", "count": 50,
                        "provenance": "hand-authored aligned propositions deployed+verified at rung3 NC=100 (40 aphorisms + 10 new)"},
                    "tier3_model_authored_new": {"concepts": f"100..{target_nc-1}", "count": target_nc - 100,
                        "provenance": "model-authored aligned (real-semantic, NOT FLORES-gold, NOT synthetic) — NEW for rung4"}},
                "byte_len_stats_per_tier": stats, "byte_hist_L1_separation": l1,
                "sha256": sha, "merkle": merkle}
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2, ensure_ascii=False)
    print(f"[{label}] {count} anchors / {target_nc} concepts -> {shard}")
    print(f"[{label}] sha256={sha}")
    print(f"[{label}] merkle={merkle}")
    print(f"[{label}] per-tier byte-len: {json.dumps(stats)}")
    print(f"[{label}] byte-hist L1 separation: {json.dumps(l1)}")
    return manifest

if __name__ == "__main__":
    m250 = emit(250, TIER3, "~/clm_kosmos_akida/corpus_real250", "real250")
    if len(TIER3_EXT500) == 250:
        emit(500, TIER3 + TIER3_EXT500, "~/clm_kosmos_akida/corpus_real500", "real500")
    else:
        print(f"[real500] SKIPPED — Tier-3 ext authored={len(TIER3_EXT500)}/250. Honest real ceiling = NC=250 "
              f"(NO synthetic padding; faithful authoring stopped at the honest NC). a_paper_negative_ok valid outcome.")
