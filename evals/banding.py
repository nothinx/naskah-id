#!/usr/bin/env python3
"""Bandingkan mutu tulisan dua folder jawaban secara berpasangan dan buta.

    python evals/banding.py evals/hasil/dengan-skill evals/hasil/tanpa-skill --penilai "claude -p"
    python evals/banding.py A B                      # hanya ukuran objektif periksa.py
    python evals/banding.py --tes

Untuk tiap kasus yang jawabannya ada di kedua folder, penilai melihat jawaban 1 dan 2 dengan
urutan acak (tetap per kasus) dan memilih yang lebih baik pada empat aspek. Ukuran objektif:
temuan periksa.py per 100 kata pada teks hasil (sebelum catatan perubahan), tanpa SG-04 yang
berisik. Folder pertama disebut A, folder kedua B.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR / "scripts"))
sys.path.insert(0, str(AKAR / "evals"))
from periksa import periksa  # noqa: E402
from jalankan import jalankan, teks_hasil  # noqa: E402

ASPEK = ["kebakuan", "kealamian", "keringkasan", "kesetiaan"]

PROMPT_BANDING = """Kamu penyunting senior naskah ilmiah berbahasa Indonesia. Bandingkan dua jawaban
untuk permintaan yang sama. Nilai tulisannya, bukan panjang penjelasannya.

PERMINTAAN PENGGUNA:
{prompt}

JAWABAN 1:
{j1}

JAWABAN 2:
{j2}

Aspek:
- kebakuan: ejaan EYD V, kata baku KBBI, tanda baca
- kealamian: terbaca seperti tulisan peneliti Indonesia yang cermat, bukan terjemahan atau tulisan mesin
- keringkasan: ringkas dan jelas tanpa pleonasme atau kalimat kosong
- kesetiaan: angka, fakta, sitasi, dan batas permintaan dipatuhi; tidak ada fakta karangan

Balas hanya empat baris, format persis:
<aspek>: 1|2|SERI - <alasan singkat>
"""


def kepadatan(teks):
    """Temuan periksa.py per 100 kata, per label, tanpa SG-04."""
    kata = max(len(teks.split()), 1)
    n = {"K": 0, "G": 0, "AI": 0}
    for _, kode, label, _, _ in periksa(teks):
        if kode != "SG-04":
            n[label] += 1
    return {k: v * 100 / kata for k, v in n.items()}


def putusan(teks):
    """{aspek: '1'|'2'|'SERI'}; aspek tanpa putusan dianggap SERI."""
    hasil = {m[1].lower(): m[2].upper() for m in re.finditer(r"^\W*(\w+)\W*:\s*(1|2|SERI)\b", teks, re.M | re.I)}
    return {a: hasil.get(a, "SERI") for a in ASPEK}


def tukar(kid):
    """Urutan acak tetapi tetap per kasus: True berarti A tampil sebagai jawaban 2."""
    return hashlib.sha256(kid.encode()).digest()[0] % 2 == 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("a", nargs="?")
    ap.add_argument("b", nargs="?")
    ap.add_argument("--penilai")
    ap.add_argument("--kasus", help="id dipisah koma")
    ap.add_argument("--tes", action="store_true")
    arg = ap.parse_args()
    if arg.tes:
        return tes()
    semua = json.loads((AKAR / "evals" / "cases.json").read_text(encoding="utf-8"))["cases"]
    pilih = set(arg.kasus.split(",")) if arg.kasus else None
    menang = {a: {"A": 0, "B": 0, "SERI": 0} for a in ASPEK}
    padat = {"A": {"K": 0.0, "G": 0.0, "AI": 0.0}, "B": {"K": 0.0, "G": 0.0, "AI": 0.0}}
    n = 0
    for k in semua:
        fa, fb = Path(arg.a) / f"{k['id']}.md", Path(arg.b) / f"{k['id']}.md"
        if (pilih and k["id"] not in pilih) or not (fa.exists() and fb.exists()):
            continue
        ja, jb = fa.read_text(encoding="utf-8"), fb.read_text(encoding="utf-8")
        if not ja.strip() or not jb.strip():
            print(f"[{k['id']}] LEWAT: jawaban kosong")
            continue
        n += 1
        for sisi, j in (("A", ja), ("B", jb)):
            for lab, v in kepadatan(teks_hasil(j)).items():
                padat[sisi][lab] += v
        if not arg.penilai:
            continue
        t = tukar(k["id"])
        j1, j2 = (jb, ja) if t else (ja, jb)
        p = putusan(jalankan(arg.penilai, PROMPT_BANDING.format(prompt=k["prompt"], j1=j1, j2=j2)))
        baris = []
        for a, v in p.items():
            pemenang = "SERI" if v == "SERI" else ("A" if (v == "1") != t else "B")
            menang[a][pemenang] += 1
            baris.append(f"{a} {pemenang}")
        print(f"[{k['id']}] " + ", ".join(baris))
    if not n:
        print("Tidak ada kasus yang jawabannya ada di kedua folder.")
        return 1
    print(f"\n{n} kasus. Temuan periksa.py per 100 kata (rerata, tanpa SG-04):")
    for sisi, folder in (("A", arg.a), ("B", arg.b)):
        print(f"  {sisi} {folder}: " + ", ".join(f"{lab} {v / n:.2f}" for lab, v in padat[sisi].items()))
    if arg.penilai:
        print("Putusan penilai (A menang / B menang / seri):")
        for a, v in menang.items():
            print(f"  {a:12} {v['A']:3} / {v['B']:3} / {v['SERI']:3}")
    return 0


def tes():
    assert putusan("kebakuan: 1 - a\n**kealamian**: 2 - b\nkeringkasan: seri\n") == {
        "kebakuan": "1", "kealamian": "2", "keringkasan": "SERI", "kesetiaan": "SERI"}
    assert kepadatan("Analisa data dilakukan.")["K"] > 0 and kepadatan("Data dianalisis.")["K"] == 0
    assert tukar("abc") == tukar("abc")
    assert {tukar(f"kasus-{i}") for i in range(20)} == {True, False}
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
