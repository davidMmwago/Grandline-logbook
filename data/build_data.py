"""Builds data/one-piece.json from the raw source files in data/raw/.

Sources:
  raw_wc.txt   - One Piece Wiki, Template:WC (chapter -> episodes, with page ranges)
  raw_imdb.txt - IMDb episode ratings (all eps) + titles for eps rated >= 8.5
  raw_chdates.txt - One Piece Wiki, Template:WhichMangaDate (chapter release dates, stored as day gaps)
  raw_epdates.txt - One Piece Wiki, Template:WhichAnimeDate (episode air dates, stored as day gaps)
"""
import json, re, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = lambda f: os.path.join(HERE, "raw", f)
PULLED = datetime.date(2026, 11, 2)

def pages(spec):
    n = 0
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-'); n += int(b) - int(a) + 1
        elif part:
            n += 1
    return n

# ---------- chapter -> episodes ----------
ch2ep = {}
for line in open(RAW('raw_wc.txt')):
    line = line.strip()
    if not line: continue
    ch, rest = line.split(':', 1)
    eps = []
    for m in re.finditer(r'(\d+)\(([^)]*)\)', rest):
        ep, spec = int(m.group(1)), m.group(2)
        if spec == '1':        # title/cover page reused in a recap or eyecatch; not a real adaptation
            continue
        eps.append([ep, spec, pages(spec)])
    ch2ep[int(ch)] = eps

LAST_ADAPTED = max(ch2ep)

# ---------- chapter release dates ----------
hdr, gaps = open(RAW('raw_chdates.txt')).read().strip().split('\n')
d0 = datetime.date.fromisoformat(hdr.split()[0].split('=')[1])
gaps = [int(x) for x in gaps.split(',')]
dates = [d0]
for g in gaps: dates.append(dates[-1] + datetime.timedelta(days=g))
released = [d for d in dates if d <= PULLED]          # drop scheduled-but-unreleased chapters
LAST_CH = len(released)
ch_gaps = gaps[:LAST_CH - 1]

# ---------- episode air dates (One Piece Wiki, Template:WhichAnimeDate) ----------
ehdr, egaps = open(RAW('raw_epdates.txt')).read().strip().split('\n')
e0 = datetime.date.fromisoformat(ehdr.split()[0].split('=')[1])
ep_gaps = [int(x) for x in egaps.split(',')]

# invert: episode -> chapters (with page count, to find the 'main' chapter)
ep2ch = {}
for ch, eps in ch2ep.items():
    for ep, spec, n in eps:
        ep2ch.setdefault(ep, []).append([ch, spec, n])

# ---------- IMDb ----------
lines = open(RAW('raw_imdb.txt')).read().strip().split('\n')
ratings = [float(x) for x in lines[0][2:].split(',')]
LAST_EP = len(ratings)
titles = {}
for l in lines[1:]:
    ep, r, votes, title = l.split('|', 3)
    titles[int(ep)] = {'r': float(r), 'v': votes, 't': title}

# ---------- arcs (One Piece Wiki, Story Arcs page) ----------
canon = [
 # id, name, saga, chStart, chEnd, location
 ('romance-dawn','Romance Dawn','East Blue',1,7,'dawn'),
 ('orange-town','Orange Town','East Blue',8,21,'orange'),
 ('syrup-village','Syrup Village','East Blue',22,41,'syrup'),
 ('baratie','Baratie','East Blue',42,68,'baratie'),
 ('arlong-park','Arlong Park','East Blue',69,95,'cocoyasi'),
 ('loguetown','Loguetown','East Blue',96,100,'logue'),
 ('reverse-mountain','Reverse Mountain','Arabasta',101,105,'reverse'),
 ('whisky-peak','Whisky Peak','Arabasta',106,114,'whisky'),
 ('little-garden','Little Garden','Arabasta',115,129,'littlegarden'),
 ('drum-island','Drum Island','Arabasta',130,154,'drum'),
 ('arabasta','Arabasta','Arabasta',155,217,'arabasta'),
 ('jaya','Jaya','Sky Island',218,236,'jaya'),
 ('skypiea','Skypiea','Sky Island',237,302,'skypiea'),
 ('long-ring','Long Ring Long Land','Water 7',303,321,'lrll'),
 ('water-7','Water 7','Water 7',322,374,'water7'),
 ('enies-lobby','Enies Lobby','Water 7',375,430,'enies'),
 ('post-enies','Post-Enies Lobby','Water 7',431,441,'water7'),
 ('thriller-bark','Thriller Bark','Thriller Bark',442,489,'thriller'),
 ('sabaody','Sabaody Archipelago','Summit War',490,513,'sabaody'),
 ('amazon-lily','Amazon Lily','Summit War',514,524,'amazon'),
 ('impel-down','Impel Down','Summit War',525,549,'impel'),
 ('marineford','Marineford','Summit War',550,580,'marineford'),
 ('post-war','Post-War','Summit War',581,597,'amazon'),
 ('return-sabaody','Return to Sabaody','Fish-Man Island',598,602,'sabaody'),
 ('fishman-island','Fish-Man Island','Fish-Man Island',603,653,'fishman'),
 ('punk-hazard','Punk Hazard','Dressrosa',654,699,'punk'),
 ('dressrosa','Dressrosa','Dressrosa',700,801,'dressrosa'),
 ('zou','Zou','Whole Cake Island',802,824,'zou'),
 ('whole-cake','Whole Cake Island','Whole Cake Island',825,902,'wci'),
 ('levely','Levely','Whole Cake Island',903,908,'levely'),
 ('wano','Wano Country','Wano Country',909,1057,'wano'),
 ('egghead','Egghead','Final',1058,1125,'egghead'),
 ('elbaph','Elbaph','Final',1126,LAST_CH,'elbaph'),
]
filler = [
 ('warship-island','Warship Island',54,61,'f-warship'),
 ('post-arabasta','Post-Arabasta',131,135,'f-postarabasta'),
 ('goat-island','Goat Island',136,138,'f-goat'),
 ('ruluka','Ruluka Island',139,143,'f-ruluka'),
 ('g8','G-8',196,206,'f-g8'),
 ('oceans-dream',"Ocean's Dream",220,224,'f-dream'),
 ('foxy-return',"Foxy's Return",225,228,'f-foxy'),
 ('ice-hunter','Ice Hunter',326,335,'f-ice'),
 ('spa-island','Spa Island',382,384,'f-spa'),
 ('little-east-blue','Little East Blue',426,429,'f-leb'),
 ('z-ambition',"Z's Ambition",575,578,'f-z'),
 ('caesar-retrieval','Caesar Retrieval',626,628,'f-caesar'),
 ('silver-mine','Silver Mine',747,750,'f-silver'),
 ('marine-rookie','Marine Rookie',780,782,'f-rookie'),
 ('cidre-guild','Cidre Guild',895,896,'f-cidre'),
 ('uta-past',"Uta's Past",1029,1030,'f-uta'),
]

EP_RANGES = {'romance-dawn': (1, 4), 'orange-town': (4, 8), 'syrup-village': (9, 18), 'baratie': (19, 30), 'arlong-park': (31, 44), 'loguetown': (45, 53), 'reverse-mountain': (62, 63), 'whisky-peak': (64, 67), 'little-garden': (70, 77), 'drum-island': (78, 91), 'arabasta': (92, 130), 'jaya': (144, 152), 'skypiea': (153, 195), 'long-ring': (207, 219), 'water-7': (229, 263), 'enies-lobby': (264, 312), 'post-enies': (313, 325), 'thriller-bark': (337, 381), 'sabaody': (385, 405), 'amazon-lily': (408, 421), 'impel-down': (422, 452), 'marineford': (457, 489), 'post-war': (490, 516), 'return-sabaody': (517, 522), 'fishman-island': (523, 574), 'punk-hazard': (579, 625), 'dressrosa': (629, 746), 'zou': (751, 779), 'whole-cake': (783, 877), 'levely': (878, 889), 'wano': (890, 1085), 'egghead': (1086, 1155), 'elbaph': (1156, None)}  # One Piece Wiki, Story Arcs page

def arc_of_ch(c):
    for a in canon:
        if a[3] <= c <= a[4]: return a[0]
    return None

# episode -> primary chapter (most pages) -> arc
ep_main = {}
for ep, lst in ep2ch.items():
    if ep > LAST_EP: continue
    best = max(lst, key=lambda x: x[2])
    ep_main[ep] = best[0]

filler_ep = {}
for fid, name, a, b, loc in filler:
    for e in range(a, b + 1): filler_ep[e] = fid

arcs = []
for aid, name, saga, cs, ce, loc in canon:
    a, b = EP_RANGES[aid]; b = b or LAST_EP
    eps = [e for e in range(a, b + 1) if e not in filler_ep]
    arcs.append({'id': aid, 'name': name, 'saga': saga, 'type': 'canon', 'loc': loc,
                 'ch': [cs, ce], 'ep': [a, b], 'epCount': len(eps)})
for fid, name, a, b, loc in filler:
    arcs.append({'id': fid, 'name': name, 'saga': None, 'type': 'filler', 'loc': loc,
                 'ch': None, 'ep': [a, b], 'epCount': b - a + 1})

# per-episode type: c = canon (adapts manga), f = filler arc, x = other anime-only/recap
ep_type = []
for e in range(1, LAST_EP + 1):
    if e in filler_ep: ep_type.append('f')
    elif e in ep_main: ep_type.append('c')
    else: ep_type.append('x')

# compact chapter->episode list (only real adaptations), as [[ep, pages], ...]
c2e = {c: [[ep, spec] for ep, spec, n in eps if ep <= LAST_EP] for c, eps in ch2ep.items()}

out = {
  'meta': {'lastChapter': LAST_CH, 'lastAdapted': LAST_ADAPTED, 'lastEpisode': LAST_EP,
           'sources': {'mapping': 'One Piece Wiki (Template:WC), CC BY-SA', 'ratings': 'IMDb user ratings'},
           'pulled': PULLED.isoformat()},
  'chDates': {'first': d0.isoformat(), 'gaps': ch_gaps},
  'epDates': {'first': e0.isoformat(), 'gaps': ep_gaps[:LAST_EP - 1]},
  'arcs': arcs,
  'c2e': c2e,
  'epType': ''.join(ep_type),
  'ratings': ratings,
  'titles': titles,
}
json.dump(out, open(os.path.join(HERE, 'one-piece.json'), 'w'), separators=(',', ':'))

# ---------- checks ----------
print('chapters', LAST_CH, 'released (last', released[-1], ') adapted up to', LAST_ADAPTED, '| episodes', LAST_EP, '| titles', len(titles))
print('>=9.0', sum(r >= 9 for r in ratings), '>=8.5', sum(r >= 8.5 for r in ratings))
print('ep types', {t: ep_type.count(t) for t in 'cfx'})
other = [i + 1 for i, t in enumerate(ep_type) if t == 'x']
print('anime-only/recap (not in a named filler arc):', other)
for a in arcs:
    print(f"{a['type']:6} {a['name']:22} ch {a['ch']}  ep {a['ep']}  ({a['epCount']})")
print('size', len(json.dumps(out, separators=(',', ':'))))
