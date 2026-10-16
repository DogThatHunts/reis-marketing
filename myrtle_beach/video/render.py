"""Render a New Homes Review social teaser (1080x1920, 9:16) from a script file.

usage: python render.py scripts/qa.json            # multi-voice script
       python render.py scripts/mono.json am_onyx  # single-voice script + voice (add _deep for the pitched take)
Run vo.py first. Frames are drawn with Pillow and piped to ffmpeg; VO + music are mixed by ffmpeg.
"""
import json, subprocess, sys, os, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, 'Nhr_Myb_0826_2_images', 'Nhr_Myb_0826_2.pdf-{}.png')
SCRIPT = json.load(open(sys.argv[1]))
TAKE = SCRIPT['name'] + (f'_{sys.argv[2]}' if len(sys.argv) > 2 else '')
OUT = os.path.join(HERE, f'myrtle_beach_teaser_{TAKE}.mp4')
MUSIC = os.path.join(HERE, 'music', 'Inspired.mp3')

W, H, FPS = 1080, 1920, 30
NAVY, NAVY_DK, RED, GREEN, WHITE = (27, 58, 122), (14, 32, 72), (200, 40, 45), (46, 204, 113), (255, 255, 255)
FS = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(FS + name, size)
F_HUGE, F_BIG, F_MED, F_SUB, F_CAP = (font('Arial Black.ttf', 150), font('Arial Black.ttf', 96),
    font('Arial Black.ttf', 64), font('Arial Bold.ttf', 44), font('Arial Bold.ttf', 44))

LEAD, GAP, TAIL = 0.3, SCRIPT['gap'], 1.8      # seconds: silence before VO, between segments, end card after VO

# ---------- audio timeline ----------
SEGS = SCRIPT['segments']
clips = [sf.read(os.path.join(HERE, 'vo', TAKE, f'seg{i}.wav')) for i in range(len(SEGS))]
sr = clips[0][1]
starts, t = [], LEAD
for a, _ in clips:
    starts.append(t); t += len(a) / sr + GAP
vo_end = t - GAP
TOTAL = vo_end + TAIL
vo = np.zeros(int(TOTAL * sr) + 1)
for (a, _), s in zip(clips, starts):
    i = int(s * sr); vo[i:i + len(a)] = a
vo_path = os.path.join(HERE, 'vo', TAKE, 'timeline.wav')
sf.write(vo_path, vo, sr)
END_CARD = vo_end + 0.2
seg_end = starts[1:] + [END_CARD]

# scene windows: a scene runs from its first segment until the next scene's first segment
SCN = SCRIPT['scenes']
scn_start = [0.0] + [starts[sc['segs'][0]] for sc in SCN[1:]]
scn_end = scn_start[1:] + [END_CARD]
def at(seg, frac): return starts[seg] + frac * (seg_end[seg] - starts[seg])

# ---------- helpers ----------
def ease(x): x = max(0., min(1., x)); return 1 - (1 - x) ** 3
def lerp(a, b, x): return a + (b - a) * x

def text_img(s, f, fill):
    l, t, r, b = f.getbbox(s)
    im = Image.new('RGBA', (r - l + 4, b - t + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2 - l, 2 - t), s, font=f, fill=fill)
    return im

def fit_font(s, name, size, maxw):
    while size > 20 and font(name, size).getlength(s) > maxw: size -= 4
    return font(name, size)

def with_alpha(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a))); return im

def place(frame, im, cx, y, a=1.0, rise=40):
    """paste im centered on cx at top y, fading/rising in with progress a (0..1)."""
    if a <= 0: return
    e = ease(a)
    frame.alpha_composite(with_alpha(im, e), (int(cx - im.width / 2), int(y + (1 - e) * rise)))

def arrow(up, color, size=70):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, size), (size, size), (size / 2, 0)] if up else [(0, 0), (size, 0), (size / 2, size)], fill=color)
    return im

def stat_line(up, color, s, f):
    a, tx = arrow(up, color, int(f.size * .7)), text_img(s, f, color)
    im = Image.new('RGBA', (a.width + 24 + tx.width, max(a.height, tx.height)), (0, 0, 0, 0))
    im.alpha_composite(a, (0, (im.height - a.height) // 2)); im.alpha_composite(tx, (a.width + 24, (im.height - tx.height) // 2))
    return im

def load(key): return Image.open(IMG.format(key)).convert('RGB')
MEDIA = {k: load(v) for k, v in dict(heat='0006-04', monthly='0015-04', pie='0038-04',
                                    builders='0039-05', subs='0043-04').items()}
PAGES = [Image.open(os.path.join(HERE, 'assets', f'page-{n}.png')).convert('RGB') for n in ('001', '051', '043')]
LOGO = Image.open(os.path.join(HERE, 'assets', 'p1-001.png')).convert('RGB')

CARD_Y, CARD_W, CARD_H = 700, 980, 700
def media_card(src, x, zoom0, zoom1, focus, alpha=1.0):
    """white card with a Ken Burns crop of src; focus=(fx,fy) in 0..1 is the zoom target."""
    z = lerp(zoom0, zoom1, x)
    iw, ih = src.size
    aspect = (CARD_W - 40) / (CARD_H - 40)
    cw = iw / z; ch = cw / aspect
    if ch > ih: ch = ih; cw = ch * aspect
    fx, fy = focus
    cx = min(max(fx * iw, cw / 2), iw - cw / 2)
    cy = min(max(fy * ih, ch / 2), ih - ch / 2)
    if cw > iw:   # source narrower than card: letterbox
        crop = src
        card_img = Image.new('RGB', (CARD_W - 40, CARD_H - 40), WHITE)
        s = min((CARD_W - 40) / iw, (CARD_H - 40) / ih) * z
        r = crop.resize((int(iw * s), int(ih * s)), Image.BILINEAR)
        card_img.paste(r, ((card_img.width - r.width) // 2, (card_img.height - r.height) // 2))
    else:
        card_img = src.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize(
            (CARD_W - 40, CARD_H - 40), Image.BILINEAR)
    card = Image.new('RGBA', (CARD_W, CARD_H), WHITE + (255,))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, CARD_W - 1, CARD_H - 1), 28, fill=WHITE)
    card.paste(card_img, (20, 20))
    mask = Image.new('L', card.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, CARD_W - 1, CARD_H - 1), 28, fill=255)
    card.putalpha(mask)
    return with_alpha(card, alpha)

def background():
    g = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(NAVY) * (1 - g) + np.array(NAVY_DK) * g).astype(np.uint8)
    return Image.fromarray(np.repeat(arr, W, axis=1), 'RGB').convert('RGBA')
BG = background()

def header(frame):
    lg = LOGO.resize((LOGO.width * 2, LOGO.height * 2), Image.LANCZOS)
    pill = Image.new('RGBA', (lg.width + 60, lg.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle((0, 0, pill.width - 1, pill.height - 1), 24, fill=WHITE)
    pill.paste(lg, (30, 15))
    frame.alpha_composite(pill, ((W - pill.width) // 2, 110))
    sub = text_img("MYRTLE BEACH & BRUNSWICK COUNTY", font('Arial Bold.ttf', 34), (200, 215, 240))
    frame.alpha_composite(sub, ((W - sub.width) // 2, 110 + pill.height + 22))
HEADER = BG.copy(); header(HEADER)

def wrap(s, f, maxw):
    out, cur = [], ''
    for w in s.split():
        nxt = (cur + ' ' + w).strip()
        if f.getlength(nxt) <= maxw: cur = nxt
        else: out.append(cur); cur = w
    return out + [cur]

def caption(frame, t):
    """burned-in caption for the segment being spoken; chunks are timed evenly across it.
    questions ("q") sit on a red box, answers on black."""
    if t < starts[0]: return
    idx = max(i for i, s in enumerate(starts) if t >= s)
    chunks = SEGS[idx]['caption']
    lt = (t - starts[idx]) / (seg_end[idx] - starts[idx])
    cum = np.cumsum([len(c) for c in chunks]) / sum(len(c) for c in chunks)   # time chunks by text length
    chunk = wrap(chunks[min(int(np.searchsorted(cum, lt, side='right')), len(chunks) - 1)], F_CAP, 1000)
    fill = RED + (235,) if SEGS[idx]['style'] == 'q' else (0, 0, 0, 170)
    y = 1450
    for r in chunk:
        tx = text_img(r, F_CAP, WHITE)
        box = Image.new('RGBA', (tx.width + 36, tx.height + 22), fill)
        box.alpha_composite(tx, (18, 11))
        frame.alpha_composite(box, ((W - box.width) // 2, y)); y += box.height + 8

# ---------- scenes: (frame, progress 0..1, seconds into scene, split point 0..1, seconds until answer) ----------
def s_intro(fr, x, ts, sp, a0):
    place(fr, text_img("MYRTLE BEACH", F_BIG, WHITE), W / 2, 400, ts / .3)
    place(fr, text_img("& BRUNSWICK COUNTY · JAN–AUG '26", F_SUB, (200, 215, 240)), W / 2, 540, ts / .4)
    place(fr, media_card(PAGES[0], x, 1.0, 1.25, (.5, .45)), W / 2, CARD_Y, ts / .5)

def s_hook(fr, x, ts, sp, a0):
    if ts < a0:   # question being asked
        place(fr, text_img("HOW'S THE", F_BIG, WHITE), W / 2, 700, ts / .25)
        place(fr, text_img("MARKET?", F_HUGE, WHITE), W / 2, 830, ts / .35)
        return
    place(fr, text_img("U.S. NEW HOME SALES", F_SUB, (200, 215, 240)), W / 2, 520, (ts - a0) / .3)
    place(fr, stat_line(False, (255, 90, 90), "2.0%", F_HUGE), W / 2, 590, (ts - a0) / .4)
    k = (x - sp) / .08
    place(fr, text_img("MYRTLE BEACH & BRUNSWICK CO.", F_SUB, (200, 215, 240)), W / 2, 900, k)
    place(fr, stat_line(True, GREEN, "3.0%", F_HUGE), W / 2, 970, k)
    place(fr, text_img("AUG '26 vs AUG '25", F_SUB, WHITE), W / 2, 1230, k - .5)

def s_volume(fr, x, ts, sp, a0):
    if x < sp:
        n = int(5812 * ease((ts - a0) / 1.2))
        place(fr, text_img(f"{n:,}", F_HUGE, WHITE), W / 2, 380, (ts - a0) / .25)
        place(fr, text_img("NEW HOME CLOSINGS · JAN–AUG '26", F_SUB, (200, 215, 240)), W / 2, 580, ts / .35)
        place(fr, media_card(MEDIA['heat'], x / sp, 1.0, 1.35, (.45, .4)), W / 2, CARD_Y, ts / .4)
    else:
        lt = (x - sp) / (1 - sp)
        place(fr, text_img("$374,680", F_HUGE, WHITE), W / 2, 380, lt / .15)
        place(fr, stat_line(True, GREEN, "1.2%  AVG PRICE · TRAILING 12 MO", F_SUB), W / 2, 580, lt / .2)
        place(fr, media_card(MEDIA['monthly'], lt, 1.0, 1.15, (.45, .45)), W / 2, CARD_Y, lt / .2)

def s_builders(fr, x, ts, sp, a0):
    if x < sp:
        lt = x / sp
        place(fr, text_img("#1 D.R. HORTON", fit_font("#1 D.R. HORTON", 'Arial Black.ttf', 120, 980), WHITE), W / 2, 390, ts / .25)
        place(fr, text_img("28% MARKET SHARE · 1,614 CLOSINGS", F_SUB, (200, 215, 240)), W / 2, 580, ts / .35)
        place(fr, media_card(MEDIA['pie'], lt, 1.0, 1.5, (.6, .35)), W / 2, CARD_Y, ts / .4)
    else:
        lt = (x - sp) / (1 - sp)
        place(fr, text_img("LOGAN HOMES", fit_font("LOGAN HOMES", 'Arial Black.ttf', 120, 980), WHITE), W / 2, 390, lt / .15)
        place(fr, stat_line(True, GREEN, "55% CLOSINGS · 155 → 241", F_SUB), W / 2, 580, lt / .2)
        place(fr, media_card(MEDIA['builders'], lt, 1.0, 1.9, (.55, .6)), W / 2, CARD_Y, lt / .2)

def s_community(fr, x, ts, sp, a0):
    place(fr, text_img("AUBERON WOODS", fit_font("AUBERON WOODS", 'Arial Black.ttf', 120, 980), WHITE), W / 2, 390, ts / .25)
    place(fr, text_img("#1 COMMUNITY · 157 CLOSINGS", F_SUB, (200, 215, 240)), W / 2, 580, ts / .35)
    place(fr, media_card(MEDIA['subs'], x, 1.0, 1.3, (.4, 0)), W / 2, CARD_Y, ts / .4)

def s_report(fr, x, ts, sp, a0):
    place(fr, text_img("112 PAGES", F_HUGE, WHITE), W / 2, 360, ts / .25)
    if not (a0 and ts >= a0):
        place(fr, text_img("RANKINGS · PRICING · MARKET AREAS", F_SUB, (200, 215, 240)), W / 2, 570, ts / .35)
    else:   # answer: show where to get it
        url = text_img("reis-myrtlebeach.com", font('Arial Black.ttf', 56), WHITE)
        pill = Image.new('RGBA', (url.width + 70, url.height + 44), (0, 0, 0, 0))
        ImageDraw.Draw(pill).rounded_rectangle((0, 0, pill.width - 1, pill.height - 1), pill.height // 2, fill=RED)
        pill.alpha_composite(url, (35, 22))
        place(fr, pill, W / 2, 548, (ts - a0) / .3)
    # fanned page stack, flipping through
    i = min(int(x * 3), 2)
    for j, k in enumerate([(i + 2) % 3, (i + 1) % 3, i]):
        p = PAGES[k].resize((560, int(560 * PAGES[k].height / PAGES[k].width)), Image.BILINEAR).convert('RGBA')
        p = p.rotate((j - 2) * -6, expand=True, resample=Image.BICUBIC)
        place(fr, p, W / 2 + (j - 2) * 30, 690 + (2 - j) * 10, ts / .3 if j == 2 else 1)

def s_end(fr, ts):
    fr.paste(WHITE + (255,), (0, 0, W, H))
    lg = LOGO.resize((LOGO.width * 3, LOGO.height * 3), Image.LANCZOS).convert('RGBA')
    place(fr, lg, W / 2, 520, ts / .3)
    place(fr, text_img("Myrtle Beach & Brunswick County", font('Arial Bold.ttf', 50), NAVY), W / 2, 790, ts / .4)
    place(fr, text_img("New Homes Review · Jan–Aug 2026", font('Arial.ttf', 40), (90, 100, 120)), W / 2, 870, ts / .5)
    url = text_img("reis-myrtlebeach.com", font('Arial Black.ttf', 64), WHITE)
    pill = Image.new('RGBA', (url.width + 90, url.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle((0, 0, pill.width - 1, pill.height - 1), pill.height // 2, fill=RED)
    pill.alpha_composite(url, (45, 30))
    place(fr, pill, W / 2, 1060, (ts - .3) / .4)
    place(fr, text_img("Get the full report", font('Arial Bold.ttf', 44), NAVY), W / 2, 1230, (ts - .5) / .4)

SCENES = dict(intro=s_intro, hook=s_hook, volume=s_volume, builders=s_builders, community=s_community, report=s_report)

def frame_at(t):
    if t >= END_CARD:
        fr = BG.copy(); s_end(fr, t - END_CARD); return fr
    i = max(j for j, s in enumerate(scn_start) if t >= s)
    sc, s0, e0 = SCN[i], scn_start[i], scn_end[i]
    sp = (at(*sc['split']) - s0) / (e0 - s0) if 'split' in sc else .5
    ans = [k for k in sc['segs'] if SEGS[k]['style'] == 'a']
    a0 = (starts[ans[0]] - s0) if ans else 0
    fr = HEADER.copy()
    SCENES[sc['scene']](fr, (t - s0) / (e0 - s0), t - s0, sp, a0)
    caption(fr, t)
    return fr

# ---------- encode ----------
silent = OUT + '.video.mp4'
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                       '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', silent],
                      stdin=subprocess.PIPE)
for n in range(int(TOTAL * FPS)):
    ff.stdin.write(frame_at(n / FPS).convert('RGB').tobytes())
ff.stdin.close(); ff.wait()

# music ducked under VO, faded in/out
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', vo_path, '-i', MUSIC, '-filter_complex',
    f"[2:a]atrim=0:{TOTAL},asetpts=N/SR/TB,volume=0.35,afade=t=in:d=0.5,afade=t=out:st={TOTAL - 1.5}:d=1.5[m];"
    f"[1:a]aresample=48000,volume=1.6,asplit[v1][v2];"
    f"[m][v1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];"
    f"[md][v2]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', OUT], check=True)
os.remove(silent)
print(f'{OUT}  {TOTAL:.2f}s')
