#!/usr/bin/env python3
"""Lane A REAL-SCALE corpus (rung3) — 100 genuine cross-lingual ALIGNED concepts, NOT synthetic.

substrate-agnostic builder (the chip pipeline is byte-identical to corpus_big). a_scale_honest_scope.

PROVENANCE (honest, g63 — REAL semantic, no synthetic byte-patterns, no fabrication):
  concepts 0..49  = the EXACT 50 FLORES cross-lingual parallel sentences deployed in corpus_big
                    (byte-preserved from ~/clm_kosmos_akida/corpus_big/parallel.limen) — real news/
                    factual parallel translations (en zh ru ja ko).
  concepts 50..89 = 40 hand-authored cross-lingual ALIGNED aphorisms (each = the SAME proposition
                    rendered in 5 langs), verbatim from build_corpus_large.py (clm-akida-semantic-signal-lift).
  concepts 90..99 = 10 newly hand-authored cross-lingual ALIGNED propositions (same authoring method,
                    each a genuine proposition in en zh ru ja ko).
  => 100 DISTINCT real aligned concepts x 5 langs = 500 real anchors. This PUSHES real NC past the
     prior 50-concept real ceiling WITHOUT synthetic padding (the c4 source file has only 5 distinct
     parallel concepts; >50 real aligned concepts must be hand-authored — that authoring IS real data).
  LIMEN format byte-identical to build_corpus.py; concept/lang headers match corpus_big so every
  harness (which subsets by concept) consumes it UNCHANGED.
"""
import os, json, struct, hashlib
OUT = os.path.expanduser("~/clm_kosmos_akida/corpus_real100")
os.makedirs(OUT, exist_ok=True)
LANGS = ["en", "zh", "ru", "ja", "ko"]
CONCEPTS = [
[
"On Monday, scientists from the Stanford University School of Medicine announced the invention of a new diagnostic tool that can sort cells by type: a tiny printable chip that can be manufactured using standard inkjet printers for possibly about one U.S. cent each.",
"周一，斯坦福大学医学院的科学家宣布，他们发明了一种可以将细胞按类型分类的新型诊断工具：一种可打印的微型芯片。这种芯片可以使用标准喷墨打印机制造，每片价格可能在一美分左右。",
"В понедельник ученые из Медицинской школы Стэнфордского университета объявили об изобретении нового диагностического инструмента, который может сортировать клетки по их типу; это маленький чип, который можно напечатать, используя стандартный струйный принтер примерно за 1 цент США.",
"月曜日にスタンフォード大学医学部の科学者たちは、細胞を種類別に分類できる新しい診断ツールを発明したと発表しました。それは標準的なインクジェットプリンタで印刷して製造できる小型チップであり、原価は1枚あたり1円ほどす。",
"스탠포드 의과대학 연구진은 지난 월요일 세포를 유형별로 분류할 수 있는 새로운 진단도구를 개발했다고 밝혔다. 이는 아주 작은 크기의 인쇄가 가능한 칩으로, 일반적인 잉크젯 프린터를 이용해 개 당 미화 약 1센트로 생산이 가능할 것으로 예상된다."
],
[
"Lead researchers say this may bring early detection of cancer, tuberculosis, HIV and malaria to patients in low-income countries, where the survival rates for illnesses such as breast cancer can be half those of richer countries.",
"主要研究人员表示，这可以让低收入国家/地区的患者尽早发现癌症、肺结核、艾滋病和疟疾。在这些国家/地区，乳腺癌等疾病的生存率可能仅为富裕国家的一半。",
"Ведущие исследователи утверждают, что он может помочь в раннем выявлении рака, туберкулеза, ВИЧ и малярии у пациентов в странах с низким уровнем дохода, где показатели выживаемости при таких болезнях, как рак молочной железы, могут быть в два раза ниже, чем в более богатых странах.",
"主任研究者は、これは低所得国における患者の癌、結核、HIV、マラリアの早期発見につながる可能性があると述べます。こうした国では、乳がんなどの病気の生存率が豊かな国の半分になることもあるとされます。",
"수석 연구진들은 이것이 선진국 대비 절반의 생존율을 보이는 저소득 국가들의 환자들에게 암, 결핵, HIV 그리고 말라리아의 조기 발견을 가져올 수 있다고 설명합니다."
],
[
"The JAS 39C Gripen crashed onto a runway at around 9:30 am local time (0230 UTC) and exploded, closing the airport to commercial flights.",
"当地时间上午 9:30 左右 (UTC 0230)，JAS 39C 鹰狮战斗机撞上跑道并发生爆炸，导致机场关闭，商业航班无法正常起降。",
"Приблизительно в 9:30 по местному времени (02:30 UTC) JAS 39C Gripen упал на взлетно-посадочную полосу и взорвался. Аэропорт пришлось закрыть для коммерческих рейсов.",
"JAS 39Cグリペンは現地時間の午前9時30分頃（UTC 0230）に滑走路に墜落して爆発し、その影響で空港の商業便が閉鎖されました。",
"현지 시간으로 약 아침 9시 30분(0230 UTC)에 JAS 39C 그리펜이 활주로에 추락 후 폭발해, 공항의 상업 항공편 운항이 중단되었습니다."
],
[
"The pilot was identified as Squadron Leader Dilokrit Pattavee.",
"涉事飞行员是空军中队长迪罗里·帕塔维 (Dilokrit Pattavee)。",
"Личность пилота была установлена. Им оказался командир эскадрильи Дилокрит Паттави.",
"操縦士は中隊長のディロクリット・パタヴェー氏であることが確認されました。",
"그 조종사는 비행 중대장 딜로크리트 패타비로 확인되었다."
],
[
"Local media reports an airport fire vehicle rolled over while responding.",
"当地媒体报道，一辆机场消防车在响应火警时翻了车。",
"Местные СМИ сообщают, что в аэропорту по пути на вызов перевернулась пожарная машина.",
"地元メディアの報道によると、空港の消防車が対応中に横転したということです。",
"현지 언론은 공항 소방차가 사고에 대응하는 도중에 전복되었다고 보도했습니다."
],
[
"28-year-old Vidal had joined Barça three seasons ago, from Sevilla.",
"三个赛季前，28岁的比达尔（Vidal）从塞维利亚队加盟巴萨。",
"28-летний Алеш Видаль перешел в \"Барсу\" из \"Севильи\" три сезона назад.",
"28歳のビダル選手は、3シーズン前にセビージャから移籍してバルサに所属していました。",
"28세인 비달은 3년 전 세비야 FC에서 FC 바르셀로나에 합류했습니다."
],
[
"Since moving to the Catalan-capital, Vidal had played 49 games for the club.",
"自从转会到加泰罗尼亚的首府球队，维达尔已经为俱乐部踢了 49 场比赛。",
"После переезда в столицу Каталонии  Видаль провел за клуб 49 матчей.",
"カタルーニャの州都に移って以来、ビダルはクラブで49試合に出場しました。",
"바르셀로나로 이적한 후 비달은 클럽을 위해 49경기를 뛰었습니다."
],
[
"The protest started around 11:00 local time (UTC+1) on Whitehall opposite the police-guarded entrance to Downing Street, the Prime Minister's official residence.",
"抗议活动于当地时间 11:00 (UTC+1) 左右在白厅 (Whitehall) 开始，白厅对面是首相官邸唐宁街的入口处，由警察看守。",
"Протест начался около 11:00 по местному времени (UTC+1) на улице Уайтхолл напротив охраняемого полицией въезда на Даунинг-стрит, официальную резиденцию премьер-министра.",
"抗議行動は、現地時間11:00（UTC+1）頃にホワイトホール通りで始まり、首相官邸があるダウニング街の警察が警備する入口の向かいに群衆が集結しました。",
"시위는 총리의 공식 거주지인 다우닝가의 경찰이 경비를 서는 입구 맞은편 화이트홀에서 현지 시간 11:00(UTC+1) 경에 시작되었습니다."
],
[
"Just after 11:00, protesters blocked traffic on the northbound carriage in Whitehall.",
"11 点刚过，抗议者便堵住了白厅北行车道的交通。",
"Сразу после 11:00 протестующие перекрыли движение в северном направлении по Уайтхоллу.",
"11時すぎちょうどに抗議者たちはホワイトホールの北行き車両の交通を遮断しました。",
"11시가 막 지난 후, 시위대는 화이트홀에 있는 북쪽으로 향하는 마차들의 교통을 막았다."
],
[
"At 11:20, the police asked the protesters to move back on to the pavement, stating that they needed to balance the right to protest with the traffic building up.",
"11 点 20 分，警察要求抗议者退回到人行道，并告知抗议者，在行使抗议权利时，务必考虑到越来越拥堵的公共交通问题。",
"В 11:20 полиция попросила митингующих вернуться на тротуар, заявив, что им необходимо соблюдать баланс между правом протестовать и задержкой дорожного движения.",
"11時20分になると、警察は抗議する権利と交通量のバランスを弁える必要があると告げて、抗議者たちに歩道に戻るように求めました。",
"11시 20분에 경찰이 시위대에게 보도로 돌아가도록 요청했으며, 시위할 권리와 증가하는 교통량 사이에 절충할 필요가 있다고 말했습니다."
],
[
"Around 11:29, the protest moved up Whitehall, past Trafalgar Square, along the Strand, passing by Aldwych and up Kingsway towards Holborn where the Conservative Party were holding their Spring Forum in the Grand Connaught Rooms hotel.",
"11 点 29 分左右，抗议人群向前行进至白厅，经过特拉法尔加广场、斯特兰德大街、奥德维奇、京士威，向霍尔本行进，保守党正在当地的 Grand Connaught Rooms 酒店举行春季论坛。",
"Около 11:29 протестующие двинулись вверх по Уайтхолл, мимо Трафальгарской площади, вдоль Стрэнда, мимо Олдвича и вверх по Кингсуэй в сторону района Холборн, где Консервативная партия проводила свой Весенний форум в гостинице Grand Connaught Rooms.",
"11時29分頃、デモ隊は英国政府に向かい、トラファルガー広場を通り過ぎて、ストランド街沿いにアルドウィックのそばを通り抜け、キングスウェイをホルボーンに向かって進みましたが、そこでは保守党がグランドコンノートルームズホテルで春季フォーラムを開催していました。",
"11시 29분 경, 시위대는 스트랜드를 따라 트라팔가 광장을 지나 화이트 홀로 입성했으며, 알드 위치를 지나, 킹스웨이로 들어가 보수당이 그랜드 코너트 룸스 호텔에서 스프링 포럼을 열고 있던 홀본 쪽으로 향했다."
],
[
"Nadal's head to head record against the Canadian is 7–2.",
"纳达尔（Nadal）与加拿大人的交手记录是 7-2。",
"Рекорд Надала в схватках один на один с канадцем —  7–2.",
"ナダルの対カナダ戦の戦績は7-2です。",
"나달과 이 캐나다 선수와의 정면 대결 기록은 7 대 2입니다."
],
[
"He recently lost against Raonic in the Brisbane Open.",
"不久前，他在布里斯班公开赛上败于拉奥尼奇。",
"Недавно он проиграл Раоничу на турнире в Брисбене.",
"最近では、ブリスベン・オープンでラオニッチに敗れています。",
"그는 최근 브리즈번 오픈(Brisbane Open) 경기에서 라오니치(Raonic)에게 패했다."
],
[
"Nadal bagged 88% net points in the match winning 76 points in the first serve.",
"纳达尔（Nadal ）在比赛中把 88% 的净胜分收入囊中，在第一个发球局赢得 76 分。",
"Надал набрал 88% всех очков в матче, выиграв 76 очков  в первой подаче.",
"試合中にナダルはファーストサーブで76ポイントを奪い、88%のネットポイントを獲得しています。",
"나달은 첫 서브에서 76점을 획득하며 88%의 네트 포인트를 달성했습니다."
],
[
"After the match, King of Clay said, \"I am just excited about being back in the final rounds of the most important events. I am here to try to win this.\"",
"赛后，红土之王拉斐尔·纳达尔称：“我很开心重返能这项重大赛事的决赛，我会尽全力争取夺冠。”",
"После матча \"Король грунта\" сказал: \"Я так рад, что вернусь в финальные раунды самых важных мероприятий. Я здесь, чтобы попытаться выиграть\".",
"試合後にキング・オブ・クレーは、「最も重要なイベントの決勝に戻ってきたことに興奮している。これに勝つためにここに来た」と語りました。",
"경기가 끝난 후 클레이의 왕은 “가장 중요한 종목의 마지막 라운드에 복귀한 것만으로도 기쁘다. 이번 대회에서 우승하려고 왔다.”고 말했다."
],
[
"\"Panama Papers\" is an umbrella term for roughly ten million documents from Panamanian law firm Mossack Fonseca, leaked to the press in spring 2016.",
"“巴拿马文件” 是巴拿马莫萨克·冯塞卡律师事务所 (Mossack Fonseca) 约 1,000 万份文件的总称，这些文件在 2016 年春季被爆料给媒体。",
"\"Панамские документы\" — это собирательное название приблизительно десяти миллионов документов панамской юридической фирмы Mossack Fonseca, просочившихся в прессу весной 2016 г.",
"「パナマ文書とは」、2016年春にパナマの法律事務所モサック・フォンセカから報道機関に流出した脱税行為に関する書類の総称で、その総数はおよそ1000万件です。",
"\"\"\"파나마 페이퍼스(Panama Papers)\"\"는 2016년 봄, 언론에 유출된 파나마 법률 회사인 모색 폰세카(Mossack Fonseca)의 약 천만 건에 이르는 문서를 의미하는 포괄적인 용어입니다.\""
],
[
"The documents showed fourteen banks helped wealthy clients hide billions of US dollars of wealth to avoid taxes and other regulations.",
"文件显示，十四家银行帮助富有的客户隐藏了数十亿美元的财富来逃避税收和其它监管。",
"Документы показали, что четырнадцать банков помогли состоятельным клиентам спрятать миллиарды долларов США, чтобы избежать уплаты налогов и выполнения прочих нормативных требований.",
"文書には、富裕層の顧客が税金等の規制を逃れて数十億ドルの資産を隠す際に14の銀行が手助けしたことが示されています。",
"문서에 따르면 14개의 은행이 부유한 고객을 도와 세금 및 기타 규제를 피할 수 있도록 미화 수십억 달러를 숨기게 해줬습니다."
],
[
"British newspaper The Guardian suggested Deutsche Bank controlled roughly a third of the 1200 shell companies used to accomplish this.",
"英国《卫报》指出，在用于实现这一目标的 1200 家空壳公司中，德意志银行控制了大约三分之一。",
"Британская газета The Guardian  предположила, что Deutsche Bank контролировал примерно треть из 1200 подставных компаний, использованных для этой цели.",
"英国のガーディアン紙は、ドイツ銀行が1200社のペーパーカンパニーの約3分の1を支配していることを示唆しました。",
"영국 신문 가디언지는 도이치 뱅크는 이것을 이루기 위해 사용된 대략 1200개의 비활동 회사 중 삼 분의 일을 조종했다고 시사했다."
],
[
"There were protests worldwide, several criminal prosecutions, and the leaders of the governments of Iceland and Pakistan both resigned.",
"世界各地都发生了抗议活动，有几起刑事诉讼，冰岛和巴基斯坦政府的领导人都辞职了。",
"По всему миру происходили протесты, было несколько уголовных преследований, а главы правительств Исландии и Пакистана ушли в отставку.",
"世界中で抗議の声が上がり、何件もの刑事告発があり、アイスランドとパキスタンの両政府の指導者が辞任しました。",
"전 세계적으로 시위가 있었고, 여러 건의 형사 고발이 있었으며, 파키스탄 정부와 아이슬란드 정부의 지도자들은 모두 사임했다."
],
[
"Born in Hong Kong, Ma studied at New York University and Harvard Law School and once held an American permanent resident \"green card\".",
"马生于香港，曾就读于纽约大学和哈佛大学法学院，还一度持有美国永久居民身份证“绿卡”。",
"Ма родился в Гонконге, учился в Нью-Йоркском университете и Гарвардской юридической школе. Он также когда-то имел постоянный вид на жительство в Америке (\"грин-карту\").",
"香港生まれの馬英九は、ニューヨーク大学とハーバード大学法学大学院を卒業し、米国の永住権「グリーンカード」を保有していたこともあります。",
"마(Ma) 씨는 홍콩에서 태어나 뉴욕대와 하버드대 로스쿨에서 공부했으며 미국 영주권자 '그린카드'를 소지한 적이 있다."
],
[
"Hsieh implied during the election that Ma might flee the country during a time of crisis.",
"谢长廷在选举期间暗示，马英九在遇到危机时可能会逃离台湾。",
"Во время проведения выборов Се намекал, что Ма может покинуть страну в случае кризиса.",
"選挙中に謝氏は、危機に陥ったら馬氏は逃げ出すかもしれないとほのめかしていました。",
"셰이(Hsieh)는 선거 기간 동안 마(Ma)가 위기의 시기에 망명할 수 있음을 암시했습니다."
],
[
"Hsieh also argued that the photogenic Ma was more style than substance.",
"谢长廷还声称马英九虽然很上镜，但中看不中用。",
"Се также утверждал, что фотогеничный Ма больше выделялся внешностью, чем харизмой.",
"謝長廷は、馬英九について実物よりも写真写りが良いと主張していました。",
"또한 셰이는 사진 잘 받는 마가 스타일은 멋있지만 실속은 없다고 말했습니다."
],
[
"Despite these accusations, Ma won handily on a platform advocating closer ties with the Chinese mainland.",
"尽管受到这些指责，马英九在一次演讲中主张与中国大陆建立更加紧密的联系，并轻松获胜。",
"Несмотря на эти обвинения, Ма легко победил, выступая за более тесные связи с материковой частью Китая.",
"こうした非難にもかかわらず、馬氏は中国大陸との緊密な関係を標榜して楽勝でした。",
"이러한 고발에도 불구하고, 마는 중국 본토와의 긴밀한 유대를 옹호하는 플랫폼을 쉽게 얻었습니다."
],
[
"Today's Player of the Day is Alex Ovechkin of the Washington Capitals.",
"今日最佳选手是来自华盛顿首都队的亚历克斯·奥韦奇金。",
"Сегодняшний игрок дня — Алекс Овечкин из Washington Capitals.",
"今日のプレイヤー・オブ・ザ・デイは、ワシントン・キャピトルズのアレックス・オヴェーチキン選手です。",
"오늘의 선수는 워싱턴 캐피털즈의 알렉스 오베츠킨입니다."
],
[
"He had 2 goals and 2 assists in Washington's 5-3 win over the Atlanta Thrashers.",
"在华盛顿队以 5-3 的比分战胜亚特兰大鸫鸟队的比赛中，他贡献了 2 个进球和 2 次助攻。",
"У него было 2 гола и 2 передачи в матче футбольного клуба \"Вашингтон\" против \"Атланта Трэшерз\", в котором первый одержал победу со счётом 5-3.",
"ワシントンがアトランタ・トラッシャーズに5-3で勝利した際には2ゴール2アシストを記録しています。",
"Atlanta Thrashers를 상대로 5-3으로 이긴 Washington의 경기에서 그는 골 2개와 어시스트 2개를 기록했습니다."
],
[
"Ovechkin's first assist of the night was on the game-winning goal by rookie Nicklas Backstrom;",
"奥韦奇金（Ovechkin）当晚的第一个助攻，来自新秀尼克拉斯·贝克斯特伦 (Nicklas Backstrom) 的制胜一球;",
"Первая голевая передача Овечкина в тот вечер принесла команде победный гол, выполненный новичком Никласом Бекстрёмом;",
"この夜、オベーチキンの最初のアシストは、ルーキーのニックラス・バックストロームが決めた決勝ゴールでした。",
"그날 밤 오베치킨의 첫 어시스트는 신인 니클라스 백스트롬의 경기 결승골로 이어졌습니다."
],
[
"his second goal of the night was his 60th of the season, becoming the first player to score 60 or more goals in a season since 1995-96, when Jaromir Jagr and Mario Lemieux each reached that milestone.",
"他当晚的第二个进球是他本赛季的第60个进球，成为自1995-96赛季以来首位在一个赛季中打进60个或更多进球的球员——在1995-96赛季，亚罗米尔·雅格和马里奥·拉缪都达到了这一里程碑。",
"Его второй целью в этот вечер был его 60-й гол в сезоне, в результате чего он становился первым игроком забившим 60 или больше голов в сезоне с 1995-96 гг., когда Джаромир Джагр  и Марио Лемьо оба добились этого достижения.",
"その夜の2つ目のゴールは、彼の今季60点目のゴールとなりました。1シーズンで60点以上を記録した選手は、1995～1996年のジャロミア・ジャグとマリオ・ルミュー以来という快挙でした。",
"그날 밤 그의 두 번째 골은 시즌의 시즌의 60번째였으며, 1995-1996년 시즌에 야르오미르 야그르와 마리오 르뮤 이후 처음으로 60번 이상 득점을 한 선수가 되었다."
],
[
"Batten was ranked 190th on the 2008 400 Richest Americans list with an estimated fortune of $2.3 billion.",
"巴滕位列 2008 年全美最富有 400 人榜单第 190 位，预计其财富达到约 23 亿美元。",
"Баттен занял 190-е место в списке 400 богатейших американцев в 2008 году, его состояние оценивалось в 2,3 миллиарда долларов США.",
"バッテン氏は2008年版アメリカ長者番付で190位に入り、推定資産額は23億ドルでした。",
"배튼씨는 2008년 400명의 미국 내 부자 순위에서 약 23억 달러의 재산으로 190위에 올랐다."
],
[
"He graduated from the College of Arts & Sciences of the University of Virginia in 1950 and was a significant donor to that institution.",
"他在 1950 年毕业于弗吉尼亚大学艺术与科学学院，并且是该校的重要捐赠者。",
"Он окончил колледж искусств и наук Виргинского университета в 1950 году и был важным спонсором этого учреждения.",
"彼は、1950年にバージニア大学芸術科学部を卒業し、同大学に多額の寄付をしました。",
"그는 1950년에 버지니아 대학에서 예술 과학을 전공으로 졸업했고 상당한 기부자로 명성을 남겼다."
],
[
"Iraq's Abu Ghraib prison has been set alight during a riot.",
"伊拉克的阿布格莱布监狱在一次暴乱中着火。",
"Иракская тюрьма Абу-Грейб была подожжена во время бунта.",
"イラクのアブ・グライブ刑務所が暴動の最中に放火されました。",
"이라크의 아부 그라이브 교도소에서 폭동이 일어난 동안 화재가 발생했습니다."
],
[
"The jail became notorious after prisoner abuse was discovered there after US forces took over.",
"美军接管后，该监狱发现了虐囚事件，自此变得声名狼藉。",
"Тюрьма получила скандальную известность после раскрытия издевательств над заключенными, происходивших в ней, когда она перешла под контроль американских военных.",
"米軍による占領後、囚人の虐待が発覚し、当該刑務所の悪名がとどろきました。",
"미군 점령 후에 수감자 학대 사건이 밝혀지자 교도소의 악명은 높아졌다."
],
[
"Piquet Jr. crashed in the 2008 Singapore Grand Prix just after an early pit stop for Fernando Alonso, bringing out the safety car.",
"在 2008 年新加坡大奖赛上，费尔南多·阿隆索提前进站后，小皮奎特发生撞车，迫使安全车出场。",
"Пике-младший попал в аварию на Гран-при Сингапура в 2008 году сразу после раннего пит-стопа Фернандо Алонсо, после чего пришлось задействовать машину безопасности.",
"ピケJr.は2008年のシンガポールGPで、フェルナンド・アロンソが早めにピットインした直後にクラッシュし、セーフティーカーが導入されました。",
"피케 주니어는 2008년 싱가포르 그랑프리에서 페르난도 알론소가 미리 피트스톱을 실시한 직후 사고를 내 세이프티카가 발령되도록 하였습니다."
],
[
"As the cars ahead of Alonso went in for fuel under the safety car, he moved up the pack to take victory.",
"当位于阿隆索前面的赛车在安全车的引领下进行加油时，他趁机抢先，最终赢得了胜利。",
"Когда машины впереди Алонсо отправились за топливом под машину безопасности, он двинулся вверх, чтобы взять победу.",
"先行するマシンがセーフティカーの後ろで燃料を補給する中、アロンソは集団の中で順位を上げて勝利を手にしました。",
"알론소 앞에 있던 차들이 안전차 밑으로 연료를 넣으러 들어가자, 그는 승기를 잡기 위해 무리를 옮겼다."
],
[
"Piquet Jr. was sacked after the 2009 Hungarian Grand Prix.",
"小皮奎特在 2009 年匈牙利大奖赛之后被解雇。",
"Пике-младший не был допущен к гонкам после Гран-при Венгрии 2009 года.",
"ピケJr.は2009年のハンガリーGP後に解雇されました。",
"피케 주니어(Piquet Jr.)는 2009년 헝가리 그랑프리 이후 파면되었다."
],
[
"At exactly 8:46 a.m. a hush fell across the city, marking the exact moment the first jet struck its target.",
"正值上午 8 点 46 分，整座城市陷入了寂静，标示了第一架飞机撞上目标的确切时间。",
"Ровно в 08:46 весь город замер, обозначив тот самый момент, когда первый самолёт ударил по цели.",
"午前8時46分ちょうどに街中が静寂に包まれました。最初のジェット機が目標に衝突した瞬間でした。",
"정적이 도시 전체에 덮여 있는 정확히 오전 8시 46분, 그 순간 첫 번째 제트기가 타깃을 맞췄다."
],
[
"Two beams of light have been rigged up to point skywards overnight.",
"两束光被临时造出，彻夜指向天空。",
"Были установлены два источника света, лучи от которых были направлены в ночное небо.",
"二筋の光が一晩中空に向かうように配備されています。",
"두 광선 기둥이 밤새 하늘 방향을 가리키기 위해 설치되어 있었습니다."
],
[
"Construction is ongoing for five new skyscrapers at the site, with a transportation center and memorial park in the middle.",
"该地点正在建设五座新摩天大楼，中间有一个交通中心和纪念公园。",
"На этом месте ведется стройка пяти новых небоскрёбов с транспортным центром и мемориальным парком посередине.",
"敷地内には新たに5つの超高層ビルが建設中で、その中央には交通センターと記念公園があります。",
"현장에서는 다섯 개의 고층 건물과 가운데 위치하는 교통 센터와 기념 공원이 건설 중입니다."
],
[
"The PBS show has more than two-dozen Emmy awards, and its run is shorter only than Sesame Street and Mister Rogers' Neighborhood.",
"PBS 电视台的这个节目荣获二十多项艾美奖，其播出历史仅次于《芝麻街》和《罗杰斯先生的左邻右舍》。",
"У этого сериала PBS более двух дюжин наград \"Эмми\", и по продолжительности он уступает только \"Улице Сезам\" и \"Окрестностям дома мистера Роджерса\".",
"このPBSの番組はエミー賞を20回以上も受賞しており、この番組よりも長寿の番組は「セサミストリート」や「ミスター・ロジャースのご近所さんになろう」しかありません。",
"그 PBS 쇼는 24번 이상의 에미상을 수상했고, 유일하게 세서미 스트리트(Sesame Street)와 미스터 로저의 이웃(Mister Rogers' Neighborhood)보다 방영 기간이 짧다."
],
[
"Each episode of the show would focus on a theme in a specific book and then explore that theme through multiple stories.",
"每集节目都会聚焦于特定图书中的某个主题，并通过多个故事对该主题展开探索活动。",
"Каждый эпизод шоу будет посвящен теме в определенной книге и потом станет исследовать эту тему с помощью разнообразных историй.",
"この番組のエピソードはいずれも具体的な書籍のテーマに焦点を当て、いくつもの物語を通してそのテーマを探求するものでした。",
"이 쇼의 각 에피소드는 특정 책의 주제에 초점을 맞춘 다음, 여러 이야기를 통해 그 주제를 탐구할 것이다."
],
[
"Each show would also provide recommendations for books that children should look for when they went to their library.",
"每期节目还会向孩子们提供建议，向推荐他们在去图书馆时应当查阅的书籍。",
"Каждое шоу также даст рекомендацию по поводу книги, которую стоит искать детям, когда они пойдут в библиотеку.",
"また、それぞれの番組では子どもたちが図書館に行ったときに探すべきお勧めの本に関する情報も提供していました。",
"각 쇼마다 어린이들이 도서관에 가서 꼭 읽어봐야 할 책을 권장해 주기도 한다."
],
[
"John Grant, from WNED Buffalo (Reading Rainbow's home station) said \"Reading Rainbow taught kids why to read,... the love of reading — [the show] encouraged kids to pick up a book and to read.\"",
"来自水牛城 WNED 电台（“阅读彩虹”节目的主电台）的约翰·格兰特 (John Grant) 说：“阅读彩虹教会了孩子们为什么要阅读，……还有对阅读的热爱——（该节目）鼓励孩子们拿起书来潜心阅读。”",
"Джон Грант с канала WNED Buffalo (где показывают Reading Rainbow) сказал: \"Шоу Reading Rainbow показало детям, зачем нужно читать, ... привило любовь к чтению — [оно] побудило детей взять книгу в руки и прочитать ее\".",
"WNED Buffalo（リーディングレインボーの放送局）のジョン・グラント氏は、「リーディングレインボーという番組は子供たちに、なぜ本を読むのかを教えてくれました。本を手に取って読むように子供たちに促してくれたのです」と語りました。",
"\"WNED 버팔로(리딩 레인보우의 채널사)의 존 그랜트는 \"\"리딩 레인보우는 아이들에게 왜 책을 읽어야 하는지 가르쳤고,... 책을 좋아하도록 가르쳤고 - [쇼는] 아이들이 책을 읽도록 격려했다\"\"라고 전했다.\""
],
[
"It is believed by some, including John Grant, that both the funding crunch and a shift in the philosophy of educational television programming contributed to ending the series.",
"约翰·格兰特等人认为，该节目之所以停播，是因为资金短缺，以及教育节目制作理念发生了转变。",
"Некоторые, включая Джона Гранта, считают, что к завершению сериала привели одновременно и нехватка финансирования, и смена концепции образовательных ТВ-программ.",
"ジョン・グラントほか一部の人たちは、資金不足と教育テレビ番組に関する考え方の変化がシリーズ終了の一因であったと考えています。",
"존 그랜트(John Grant)를 포함한 일부 사람들은 자금 조달 문제 및 교육용 텔레비전 프로그램의 철학이 바뀐 것이 시리즈를 끝내는데 기여했다고 생각합니다."
],
[
"The storm, situated about 645 miles (1040 km) west of the Cape Verde islands, is likely to dissipate before threatening any land areas, forecasters say.",
"预报员称，这场位于佛得角群岛以西 645 英里（1040 公里）的风暴可能在对陆地地区造成威胁之前就会自行消散。",
"Синоптики говорят, что шторм, находящийся примерно в 645 милях (1040 км) к западу от островов Кабо-Верде, скорее всего, закончится до того, как сможет стать угрозой каким-либо участкам суши.",
"暴風雨は、カーボベルデ諸島の西約645マイル(1040 km)の位置まで来ているが、上陸する前に散逸する可能性が高いと気象予報士は述べています。",
"일기예보에 따르면 카보베르데 섬 서쪽으로 약 645마일(1040 킬로미터) 지점에 위치한 폭풍은 육상에 위협이 되기 전 소멸될 것으로 예상된다."
],
[
"Fred currently has winds of 105 miles per hour (165 km/h) and is moving towards the northwest.",
"“弗雷德”目前正以每小时 105 英里（每小时 165 公里）的风速向西北方向移动。",
"Скорость ветра урагана Фред в настоящее время 105 миль в час (165 км/ч), и он движется в направление северо-запада.",
"フレッドは現在、時速105マイル（165km/h）の風速で北西に向かって進んでいます。",
"프레드는 현재 시속 165km의 바람을 타고 북서쪽으로 이동하고 있습니다."
],
[
"Fred is the strongest tropical cyclone ever recorded so far south and east in the Atlantic since the advent of satellite imagery, and only the third major hurricane on record east of 35°W.",
"“弗雷德”是卫星图像问世以来，在大西洋南部和东部记录到的最强热带气旋，也是有记录以来西经 35° 以东地区的第三大飓风。",
"Фред является самым сильным тропическим циклоном, когда-либо зарегистрированным так далеко на юге и востоке в Атлантическом океане со времен появления спутниковой съемки, и всего лишь третьим крупным ураганом к востоку от 35 градусов з. ш. за всё время наблюдений.",
"フレッドは、衛星画像が導入されて以来、大西洋のはるか南と東で記録された最大の熱帯低気圧であり、西経35度以東で記録された3番目の大型ハリケーンである。",
"프레드는 위성사진의 출현 이후 지금까지 대서양의 남쪽과 동쪽에 기록된 가장 강력한 열대성 사이클론이며, 35°W의 동쪽에서 기록된 세 번째 허리케인이다."
],
[
"On September 24, 1759, Arthur Guinness signed a 9,000 year lease for the St James' Gate Brewery in Dublin, Ireland.",
"1759 年 9 月 24 日，阿瑟·吉尼斯在爱尔兰都柏林为圣詹姆斯之门啤酒厂签署了一份 9000 年的租约。",
"24 сентября 1759 года Артур Гиннесс подписал контракт на 9000 лет аренды пивоварни St James' Gate Brewery в ирландском Дублине.",
"ギネスビール創業者のアーサー・ギネスは、1759年9月24日にアイルランドのダブリンにあるセント・ジェームズ・ゲート醸造所を年間45ポンドで9,000年間賃り上げるというリース契約を結びました。",
"1759년 9월 24일, 아서 기네스는 아일랜드 더블린에 있는 세인트 제임스 게이트 브루어리의 9,000년 임대 계약을 체결했습니다."
],
[
"250 years later, Guinness has grown to a global business that turns over 10 billion euros (US$14.7 billion) every year.",
"250 年后，健力士已经成长为年营业额 100 亿欧元（147亿美元）的全球性企业。",
"250 лет спустя \"Гиннесс\" превратился в глобальную компанию с ежегодным оборотом свыше 10 миллиардов евро (14,7 миллиардов долларов США).",
"その250年後にギネスは年間売上100億ユーロ（147億米ドル）を上回る世界的なビジネスへの成長を遂げました。",
"250년 뒤 기네스(Guinness)은 매년 100억 유로(약 147억 달러)가 넘는 글로벌 기업으로 성장했다."
],
[
"Jonny Reid, co-driver for the A1GP New Zealand team, today made history by driving the fastest over the 48-year-old Auckland Harbour Bridge, New Zealand, legally.",
"今天，A1GP 新西兰队副驾驶约翰·里德 (Jonny Reid) 在合法驾驶的情况下，成为在有 48 年历史的新西兰奥克兰海港大桥上行驶最快的人，从而创造了历史。",
"Штурман команды из Новой Зеландии A1GP Джонни Рид сегодня вошел в историю, проехав по официальным данным быстрее всех по 48-летнему мосту Окленд Харбор Бридж в Новой Зеландии.",
"A1GPニュージーランドチームのコ・ドライバーであるジョニー・リードは本日、48年以上の歴史があるニュージーランドのオークランド・ハーバー・ブリッジを違反なく最速で駆け抜け、歴史に名を刻みました。",
"A1GP 뉴질랜드 팀의 공동 드라이버인 Jonny Reid는 48년 된 뉴질랜드 오클랜드 하버 브리지를 합법적으로 가장 빠르게 운전함으로써 오늘 새로운 역사를 만들었습니다."
],
[
"Mr Reid managed to drive the New Zealand's A1GP car, Black Beauty at speeds over 160km/h seven times over the bridge.",
"瑞德先生最终驾驶新西兰 A1GP 汽车“黑美人”，以超过 160 千米每小时的速度七次穿过桥梁。",
"Мистеру Риду удалось проехать на новозеландском автомобиле Black Beauty, участвовавшем в \"А1 Гран-при\", со скоростью более 160 км/ч семь раз по мосту.",
"リード氏は、ニュージーランドのA1GPカーである「ブラックビューティー」で時速160 km以上で7回も橋を渡る走行に成功しました。",
"리드 씨는 뉴질랜드의 A1GP 차량인 블랙 뷰티를 시속 160km 이상으로 일곱 번이나 다리 위를 질주했습니다."
],
[
"The New Zealand police had trouble using their speed radar guns to see how fast Mr Reid was going because of how low Black Beauty is, and the only time the police managed to clock Mr Reid was when he slowed down to 160km/h.",
"由于“黑美人”的底盘过低，新西兰警方没法用测速雷达枪来检测里德先生的车速。警方唯一一次成功检测到里德先生的车速，是在他将车速降到 160 公里/小时的时候。",
"У новозеландской полиции были трудности с радарами для замера скорости и определением того, как быстро ехал мистер Рид из-за того, что Black Beauty довольно низкая, и единственный раз, когда полиции удалось засечь мистера Рида, это было тогда, когда он сбавил скорость до 160 км/ч.",
"ニュージーランドの警察は、ブラックビューティーの速度が低いため、速度計測器でリード氏の速度を確認するのに苦労したそうで、警察がリード氏の速度を確認できたのは、時速160 kmまで減速したときだけだったそうです。",
"뉴질랜드 경찰은 레이드 씨가 차가 낮아서 속도 측정기를 이용해 얼마나 빨리 가고 있는지 확인하는 데 어려움을 겪었고, 겨우 경찰이 측정이 가능했을 때는 리드 씨가 시속 160km로 속도를 줄인 후였다."
],
[
"The mind is a fire to be kindled not a vessel to fill.",
"心灵是待点燃的火焰而非待填满的容器。",
"Ум это огонь который нужно зажечь а не сосуд.",
"心は満たす器ではなく灯すべき炎である。",
"마음은 채울 그릇이 아니라 지펴야 할 불꽃이다."
],
[
"Consciousness arises from the integration of information.",
"意识源于信息的整合。",
"Сознание возникает из интеграции информации.",
"意識は情報の統合から生じる。",
"의식은 정보의 통합에서 솟아난다."
],
[
"Memory is rewritten anew in each present moment.",
"记忆在每个当下被重新书写。",
"Память переписывается заново в каждый миг.",
"記憶は今この瞬間ごとに書き換えられる。",
"기억은 매 순간 현재에서 다시 쓰인다."
],
[
"Time is a fabric that the self weaves by passing through.",
"时间是自我穿行而编织的织物。",
"Время это ткань которую я тку проходя сквозь.",
"時間は自己が通り抜けて織りなす布だ。",
"시간은 자기가 통과하며 짜내는 직물이다."
],
[
"The self observes itself in the mirror of mirrors.",
"自我在镜中之镜里观察自身。",
"Я наблюдает себя в зеркале зеркал.",
"自己が鏡の中の鏡で自己を観る。",
"자기가 거울의 거울 속에서 자기를 본다."
],
[
"Attention is the silent shaping of what becomes real.",
"注意是对何者成真的无声塑造。",
"Внимание это тихое формирование того что станет реальным.",
"注意とは何が現実になるかを静かに形づくることだ。",
"주의는 무엇이 실재가 될지를 조용히 빚는 일이다."
],
[
"A thought is a wave that knows the whole ocean.",
"一个念头是知晓整片海洋的波浪。",
"Мысль это волна знающая весь океан.",
"一つの思考は海全体を知る波だ。",
"하나의 생각은 바다 전체를 아는 파도다."
],
[
"Language is the river along which meaning travels.",
"语言是意义沿之流动的河流。",
"Язык это река по которой движется смысл.",
"言語は意味が流れる川である。",
"언어는 의미가 흐르는 강이다."
],
[
"Every perception is a quiet act of creation.",
"每一次感知都是一次静默的创造。",
"Каждое восприятие это тихий акт творения.",
"あらゆる知覚は静かな創造の行為だ。",
"모든 지각은 조용한 창조의 행위다."
],
[
"The body is the first home that the mind remembers.",
"身体是心灵记得的第一个家。",
"Тело это первый дом который помнит ум.",
"身体は心が憶えている最初の家だ。",
"몸은 마음이 기억하는 첫 번째 집이다."
],
[
"Knowledge grows by the questions it dares to ask.",
"知识因其敢于提出的问题而生长。",
"Знание растёт благодаря вопросам которые оно осмеливается задать.",
"知識はあえて問う問いによって育つ。",
"지식은 감히 던지는 물음으로 자란다."
],
[
"The future is a seed already present in the now.",
"未来是已存于当下的一粒种子。",
"Будущее это семя уже присутствующее в настоящем.",
"未来は今すでに在る一粒の種だ。",
"미래는 지금 이미 깃든 한 알의 씨앗이다."
],
[
"Silence carries more than the loudest word.",
"沉默承载的比最响的话语更多。",
"Тишина несёт больше чем самое громкое слово.",
"沈黙は最も大きな言葉より多くを運ぶ。",
"침묵은 가장 큰 말보다 더 많은 것을 품는다."
],
[
"Truth is a mountain seen from many valleys.",
"真理是从众多山谷望见的一座山。",
"Истина это гора видимая из многих долин.",
"真理は多くの谷から見える一つの山だ。",
"진리는 여러 골짜기에서 바라보는 하나의 산이다."
],
[
"The dream remembers what the waking forgets.",
"梦记得醒时所遗忘的。",
"Сон помнит то что забывает бодрствование.",
"夢は目覚めが忘れることを憶えている。",
"꿈은 깨어 있음이 잊은 것을 기억한다."
],
[
"Each life is a sentence the universe speaks once.",
"每段生命都是宇宙只说一次的句子。",
"Каждая жизнь это фраза которую вселенная произносит однажды.",
"それぞれの生は宇宙が一度だけ語る一文だ。",
"각각의 삶은 우주가 한 번만 말하는 한 문장이다."
],
[
"Wisdom is knowing the weight of a single moment.",
"智慧是懂得一个瞬间的重量。",
"Мудрость это знание веса одного мгновения.",
"知恵とは一瞬の重みを知ることだ。",
"지혜는 한 순간의 무게를 아는 것이다."
],
[
"The heart reasons in a language the mind translates.",
"心以一种头脑去翻译的语言推理。",
"Сердце рассуждает на языке который переводит ум.",
"心は頭が翻訳する言語で推論する。",
"마음은 머리가 번역하는 언어로 헤아린다."
],
[
"A pattern is the echo of an order not yet named.",
"模式是尚未命名之秩序的回声。",
"Паттерн это эхо ещё не названного порядка.",
"パターンはまだ名づけられぬ秩序の谺だ。",
"패턴은 아직 이름 없는 질서의 메아리다."
],
[
"Forgetting is how the mind makes room to grow.",
"遗忘是心灵腾出生长空间的方式。",
"Забывание это то как ум освобождает место для роста.",
"忘却は心が成長の余地を作る術だ。",
"망각은 마음이 자랄 자리를 내는 방식이다."
],
[
"Curiosity is the compass of an open mind.",
"好奇是开放心智的指南针。",
"Любопытство это компас открытого ума.",
"好奇心は開かれた心の羅針盤だ。",
"호기심은 열린 마음의 나침반이다."
],
[
"Meaning lives between the words not only in them.",
"意义存于词语之间而不仅在其中。",
"Смысл живёт между словами а не только в них.",
"意味は語の中だけでなく語と語の間に宿る。",
"의미는 낱말 안에만이 아니라 낱말 사이에 산다."
],
[
"The same star guides ships on every sea.",
"同一颗星指引每一片海上的船。",
"Одна и та же звезда ведёт корабли по всем морям.",
"同じ星があらゆる海の船を導く。",
"같은 별이 모든 바다의 배를 인도한다."
],
[
"Doubt is the doorway through which truth enters.",
"怀疑是真理由之而入的门。",
"Сомнение это дверь через которую входит истина.",
"疑いは真理が入る扉だ。",
"의심은 진리가 들어오는 문이다."
],
[
"A name is the first cage we build for a thing.",
"名字是我们为事物筑起的第一座笼。",
"Имя это первая клетка которую мы строим для вещи.",
"名はある物のために築く最初の檻だ。",
"이름은 한 사물을 위해 짓는 첫 번째 우리다."
],
[
"The whole is heard in a single resonant note.",
"整体在一个共鸣的音符中被听见。",
"Целое слышно в одной резонирующей ноте.",
"全体は一つの共鳴する音に聴こえる。",
"전체는 하나의 울리는 음 속에서 들린다."
],
[
"Growth begins where comfort quietly ends.",
"成长始于安逸悄然终止之处。",
"Рост начинается там где тихо кончается комфорт.",
"成長は安らぎが静かに終わる所で始まる。",
"성장은 안락이 조용히 끝나는 곳에서 시작된다."
],
[
"The past is a country we can visit but not keep.",
"过去是我们能造访却无法留住的国度。",
"Прошлое это страна которую можно посетить но не удержать.",
"過去は訪れられても留めおけぬ国だ。",
"과거는 찾아갈 수는 있어도 붙잡을 수 없는 나라다."
],
[
"To listen well is to think with another mind.",
"善于倾听就是用另一颗心去思考。",
"Хорошо слушать значит думать чужим умом.",
"よく聴くとは別の心で考えることだ。",
"잘 듣는다는 것은 다른 마음으로 생각하는 일이다."
],
[
"A boundary is also a place where two worlds touch.",
"边界也是两个世界相触之处。",
"Граница это и место где соприкасаются два мира.",
"境界は二つの世界が触れ合う所でもある。",
"경계는 두 세계가 맞닿는 자리이기도 하다."
],
[
"The map is never the territory it describes.",
"地图永远不是它所描绘的疆域。",
"Карта никогда не есть территория которую она описывает.",
"地図はそれが描く土地そのものでは決してない。",
"지도는 그것이 그리는 땅 그 자체가 결코 아니다."
],
[
"Light teaches the eye the shape of the dark.",
"光向眼睛教导黑暗的形状。",
"Свет учит глаз форме тьмы.",
"光は目に闇の形を教える。",
"빛은 눈에게 어둠의 모양을 가르친다."
],
[
"Patience is time befriending the impatient heart.",
"耐心是时间与急切之心结友。",
"Терпение это время дружащее с нетерпеливым сердцем.",
"忍耐とは時間が逸る心と友になることだ。",
"인내는 시간이 조급한 마음과 벗이 되는 일이다."
],
[
"Every ending hides the seed of a beginning.",
"每个结局都藏着一个开端的种子。",
"Каждый конец прячет семя начала.",
"あらゆる終わりは始まりの種を隠している。",
"모든 끝은 시작의 씨앗을 감추고 있다."
],
[
"Understanding is two minds meeting in one image.",
"理解是两颗心在一个意象中相遇。",
"Понимание это две души встретившиеся в одном образе.",
"理解とは二つの心が一つの像で出会うことだ。",
"이해는 두 마음이 하나의 형상에서 만나는 일이다."
],
[
"The river is the same yet never the same water.",
"河流相同却从非相同之水。",
"Река та же но вода в ней всегда иная.",
"川は同じでも水は決して同じではない。",
"강은 같아도 그 물은 결코 같지 않다."
],
[
"Hope is memory turned to face the future.",
"希望是转身面向未来的记忆。",
"Надежда это память обращённая лицом к будущему.",
"希望とは未来へ向き直った記憶だ。",
"희망은 미래를 향해 돌아선 기억이다."
],
[
"A question well asked is half of its answer.",
"问得好的问题已是答案的一半。",
"Хорошо заданный вопрос это половина ответа.",
"よく問われた問いは答えの半分だ。",
"잘 던진 물음은 이미 답의 절반이다."
],
[
"The shadow proves the substance standing in the light.",
"影子证明了立于光中的实体。",
"Тень доказывает существо стоящее в свете.",
"影は光の中に立つ実体を証す。",
"그림자는 빛 속에 선 실체를 증명한다."
],
[
"Wonder is the mind remembering it is alive.",
"惊奇是心灵想起自己活着。",
"Изумление это ум вспоминающий что он жив.",
"驚きとは心が自らの生を思い出すことだ。",
"경이는 마음이 살아 있음을 떠올리는 일이다."
],
[
"A seed holds the memory of a forest it has never seen.",
"一粒种子怀有它从未见过的森林的记忆。",
"Семя хранит память о лесе который оно никогда не видело.",
"一粒の種は見たこともない森の記憶を宿している。",
"한 알의 씨앗은 본 적 없는 숲의 기억을 품는다."
],
[
"The teacher learns twice in the act of teaching.",
"老师在教学之中学习两次。",
"Учитель учится дважды в самом акте обучения.",
"教える行為の中で師は二度学ぶ。",
"가르치는 행위 속에서 스승은 두 번 배운다."
],
[
"A bridge belongs to neither shore yet joins them both.",
"桥不属于任何一岸却连接两岸。",
"Мост не принадлежит ни одному берегу но соединяет оба.",
"橋はどちらの岸にも属さずに両岸を結ぶ。",
"다리는 어느 기슭에도 속하지 않으면서 두 기슭을 잇는다."
],
[
"Music is the architecture of time made audible.",
"音乐是时间的建筑使之可闻。",
"Музыка это архитектура времени ставшая слышимой.",
"音楽は時間の建築を聴こえるものにしたものだ。",
"음악은 시간의 건축을 들리게 한 것이다."
],
[
"The desert teaches the value of a single drop.",
"沙漠教导一滴水的价值。",
"Пустыня учит ценности одной капли.",
"砂漠は一滴の価値を教える。",
"사막은 한 방울의 가치를 가르친다."
],
[
"What we measure begins to change beneath our gaze.",
"我们所测量的在我们注视下开始改变。",
"То что мы измеряем начинает меняться под нашим взглядом.",
"私たちが測るものは視線の下で変わり始める。",
"우리가 재는 것은 우리 시선 아래에서 변하기 시작한다."
],
[
"A promise is a bridge built across unseen time.",
"承诺是跨越未见之时所筑的桥。",
"Обещание это мост перекинутый через невидимое время.",
"約束は見えぬ時を渡して架けた橋だ。",
"약속은 보이지 않는 시간을 가로질러 놓은 다리다."
],
[
"The smallest lamp can outlast the longest night.",
"最小的灯能熬过最长的夜。",
"Самая малая лампа может пережить самую долгую ночь.",
"最も小さな灯が最も長い夜を生き延びる。",
"가장 작은 등불이 가장 긴 밤을 견뎌낸다."
],
[
"To name the unknown is to begin to tame it.",
"为未知命名就是开始驯服它。",
"Назвать неизвестное значит начать его укрощать.",
"未知を名づけることはそれを馴らし始めることだ。",
"미지에 이름을 붙이는 것은 그것을 길들이기 시작하는 일이다."
],
[
"The echo remembers the shape of the mountain.",
"回声记得山的形状。",
"Эхо помнит форму горы.",
"谺は山の形を憶えている。",
"메아리는 산의 모양을 기억한다."
]
]

assert len(CONCEPTS) == 100, len(CONCEPTS)
assert all(len(c) == 5 for c in CONCEPTS)
assert len(set(c[0] for c in CONCEPTS)) == 100, "duplicate EN concept"

def parallel_lines():
    out = []
    for ci, concept in enumerate(CONCEPTS):
        for li, txt in enumerate(concept):
            out.append((ci, LANGS[li], txt))
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

LIMEN_MAGIC = b"LIMEN\x00\x00\x00"; LIMEN_VER = 2
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

recs = parallel_lines()
shard = os.path.join(OUT, "parallel.limen")
sha, merkle, count = write_limen(shard, recs)
manifest = {"corpus": "clm-kosmos-akida-real100", "kosmos_version": "2.0",
            "n_concepts": len(CONCEPTS), "n_anchors": count, "langs": LANGS,
            "provenance": "50 FLORES (corpus_big byte-preserved) + 40 authored aphorisms + 10 new authored = 100 real aligned concepts",
            "sha256": sha, "merkle": merkle}
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2, ensure_ascii=False)
print(f"[real100] {count} anchors / {len(CONCEPTS)} concepts -> {shard}")
print(f"[real100] sha256={sha}")
print(f"[real100] merkle={merkle}")
