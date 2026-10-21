#!/usr/bin/env python3
"""Pemeriksa cepat pola K (kaidah) dan AI (klise mesin) dalam naskah Indonesia.

Hasilnya petunjuk, bukan putusan: setiap temuan perlu dibaca dalam konteksnya.
Jangan dipakai untuk menilai apakah sebuah teks ditulis mesin.

Pemakaian:
    python scripts/periksa.py naskah.md [lain.txt ...]   # periksa berkas
    python scripts/periksa.py -                         # baca dari stdin
    python scripts/periksa.py --tes                      # uji mandiri
    python scripts/periksa.py --validasi                 # cek SKILL.md dan rujukannya

Teks yang dilewati: blok kode, `kode sebaris`, ~~coret~~, URL, dan wilayah antara
<!-- periksa:abaikan --> dan <!-- periksa:lanjut -->, serta baris yang diawali
**Sebelum:** atau **Waspadai:**. Contoh kalimat salah di dokumentasi ditulis dengan cara itu.

Kode keluar 1 bila ada temuan K, 0 bila tidak.
"""
import re
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
I = re.IGNORECASE
AWAL = r"(?:^|(?<=[.!?])\s+)"  # awal kalimat; berlaku pada teks yang penanda Markdown-nya sudah dibuang

# (id, label, regex, flag, saran, minimal kemunculan per berkas)
POLA = [
    # Kalimat efektif: subjek hilang, perangkai, pleonasme
    ("KE-01", "K", AWAL + r"(?:Dari|Dalam|Pada|Bagi|Menurut|Berdasarkan)\s(?:(?!\b(?:kami|penulis|peneliti|saya|kita)\b)[^.?!,;:])"
     r"{1,60}?\s(?:menunjukkan|membahas|memperlihatkan|menjelaskan|mengatakan|menyatakan|menggambarkan|menyajikan|menyimpulkan|membuktikan)\b",
     0, "subjek hilang karena kata depan; buang kata depannya atau pakai verba pasif", 1),
    ("KE-02", "K", r"\badalah merupakan\b", I, "pilih salah satu: adalah atau merupakan", 1),
    ("KE-03", "K", r"\b(?:agar supaya|demi untuk|sejak dari)\b", I, "pleonasme; pakai satu kata saja", 1),
    ("KE-04", "K", r"\bsangat\s+\w+\s+sekali\b", I, "pleonasme: sangat … atau … sekali", 1),
    ("KE-05", "K", r"\b(?:para|banyak|berbagai|beberapa)\s+(\w+)-\1\b", I, "penanda jamak ganda; hapus ulangan", 1),
    ("KE-06", "K", r"\bberbagai macam\b", I, "pleonasme: berbagai atau bermacam-macam", 1),
    ("KE-07", "K", r"\b(?:naik ke atas|turun ke bawah|mundur ke belakang|maju ke depan)\b", I, "pleonasme arah", 1),
    ("KE-08", "K", r"\bsaling\s+\w+-me\w+\b", I, "pleonasme: saling … atau bentuk ulang, bukan keduanya", 1),
    ("KE-09", "K", r"\bseperti\b[^.;]{1,80}?\b(?:dan lain-lain|dll\.?|dan sebagainya|dsb\.?)", I,
     "seperti dan dll. sama-sama penanda contoh; pakai salah satu", 1),
    ("KE-10", "K", r"\bberdasarkan pada\b", I, "cukup: berdasarkan", 1),
    ("KE-11", "K", r"\bantara\s+(?!lain\b)[^.,;]{1,40}?\sdengan\b", I, "pasangan baku: antara … dan …", 1),
    ("KE-12", "K", r"\bbaik\s[^.,;]{1,40}?\sataupun\b", I, "pasangan baku: baik … maupun …", 1),
    ("KE-13", "K", r"\bbukan\s(?!hanya\b|saja\b|sekadar\b|cuma\b)[^.;]{1,60}?,\s*tetapi\b", I,
     "bukan … melainkan …; tidak … tetapi …", 1),
    ("KE-14", "K", r"\b(?:meskipun|walaupun|walau|biarpun|kendatipun)\b[^.;]{1,120}?,\s*(?:tetapi|namun)\b", I,
     "dua konjungsi untuk satu hubungan; buang tetapi/namun", 1),
    ("KE-15", "K", AWAL + r"(?:Karena|Sebab)\b[^.;]{1,120}?,\s*maka\b", 0, "karena …, [induk kalimat]; buang maka", 1),
    ("KE-16", "K", AWAL + r"(?:Sehingga|Sedangkan)\b", 0,
     "konjungsi intrakalimat di awal kalimat; gabungkan atau pakai Akibatnya/Adapun", 1),
    ("KE-17", "K", r"\blebih\s+(?!dari\b)\w+\s+dari\b(?!\s+(?:pada|sekadar)\b)", I, "perbandingan memakai daripada", 1),
    # Ejaan
    ("EJ-01", "K", r"\bdimana(?:-mana)?\b", I, "kata depan ditulis terpisah: di mana", 1),
    ("EJ-02", "K", r"\bdi\s(?:analisis|analisa|uji|lakukan|gunakan|ukur|ambil|peroleh|buat|hitung|kembangkan|rancang|teliti|bahas"
     r"|amati|olah|kumpulkan|terapkan|jelaskan|tentukan|sajikan|tampilkan)\b", I, "awalan di- ditulis serangkai", 1),
    ("EJ-03", "K", r"\b(?:di(?:atas|bawah|dalam|luar|depan|belakang|samping|antara|sini|sana|situ)"
     r"|ke(?:atas|bawah|dalam|depan|belakang|samping|sini|sana|situ))\b", I,
     "kata depan di/ke ditulis terpisah", 1),
    ("EJ-04", "K", r"\b(?:kerjasama|tanggungjawab|bertanggungjawab|pertanggung jawaban|kerja-sama|tanggung-jawab)\b", I,
     "kerja sama, tanggung jawab, bertanggung jawab, pertanggungjawaban", 1),
    ("EJ-05", "K", r"\b(?:antar|pasca|non|multi|sub|pra|semi|swa|tuna|ultra|inter|intra|ekstra|mikro|makro|nano|mono"
     r"|poli|purna|dwi|tri|eka) (?=[a-z]{3,})", 0, "bentuk terikat ditulis serangkai: antarmuka, pascasarjana", 1),
    ("EJ-06", "K", AWAL + r"\d+\s+[a-z]", 0, "awal kalimat tidak dengan angka; tulis dengan huruf atau susun ulang", 1),
    ("EJ-07", "K", r"\b\d+\.\d{1,2}\s?(?:%|V|mV|kV|A|mA|W|kW|Hz|kHz|MHz|kg|g|mg|cm|mm|km|m|s|ms|°C)(?!\w)", 0,
     "desimal memakai koma: 0,5 V", 1),
    ("EJ-08", "K", r"\b\d+(?:,\d+)?(?:V|mV|kV|mA|kW|Hz|kHz|MHz|GHz|kg|mg|cm|mm|km|ms)\b", 0,
     "beri spasi antara angka dan lambang satuan: 10 V", 1),
    ("EJ-10", "K", r",\s+sehingga\b", 0, "tanpa koma bila anak kalimat mengikuti induk kalimat (EYD V, tanda koma kaidah 4)", 1),
    ("EJ-09", "K", r"\d\s?(?:Volt|Ampere|Watt|Hertz|Celcius)\b", 0, "pakai lambang satuan: V, A, W, Hz, °C", 1),
    # Klise mesin dan kalke
    ("AI-01", "AI", r"\b[Dd]i era (?:digital|modern|globalisasi|teknologi|revolusi|serba)", 0, "pembuka generik; mulai dari masalah konkret", 1),
    ("AI-02", "AI", r"\bseiring (?:dengan )?(?:perkembangan|kemajuan|berjalannya) (?:zaman|teknologi|waktu)", I,
     "pembuka generik; sebut perubahan yang spesifik", 1),
    ("AI-03", "AI", r"\bt(?:idak|ak) dapat dipungkiri\b", I, "penegas tanpa isi; ganti dengan bukti", 1),
    ("AI-04", "AI", r"\bseperti yang (?:kita )?(?:ketahui|diketahui) bersama\b", I, "pembuka kosong; hapus", 1),
    ("AI-05", "AI", r"\bmemainkan perana?n?\b", I, "kalke play a role; pakai berperan", 1),
    ("AI-06", "AI", r"\bmengambil tempat\b", I, "kalke take place; pakai berlangsung", 1),
    ("AI-07", "AI", r"\bmemegang peranan (?:yang )?(?:sangat )?(?:penting|krusial|vital|sentral)", I,
     "penguat bertumpuk; pakai berperan penting atau jelaskan perannya", 1),
    ("AI-08", "AI", r"\badalah penting untuk\b|\bitu adalah mungkin\b", I, "kalke it is … to; nyatakan langsung", 1),
    ("AI-09", "AI", r"\bsolusi (?:yang )?(?:inovatif|tepat guna dan inovatif|revolusioner)\b", I, "klaim promosi; tunjukkan dengan angka", 1),
    ("AI-10", "AI", r"\blebih dari sekadar\b", I, "struktur retoris; nyatakan langsung", 1),
    ("AI-11", "AI", r"\bmari kita\b|\bperlu diingat bahwa\b", I, "nada ceramah; hapus", 1),
    ("AI-12", "AI", r"\bsangat signifikan\b", I, "signifikan bermakna statistik; sebut nilai uji, jangan diperkuat", 1),
    ("AI-13", "AI", r"\byang mana\b", I, "kalke which; pakai yang atau pecah kalimat", 1),
    ("AI-14", "AI", r"(?<=\w)[,]?\s+di mana\s+(?!pun\b|saja\b)(?!.{0,80}\?)(?=[a-z])", 0, "di mana sebagai penghubung; pakai yang, tempat, atau saat", 1),
    ("AI-15", "AI", r"\bhal ini\b", I, "hal ini berulang; sebut subjeknya", 3),
    ("AI-16", "AI", r"\bselain itu\b", I, "penghubung pembuka berulang; variasikan atau buang", 3),
    ("AI-17", "AI", r"\boleh karena itu\b", I, "penghubung berulang; buang bila logika sudah jelas", 3),
    ("AI-18", "AI", r"\bsecara keseluruhan\b", I, "penutup ritual; hanya di simpulan bila perlu", 2),
    ("AI-19", "AI", r"\bdengan kata lain\b", I, "pengisi berulang", 2),
]

# Kata tidak baku -> baku (KBBI). Dicocokkan sebagai kata utuh, tanpa membedakan huruf besar.
KATA_BAKU = {
    "analisa": "analisis", "dianalisa": "dianalisis", "menganalisa": "menganalisis", "hipotesa": "hipotesis",
    "sintesa": "sintesis", "diagnosa": "diagnosis", "praktek": "praktik", "tehnik": "teknik", "metoda": "metode",
    "sistim": "sistem", "sistimatis": "sistematis", "resiko": "risiko", "kwalitas": "kualitas", "kwantitas": "kuantitas",
    "frekwensi": "frekuensi", "prosentase": "persentase", "obyek": "objek", "subyek": "subjek", "obyektif": "objektif",
    "subyektif": "subjektif", "projek": "proyek", "aktifitas": "aktivitas", "efektifitas": "efektivitas",
    "produktifitas": "produktivitas", "kreatifitas": "kreativitas", "sensitifitas": "sensitivitas",
    "standarisasi": "standardisasi", "ekstrim": "ekstrem", "katagori": "kategori", "merubah": "mengubah",
    "dirubah": "diubah", "mempengaruhi": "memengaruhi", "mengkonsumsi": "mengonsumsi",
    "mensukseskan": "menyukseskan", "mentaati": "menaati", "menterjemahkan": "menerjemahkan",
    "mengkonfirmasi": "mengonfirmasi", "mengkoordinasikan": "mengoordinasikan", "mensosialisasikan": "menyosialisasikan",
    "mentargetkan": "menargetkan", "mempopulerkan": "memopulerkan", "seksama": "saksama", "sekedar": "sekadar",
    "tolak ukur": "tolok ukur", "silahkan": "silakan", "ijin": "izin", "nasehat": "nasihat", "jaman": "zaman",
    "jadual": "jadwal", "hakekat": "hakikat", "kadaluarsa": "kedaluwarsa", "kadaluwarsa": "kedaluwarsa",
    "nampak": "tampak", "himbau": "imbau", "menghimbau": "mengimbau", "himbauan": "imbauan", "terlanjur": "telanjur",
    "trampil": "terampil", "ketrampilan": "keterampilan", "pondasi": "fondasi", "propinsi": "provinsi",
    "teoritis": "teoretis", "konkrit": "konkret", "managemen": "manajemen", "manajement": "manajemen",
    "detil": "detail", "varitas": "varietas", "kontinyu": "kontinu", "orisinil": "orisinal", "realita": "realitas",
    "faham": "paham", "apotik": "apotek", "atlit": "atlet", "cidera": "cedera", "legalisir": "legalisasi",
    "celcius": "Celsius", "ijasah": "ijazah", "komplek": "kompleks", "respon": "respons",
    "kharisma": "karisma", "kwitansi": "kuitansi", "nopember": "November", "menunjukan": "menunjukkan", "ditunjukan": "ditunjukkan",
}
POLA_KB = re.compile(r"\b(" + "|".join(sorted(map(re.escape, KATA_BAKU), key=len, reverse=True)) + r")\b", I)

POLA_C = [(i, lab, re.compile(rx, fl | re.M), sar, mn) for i, lab, rx, fl, sar, mn in POLA]


def bersihkan(teks):
    """Ganti bagian yang dilewati dengan spasi agar posisi baris tetap."""
    kosong = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    teks = re.sub(r"<!--\s*periksa:abaikan\s*-->.*?(?:<!--\s*periksa:lanjut\s*-->|\Z)", kosong, teks, flags=re.S)
    teks = re.sub(r"^[ \t>*+-]*\*\*(?:Sebelum|Waspadai):\*\*.*$", kosong, teks, flags=re.M)
    teks = re.sub(r"^(```|~~~).*?^\1", kosong, teks, flags=re.S | re.M)
    teks = re.sub(r"`[^`\n]*`|~~[^~\n]*~~|https?://\S+|<!--.*?-->", kosong, teks, flags=re.S)
    teks = re.sub(r"^\s*---\n.*?\n---\n", kosong, teks, count=1, flags=re.S)  # frontmatter
    # penanda Markdown di awal baris (judul, kutipan, butir, nomor) diperlakukan sebagai awal kalimat
    teks = re.sub(r"^[ \t]*(?:#+|>+|[-*+]|\d+[.)])[ \t]+(?:\*\*[^*\n]*\*\*[:.]?[ \t]*)?", kosong, teks, flags=re.M)
    return re.sub(r"[*_]", " ", teks)


def periksa(teks):
    """Kembalikan daftar (baris, id, label, cuplikan, saran)."""
    t = bersihkan(teks)
    baris = lambda pos: t.count("\n", 0, pos) + 1
    hasil = []
    for i, lab, rx, sar, mn in POLA_C:
        cocok = list(rx.finditer(t))
        if len(cocok) >= mn:
            hasil += [(baris(m.start()), i, lab, " ".join(m.group(0).split()), sar) for m in cocok]
    for m in POLA_KB.finditer(t):
        hasil.append((baris(m.start()), "KB-01", "K", m.group(0), "baku: " + KATA_BAKU[m.group(0).lower()]))
    return sorted(hasil)


def validasi():
    """Cek frontmatter SKILL.md dan berkas yang dirujuknya. Kembalikan daftar galat."""
    galat = []
    skill = (AKAR / "SKILL.md").read_text(encoding="utf-8")
    fm = re.match(r"---\n(.*?)\n---\n", skill, re.S)
    if not fm:
        return ["SKILL.md: frontmatter tidak ada"]
    meta = dict(re.findall(r"^(\w+):\s*\"?(.*?)\"?\s*$", fm.group(1), re.M))
    if meta.get("name") != "naskah-id":
        galat.append("SKILL.md: name harus naskah-id")
    if not 50 <= len(meta.get("description", "")) <= 1024:
        galat.append("SKILL.md: description harus 50-1024 karakter")
    if skill.count("\n") > 250:
        galat.append("SKILL.md: lebih dari 250 baris")
    for rel in set(re.findall(r"`((?:references|contoh|scripts)/[\w./-]*|KONTRAK\.md)`", skill)):
        if not (AKAR / rel).exists():
            galat.append(f"SKILL.md: rujukan {rel} tidak ada")
    return galat


def tes():
    salah = {
        "Dari hasil pengujian menunjukkan bahwa galat turun.": "KE-01",
        "Menurut Sugiono mengatakan bahwa sampel cukup.": "KE-01",
        "Metode ini adalah merupakan metode baru.": "KE-02",
        "Penurunannya sangat besar sekali.": "KE-04",
        "Para peneliti-peneliti sepakat.": "KE-05",
        "Alat ini terdiri dari berbagai macam modul.": "KE-06",
        "Kami memakai sensor seperti DHT22, LM35, dan lain-lain.": "KE-09",
        "Nilai dihitung berdasarkan pada rumus 2.": "KE-10",
        "Perbedaan antara metode A dengan metode B kecil.": "KE-11",
        "Ini bukan galat acak, tetapi galat sistematis.": "KE-13",
        "Meskipun mahal, tetapi alat ini awet.": "KE-14",
        "Karena arus berlebih, maka sekring putus.": "KE-15",
        "Galat naik. Sehingga hasil tidak valid.": "KE-16",
        "Metode A lebih baik dari metode B.": "KE-17",
        "Ruang dimana alat diuji.": "EJ-01",
        "Data di analisis dengan SPSS.": "EJ-02",
        "Sensor dipasang diatas meja.": "EJ-03",
        "Kerjasama antarlembaga diperlukan.": "EJ-04",
        "Sistem ini memakai antar muka web.": "EJ-05",
        "25 responden dilibatkan.": "EJ-06",
        "Tegangan terukur 0.5 V.": "EJ-07",
        "Catu daya 12V dipakai.": "EJ-08",
        "Catu daya 12 Volt dipakai.": "EJ-09",
        "Di era digital ini, data penting.": "AI-01",
        "Tidak dapat dipungkiri bahwa IoT berkembang.": "AI-03",
        "Sensor memainkan peran penting.": "AI-05",
        "Hasilnya sangat signifikan.": "AI-12",
        "Nilai galat besar, yang mana memengaruhi hasil.": "AI-13",
        "Sistem di mana data dikirim tiap detik.": "AI-14",
        "Kami melakukan analisa data.": "KB-01",
        "Berdasarkan hasil penelitian menyimpulkan bahwa nilainya sedang.": "KE-01",
        "Hasil uji menunjukan nilai r.": "KB-01",
        "Galat turun, sehingga akurasi naik.": "EJ-10",
        "Hal ini benar. Hal ini salah. Hal ini lagi.": "AI-15",
    }
    benar = [
        "Hasil pengujian menunjukkan bahwa galat turun.",
        "Dalam penelitian ini kami membahas metode baru.",
        "Pada Gambar 3, kami menunjukkan hasilnya.",
        "Sampel diambil secara acak dan dianalisis dengan uji-t.",
        "Penurunan ini signifikan (p < 0,01).",
        "Di mana sampel disimpan?",
        "Antara lain dengan cara ini, galat turun.",
        "Bukan hanya murah, tetapi juga awet.",
        "Jumlahnya lebih dari 50 orang.",
        "Biaya ini lebih kecil daripada biaya lama.",
        "Galat naik sehingga hasil tidak valid.",
        "Sebanyak 25 responden dilibatkan.",
        "Tegangan terukur 0,5 V dan beratnya 1.000 kg.",
        "Contoh kalimat salah: `Dari hasil uji menunjukkan`.",
        "<!-- periksa:abaikan -->\nDi era digital ini.\n<!-- periksa:lanjut -->\nTeks bersih.",
        "Hal ini benar. Hal ini juga benar.",
        "Versi Python 3.12 dipakai; lihat Bagian 2.1.",
        "Gaya selingkung dan kebijakan jurnal didahulukan.",
        "- Sampel diambil di laboratorium.",
        "Peserta keluar ruangan. Data bisa disimpan di mana saja.",
        "| 5 km | 2 kg |",
        "**Sebelum:** Dari hasil uji menunjukkan galat turun.",
    ]
    gagal = 0
    for teks, id_ in salah.items():
        ids = {h[1] for h in periksa(teks)}
        if id_ not in ids:
            gagal += 1
            print(f"GAGAL (tidak terdeteksi {id_}): {teks!r} -> {sorted(ids)}")
    for teks in benar:
        h = periksa(teks)
        if h:
            gagal += 1
            print(f"GAGAL (salah positif): {teks!r} -> {[x[1] for x in h]}")
    galat = validasi()
    for g in galat:
        print("GAGAL validasi:", g)
    total = len(salah) + len(benar)
    print(f"{total - gagal}/{total} kasus lulus" + ("" if not galat else f", {len(galat)} galat validasi"))
    return 1 if gagal or galat else 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--tes":
        return tes()
    if argv[0] == "--validasi":
        galat = validasi()
        print("\n".join(galat) or "SKILL.md valid")
        return 1 if galat else 0
    ada_k = False
    for nama in argv:
        teks = sys.stdin.read() if nama == "-" else Path(nama).read_text(encoding="utf-8")
        for baris, id_, lab, cuplikan, saran in periksa(teks):
            ada_k |= lab == "K"
            print(f"{nama}:{baris}: [{id_} {lab}] {cuplikan!r}: {saran}")
    return 1 if ada_k else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.exit(main(sys.argv[1:]))
