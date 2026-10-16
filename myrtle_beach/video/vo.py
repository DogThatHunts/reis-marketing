"""Render voiceover segments for a script with Kokoro TTS.

usage: python vo.py scripts/qa.json [--voice am_onyx] [--speed 1.1] [--deep am_onyx=0.84]
  --voice  fills segments whose "voice" is null (single-voice scripts)
  --deep   lowers pitch of a voice (keeps tempo); repeatable
Writes vo/<take>/seg<N>.wav, where take = script name (+ _voice for single-voice scripts).
Needs: pip install kokoro-onnx soundfile; brew install espeak-ng; model files in KOKORO_DIR.
"""
import argparse, json, os, subprocess, soundfile as sf
from kokoro_onnx import Kokoro
from kokoro_onnx.config import EspeakConfig

HERE = os.path.dirname(os.path.abspath(__file__))
KDIR = os.environ.get('KOKORO_DIR', os.path.join(HERE, 'kokoro'))
ESPEAK = '/opt/homebrew/opt/espeak-ng/'

ap = argparse.ArgumentParser()
ap.add_argument('script'); ap.add_argument('--voice'); ap.add_argument('--speed', type=float, default=1.1)
ap.add_argument('--deep', action='append', default=[])
args = ap.parse_args()
script = json.load(open(args.script))
deep = dict(d.split('=') for d in args.deep)
take = script['name'] + (f'_{args.voice}' if args.voice else '') + ('_deep' if args.voice in deep else '')
out = os.path.join(HERE, 'vo', take); os.makedirs(out, exist_ok=True)

k = Kokoro(os.path.join(KDIR, 'kokoro-v1.0.onnx'), os.path.join(KDIR, 'voices-v1.0.bin'),
           espeak_config=EspeakConfig(ESPEAK + 'lib/libespeak-ng.dylib', ESPEAK + 'share/espeak-ng-data'))
durs = []
for i, seg in enumerate(script['segments']):
    v = seg['voice'] or args.voice
    a, sr = k.create(seg['text'], voice=v, speed=seg.get('speed', args.speed), lang='en-us')
    f = os.path.join(out, f'seg{i}.wav'); sf.write(f, a, sr)
    if v in deep:
        r = float(deep[v])
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f, '-af',
                        f'asetrate={sr}*{r},aresample={sr},atempo={1 / r}', f + '.tmp.wav'], check=True)
        os.replace(f + '.tmp.wav', f); a, _ = sf.read(f)
    durs.append(round(len(a) / sr, 2))
print(take, durs, 'speech', round(sum(durs), 2), 'with gaps', round(sum(durs) + script['gap'] * (len(durs) - 1), 2))
