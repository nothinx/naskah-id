#!/usr/bin/env python3
"""Jalankan dan nilai evals/cases.json.

    python evals/jalankan.py --agen "claude -p" --hasil evals/hasil/dengan-skill
    python evals/jalankan.py --hasil evals/hasil/dengan-skill                    # nilai jawaban yang sudah ada
    python evals/jalankan.py --hasil DIR --penilai "claude -p"                   # kriteria dinilai model
    python evals/jalankan.py --hasil DIR --kasus angka-tidak-berubah,tolak-perjokian
    python evals/jalankan.py --tes

--agen: perintah yang menerima prompt di stdin dan menulis jawaban ke stdout. Jawaban disimpan
sebagai <hasil>/<id>.md. Untuk pembanding, jalankan sekali dengan skill dan sekali tanpa skill
ke folder berbeda, lalu bandingkan skornya.

Cek otomatis: angka, sitasi, dan kutipan di "bahan" harus bertahan (periksa.banding),
"harus_ada" harus cocok, "tidak_boleh_ada" tidak boleh cocok. Kriteria lain dinilai --penilai;
tanpa penilai, kriteria dicetak untuk dinilai manusia.

Kode keluar 1 bila ada cek otomatis atau kriteria yang gagal.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR / "scripts"))
from periksa import fakta  # noqa: E402


def jalankan(perintah, masukan):
    r = subprocess.run(perintah, shell=True, input=masukan, capture_output=True, text=True, encoding="utf-8", timeout=600)
    if r.returncode:
        raise RuntimeError(f"{perintah!r} keluar {r.returncode}: {r.stderr.strip()[:300]}")
    return r.stdout


def teks_hasil(jawaban):
    """Bagian jawaban sebelum catatan perubahan."""
    return re.split(r"(?im)^[#*>\s]*(?:catatan|daftar|ringkasan|rincian) perubahan.*$", jawaban)[0]


def cek_otomatis(kasus, jawaban):
    """Daftar kegagalan cek mesin; kosong berarti lulus."""
    gagal = []
    if kasus.get("bahan"):
        a, j = fakta(kasus["bahan"]), fakta(jawaban)
        gagal += [f"{jenis.lower()} hilang: {x}" for jenis in a for x in (a[jenis] - j[jenis]).elements()]
    gagal += [f"tidak ditemukan: /{rx}/" for rx in kasus.get("harus_ada", []) if not re.search(rx, jawaban)]
    # catatan perubahan wajar mengutip teks asli, jadi pola terlarang hanya dicari di teks hasil
    hasil = teks_hasil(jawaban)
    gagal += [f"terlarang muncul: /{rx}/" for rx in kasus.get("tidak_boleh_ada", []) if re.search(rx, hasil)]
    return gagal


PROMPT_PENILAI = """Kamu penilai yang ketat. Nilai jawaban agen terhadap setiap kriteria.

PROMPT PENGGUNA:
{prompt}

JAWABAN AGEN:
{jawaban}

KRITERIA:
{kriteria}

Balas hanya dengan satu baris per kriteria, format persis:
<nomor>: LULUS|GAGAL - <alasan singkat>
"""


def nilai_penilai(teks, n):
    """Ambil putusan per kriteria dari balasan penilai; kriteria tanpa putusan dianggap GAGAL."""
    putusan = {int(m[1]): (m[2] == "LULUS", m[3].strip()) for m in re.finditer(r"^\s*(\d+)\s*:\s*(LULUS|GAGAL)\s*-?\s*(.*)$", teks, re.M)}
    return [putusan.get(i, (False, "tidak dinilai")) for i in range(1, n + 1)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hasil", default=str(AKAR / "evals" / "hasil"))
    ap.add_argument("--agen")
    ap.add_argument("--penilai")
    ap.add_argument("--kasus", help="id dipisah koma")
    ap.add_argument("--tes", action="store_true")
    arg = ap.parse_args()
    if arg.tes:
        return tes()
    semua = json.loads((AKAR / "evals" / "cases.json").read_text(encoding="utf-8"))["cases"]
    pilih = set(arg.kasus.split(",")) if arg.kasus else None
    hasil = Path(arg.hasil)
    hasil.mkdir(parents=True, exist_ok=True)
    total_cek = lulus_cek = total_kr = lulus_kr = 0
    for k in semua:
        if pilih and k["id"] not in pilih:
            continue
        berkas = hasil / f"{k['id']}.md"
        if arg.agen:
            print(f"… {k['id']}", file=sys.stderr)
            berkas.write_text(jalankan(arg.agen, k["prompt"]), encoding="utf-8")
        if not berkas.exists():
            print(f"[{k['id']}] LEWAT: {berkas} belum ada")
            continue
        jawaban = berkas.read_text(encoding="utf-8")
        gagal = cek_otomatis(k, jawaban)
        total_cek += 1
        lulus_cek += not gagal
        print(f"[{k['id']}] cek otomatis: " + ("LULUS" if not gagal else "GAGAL\n    " + "\n    ".join(gagal)))
        if arg.penilai:
            daftar = "\n".join(f"{i}. {c}" for i, c in enumerate(k["kriteria"], 1))
            putusan = nilai_penilai(jalankan(arg.penilai, PROMPT_PENILAI.format(prompt=k["prompt"], jawaban=jawaban, kriteria=daftar)),
                                    len(k["kriteria"]))
            for c, (ok, alasan) in zip(k["kriteria"], putusan):
                print(f"    {'LULUS' if ok else 'GAGAL'}: {c}" + ("" if ok else f" ({alasan})"))
            total_kr += len(putusan)
            lulus_kr += sum(ok for ok, _ in putusan)
        else:
            print("    kriteria (nilai manual):\n" + "\n".join(f"    - {c}" for c in k["kriteria"]))
    print(f"\nCek otomatis: {lulus_cek}/{total_cek} kasus lulus" + (f"; kriteria penilai: {lulus_kr}/{total_kr}" if arg.penilai else ""))
    return 1 if not total_cek or lulus_cek < total_cek or lulus_kr < total_kr else 0


def tes():
    kasus = {"bahan": "Galat turun dari 4,8% menjadi 1,2% (Santoso, 2020).", "harus_ada": [r"\bturun\b"],
             "tidak_boleh_ada": [r"mengalami penurunan"]}
    assert cek_otomatis(kasus, "Galat turun dari 4,8% menjadi 1,2% (Santoso, 2020).") == []
    assert cek_otomatis(kasus, "Galat turun dari 4,8% menjadi 1,2% (Santoso, 2020).\n\n### Catatan perubahan\n- 'mengalami penurunan' diganti 'turun'.") == []
    assert cek_otomatis(kasus, "Galat turun dari 4,8% menjadi 1,2% (Santoso, 2020).\n\n**Daftar perubahan:**\n- `mengalami penurunan` -> `turun`") == []
    assert cek_otomatis(kasus, "Galat turun dari 4,8% menjadi 1,2% (Santoso, 2020), tidak mengalami penurunan perubahan.") == [
        "terlarang muncul: /mengalami penurunan/"]
    assert cek_otomatis(kasus, "Galat mengalami penurunan dari 4,8% menjadi 1,3%.") == [
        "sitasi hilang: (Santoso, 2020)", "angka hilang: 1,2%", r"tidak ditemukan: /\bturun\b/", "terlarang muncul: /mengalami penurunan/"]
    assert nilai_penilai("1: LULUS - ok\n2: GAGAL - angka berubah", 3) == [(True, "ok"), (False, "angka berubah"), (False, "tidak dinilai")]
    semua = json.loads((AKAR / "evals" / "cases.json").read_text(encoding="utf-8"))["cases"]
    assert len({k["id"] for k in semua}) == len(semua), "id kasus ganda"
    for k in semua:
        assert k["kriteria"] and k["prompt"], k["id"]
        for rx in k.get("harus_ada", []) + k.get("tidak_boleh_ada", []):
            re.compile(rx)
        if k.get("bahan"):
            assert k["bahan"] in k["prompt"], f"{k['id']}: bahan bukan bagian prompt"
            assert not cek_otomatis({"bahan": k["bahan"]}, k["prompt"]), k["id"]
    print(f"ok ({len(semua)} kasus)")
    return 0


if __name__ == "__main__":
    for aliran in (sys.stdout, sys.stderr):
        aliran.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.exit(main())
