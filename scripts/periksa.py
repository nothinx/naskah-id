#!/usr/bin/env python3
"""Pemeriksa cepat pola K (kaidah) dan AI (klise mesin) dalam naskah Indonesia.

Hasilnya petunjuk, bukan putusan: setiap temuan perlu dibaca dalam konteksnya.
Jangan dipakai untuk menilai apakah sebuah teks ditulis mesin.

Pemakaian:
    python scripts/periksa.py naskah.md [skripsi.docx ...]  # periksa berkas (.md, .txt, .docx)
    python scripts/periksa.py -                             # baca dari stdin
    python scripts/periksa.py --banding asli.md hasil.md    # angka, sitasi, kutipan yang berubah (.md, .txt, .docx)
    python scripts/periksa.py --tes                         # uji mandiri
    python scripts/periksa.py --validasi                    # cek SKILL.md dan rujukannya
    python scripts/periksa.py --abaikan SG-04,KL-01 naskah.md  # lewati kode tertentu

Pada berkas .docx, teks diambil per paragraf dari word/document.xml dan nomor baris laporan
adalah nomor paragraf.

Teks yang dilewati: blok kode, `kode sebaris`, ~~coret~~, URL, dan wilayah antara
<!-- periksa:abaikan --> dan <!-- periksa:lanjut -->, serta baris yang diawali
**Sebelum:** atau **Waspadai:**. Contoh kalimat salah di dokumentasi ditulis dengan cara itu.
Bagian Daftar Pustaka/Referensi/Abstract (sampai judul berikutnya) juga dilewati.

Kode keluar 1 bila ada temuan K (atau, pada --banding, ada fakta yang berubah), 0 bila tidak.
"""
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
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
    ("KE-15", "K", AWAL + r"(?:Karena|Sebab|Oleh karena|Berdasarkan|Mengingat)\b[^.;]{1,120}?,\s*maka\b", 0,
     "anak kalimat di depan sudah menandai hubungan; buang maka", 1),
    ("KE-16", "K", AWAL + r"(?:Sehingga|Sedangkan)\b", 0,
     "konjungsi intrakalimat di awal kalimat; gabungkan atau pakai Akibatnya/Adapun", 1),
    ("KE-17", "K", r"\blebih\s+(?!dari\b)\w+\s+dari\b(?!\s+(?:pada|sekadar)\b)", I, "perbandingan memakai daripada", 1),
    # Gaya (G): anjuran, tidak membuat kode keluar 1
    ("NM-01", "G", r"\b(?:melakukan|mengalami|memberikan|mengadakan|melaksanakan)\s+(?:pe\w{3,}an|ke\w{3,}an)\b", I,
     "nominalisasi; pakai verbanya langsung (mengukur, turun, memengaruhi)", 1),
    ("KK-01", "G", r"\bmembuktikan\b", I, "cek kekuatan klaim: menunjukkan atau mengindikasikan bila buktinya statistik/korelasi", 1),
    # Singkatan (references/singkatan.md)
    ("SG-01", "K", r"\b(?:di|ber|se|ke|ter|me[mn]?g?|pe[rn]?)[A-Z]{2,}\b|\b[A-Z]{2,}(?:nya|kan|an|lah|ku|mu)\b", 0,
     lambda c: "imbuhan dan singkatan dirangkai tanda hubung: "
     + re.sub(r"^([a-z]+)(?=[A-Z])|(?<=[A-Z])(?=[a-z]+$)", lambda m: (m.group(1) + "-") if m.group(1) else "-", c), 1),
    ("SG-02", "K", r"\b(?:dll|dsb|dst|dkk|hlm|tsb|yth)\b(?!\.)|(?<![\w/])(?:s/d|a/n|d/a|u/p)(?![\w/])", 0,
     lambda c: "singkatan umum: " + ({"s/d": "s.d.", "a/n": "a.n.", "d/a": "d.a.", "u/p": "u.p."}.get(c) or c + "."), 1),
    ("SG-03", "G", r"\b([A-Z][A-Za-z]*[A-Z])-\1\b", 0, "jamak singkatan tidak diulang: banyak UMKM, para pelaku UMKM", 1),
    # Ejaan
    ("EJ-01", "K", r"\bdimana(?:-mana)?\b", I, "kata depan ditulis terpisah: di mana", 1),
    ("EJ-02", "K", r"\bdi\s(?:analisis|analisa|uji|lakukan|gunakan|ukur|ambil|peroleh|buat|hitung|kembangkan|rancang|teliti|bahas"
     r"|amati|olah|kumpulkan|terapkan|jelaskan|tentukan|sajikan|tampilkan)\b", I, "awalan di- ditulis serangkai", 1),
    ("EJ-03", "K", r"\b(?:di(?:atas|bawah|dalam|luar|depan|belakang|samping|antara|sini|sana|situ)"
     r"|ke(?:atas|bawah|dalam|depan|belakang|samping|sini|sana|situ))\b", I,
     "kata depan di/ke ditulis terpisah", 1),
    ("EJ-04", "K", r"\b(?:kerjasama|tanggungjawab|bertanggungjawab|pertanggung jawaban|kerja-sama|tanggung-jawab)\b", I,
     "kerja sama, tanggung jawab, bertanggung jawab, pertanggungjawaban", 1),
    ("EJ-05", "K", r"\b(?:(?i:antar|pasca|non|multi|sub|pra|semi|swa|tuna|ultra|inter|intra|ekstra|mikro|makro|nano|mono"
     r"|poli|purna)|dwi|tri|eka) (?=[a-z]{3,})", 0, "bentuk terikat ditulis serangkai: antarmuka, pascasarjana", 1),
    ("EJ-06", "K", AWAL + r"\d+\s+[a-z]", 0, "awal kalimat tidak dengan angka; tulis dengan huruf atau susun ulang", 1),
    ("EJ-07", "K", r"\b\d+\.\d{1,2}\s?(?:%|V|mV|kV|A|mA|W|kW|Hz|kHz|MHz|kg|g|mg|cm|mm|km|m|s|ms|°C)(?!\w)", 0,
     lambda c: "desimal memakai koma: " + c.replace(".", ","), 1),
    ("EJ-08", "K", r"(?<![\d.,])\d+(?:[.,]\d+)?(?:V|mV|kV|mA|kW|Hz|kHz|MHz|GHz|kg|mg|cm|mm|km|ms)\b", 0,
     lambda c: "beri spasi antara angka dan lambang satuan: " + re.sub(r"(?<=\d)(?=[^\d.,])", " ", c, count=1), 1),
    ("EJ-10", "K", r",\s+sehingga\b", 0, "tanpa koma bila anak kalimat mengikuti induk kalimat (EYD V, tanda koma kaidah 4)", 1),
    ("EJ-09", "K", r"\d\s?(?:Volt|Ampere|Watt|Hertz|Celcius|Celsius|C)\b", 0, "pakai lambang satuan: V, A, W, Hz, °C", 1),
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

# Kata tidak baku -> baku (KBBI, sinkron dengan references/kata-baku.md). Dicocokkan sebagai kata utuh.
KATA_BAKU = {
    "analisa": "analisis", "dianalisa": "dianalisis", "menganalisa": "menganalisis", "hipotesa": "hipotesis",
    "sintesa": "sintesis", "diagnosa": "diagnosis", "praktek": "praktik", "mempraktekkan": "mempraktikkan",
    "dipraktekkan": "dipraktikkan", "tehnik": "teknik", "metoda": "metode", "sistim": "sistem",
    "sistimatis": "sistematis", "ekosistim": "ekosistem", "resiko": "risiko", "kwalitas": "kualitas",
    "kwantitas": "kuantitas", "frekwensi": "frekuensi", "kwalifikasi": "kualifikasi", "kwota": "kuota",
    "kwartal": "kuartal", "kwadrat": "kuadrat", "kwitansi": "kuitansi", "prosentase": "persentase",
    "presentase": "persentase", "obyek": "objek", "subyek": "subjek", "obyektif": "objektif",
    "subyektif": "subjektif", "projek": "proyek", "aktifitas": "aktivitas", "efektifitas": "efektivitas",
    "produktifitas": "produktivitas", "kreatifitas": "kreativitas", "sensitifitas": "sensitivitas",
    "reaktifitas": "reaktivitas", "konektifitas": "konektivitas", "standarisasi": "standardisasi",
    "ekstrim": "ekstrem", "katagori": "kategori", "komplek": "kompleks", "komplit": "komplet",
    "teoritis": "teoretis", "konkrit": "konkret", "orisinil": "orisinal", "realita": "realitas",
    "respon": "respons", "hirarki": "hierarki", "kuisioner": "kuesioner", "komoditi": "komoditas",
    "otentik": "autentik", "karir": "karier", "managemen": "manajemen", "manajement": "manajemen",
    "detil": "detail", "varitas": "varietas", "kontinyu": "kontinu", "apotik": "apotek", "atlit": "atlet",
    "cidera": "cedera", "syaraf": "saraf", "atmosfir": "atmosfer", "kadaluarsa": "kedaluwarsa",
    "kadaluwarsa": "kedaluwarsa", "legalisir": "legalisasi", "amandemen": "amendemen", "propinsi": "provinsi",
    "pebruari": "Februari", "nopember": "November", "kharisma": "karisma", "celcius": "celsius",
    "seksama": "saksama", "sekedar": "sekadar", "tolak ukur": "tolok ukur", "silahkan": "silakan",
    "ijin": "izin", "diijinkan": "diizinkan", "mengijinkan": "mengizinkan", "nasehat": "nasihat",
    "menasehati": "menasihati", "jaman": "zaman", "jadual": "jadwal", "hakekat": "hakikat", "ijasah": "ijazah",
    "nampak": "tampak", "terlanjur": "telanjur", "faham": "paham", "pondasi": "fondasi", "kaedah": "kaidah",
    "himbau": "imbau", "menghimbau": "mengimbau", "himbauan": "imbauan", "trampil": "terampil",
    "ketrampilan": "keterampilan", "handal": "andal", "kehandalan": "keandalan", "berfikir": "berpikir",
    "perduli": "peduli", "memperdulikan": "memedulikan", "antri": "antre", "antrian": "antrean",
    "lembab": "lembap", "kelembaban": "kelembapan", "nafas": "napas", "bernafas": "bernapas",
    "pernafasan": "pernapasan", "menunjukan": "menunjukkan", "ditunjukan": "ditunjukkan",
    "azas": "asas", "kosa kata": "kosakata", "merubah": "mengubah", "dirubah": "diubah",
    "mempengaruhi": "memengaruhi", "mengkonsumsi": "mengonsumsi", "mengkonfirmasi": "mengonfirmasi",
    "mengkoordinasikan": "mengoordinasikan", "mengkategorikan": "mengategorikan",
    "mengkombinasikan": "mengombinasikan", "mengkomunikasikan": "mengomunikasikan", "mengkoreksi": "mengoreksi",
    "mensukseskan": "menyukseskan", "mensosialisasikan": "menyosialisasikan", "mensimulasikan": "menyimulasikan",
    "mentaati": "menaati", "menterjemahkan": "menerjemahkan", "mentargetkan": "menargetkan",
    "mentelaah": "menelaah", "mempopulerkan": "memopulerkan", "mempublikasikan": "memublikasikan",
}
POLA_KB = re.compile(r"\b(" + "|".join(sorted(map(re.escape, KATA_BAKU), key=len, reverse=True)) + r")\b", I)

POLA_C = [(i, lab, re.compile(rx, fl | re.M), sar, mn) for i, lab, rx, fl, sar, mn in POLA]


def baca(nama):
    """Baca teks dari stdin ('-'), berkas .docx (satu paragraf per baris), atau berkas teks."""
    if nama == "-":
        return sys.stdin.read()
    jalur = Path(nama)
    if jalur.suffix.lower() == ".docx":
        with zipfile.ZipFile(jalur) as z, z.open("word/document.xml") as f:
            akar = ET.parse(f).getroot()
        paragraf = ["".join(t.text or "" for t in p.iter() if t.tag.endswith(("}t", ":t")) or t.tag == "t").replace("\n", " ")
                    for p in akar.iter() if p.tag.endswith(("}p", ":p")) or p.tag == "p"]
        return "\n".join(paragraf)  # paragraf kosong ikut agar nomor baris = nomor paragraf
    return jalur.read_text(encoding="utf-8")


def bersihkan(teks):
    """Ganti bagian yang dilewati dengan spasi agar posisi baris tetap."""
    kosong = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    teks = re.sub(r"<!--\s*periksa:abaikan\s*-->.*?(?:<!--\s*periksa:lanjut\s*-->|\Z)", kosong, teks, flags=re.S)
    teks = re.sub(r"^[ \t>*+-]*\*\*(?:Sebelum|Waspadai):\*\*.*$", kosong, teks, flags=re.M)
    teks = re.sub(r"^(```|~~~).*?^\1", kosong, teks, flags=re.S | re.M)
    teks = re.sub(r"`[^`\n]*`|~~[^~\n]*~~|https?://\S+|<!--.*?-->", kosong, teks, flags=re.S)
    teks = re.sub(r"^\s*---\n.*?\n---\n", kosong, teks, count=1, flags=re.S)  # frontmatter
    # ponytail: bagian berakhir di judul Markdown berikutnya; naskah polos tanpa # dilewati sampai akhir berkas
    teks = re.sub(r"^(?:#+[ \t]*)?(?:daftar pustaka|daftar rujukan|referensi|bibliografi|references|bibliography|abstract)"
                  r"[ \t]*:?[ \t]*$.*?(?=^#|\Z)", kosong, teks, flags=re.S | re.M | re.I)
    # penanda Markdown di awal baris (judul, kutipan, butir, nomor) diperlakukan sebagai awal kalimat
    teks = re.sub(r"^[ \t]*(?:#+|>+|[-*+]|\d+[.)])[ \t]+(?:\*\*[^*\n]*\*\*[:.]?[ \t]*)?", kosong, teks, flags=re.M)
    return re.sub(r"[*_]", " ", teks)


def periksa(teks):
    """Kembalikan daftar (baris, id, label, cuplikan, saran)."""
    t = bersihkan(teks)
    # awal temuan = karakter tak-kosong pertama; pola AWAL ikut menelan spasi dan baris baru sebelumnya
    baris = lambda m: t.count("\n", 0, m.start() + len(m.group(0)) - len(m.group(0).lstrip())) + 1
    hasil = []
    for i, lab, rx, sar, mn in POLA_C:
        cocok = list(rx.finditer(t))
        if len(cocok) >= mn:
            for m in cocok:
                c = " ".join(m.group(0).split())
                hasil.append((baris(m), i, lab, c, sar(c) if callable(sar) else sar))
    for m in POLA_KB.finditer(t):
        hasil.append((baris(m), "KB-01", "K", m.group(0), "baku: " + KATA_BAKU[m.group(0).lower()]))
    hasil += kalimat_panjang(teks, t) + singkatan(t)
    return sorted(hasil)


BATAS_BLOK = re.compile(r"\n(?=[ \t]*(?:\n|>[ \t]*\n|[-*+|#]|\d+[.)][ \t]))")


# Akronim yang sering salah ditulis kapital semua (EYD V: nama diri dari suku kata -> huruf awal kapital,
# bukan nama diri -> huruf kecil). Dicek per token kapital penuh, di luar baris judul berhuruf kapital.
AKRONIM = {
    "BAPPENAS": "Bappenas", "BAPPEDA": "Bappeda", "BULOG": "Bulog", "POLRI": "Polri", "DISHUB": "Dishub",
    "DINKES": "Dinkes", "DISDIK": "Disdik", "KEMENHUB": "Kemenhub", "KEMENKES": "Kemenkes", "KEMENKEU": "Kemenkeu",
    "KEMENDIKBUD": "Kemendikbud", "KEMENDIKBUDRISTEK": "Kemendikbudristek", "KEMDIKTISAINTEK": "Kemdiktisaintek",
    "KEMENDIKTISAINTEK": "Kemendiktisaintek",
    "KEMENDIKDASMEN": "Kemendikdasmen", "BUMDES": "BUMDes", "PERPRES": "Perpres", "PERMEN": "Permen", "PERDA": "Perda",
    "PUSKESMAS": "puskesmas (Puskesmas bila nama)", "POSYANDU": "posyandu (Posyandu bila nama)",
    "IPTEK": "iptek", "PEMILU": "pemilu", "BALITA": "balita", "AMDAL": "amdal", "TILANG": "tilang", "RUDAL": "rudal",
    "PEMDA": "pemda (Pemda bila nama)", "PEMKOT": "pemkot (Pemkot bila nama)", "PEMKAB": "pemkab (Pemkab bila nama)",
    "PEMPROV": "pemprov (Pemprov bila nama)", "GAPOKTAN": "gapoktan (Gapoktan bila nama)",
}
POLA_AKRONIM = re.compile(r"\b(" + "|".join(AKRONIM) + r")\b")
# Singkatan bukan nama diri: kepanjangannya ditulis huruf kecil
BUKAN_NAMA_DIRI = ("UMKM IKM BUMN BUMD BUMDes SDM SDA KTP SIM TKDN ASN PNS K3 PLTS PLTU PLTA PLTB EBT IPAL B3 TIK RSUD "
                   "ASI BBLR ISPA PHBS PAUD SD SMP SMA SMK PTN PTS KKN SKS IPK KTI APBN APBD PDB PDRB PPN NPWP KBLBB").split()
POLA_KEPANJANGAN = re.compile(r"\b[A-Z][a-z]+(?:,?\s+(?:dan\s+|&\s+)?[A-Z][a-z]+)+\s*\(\s*(?:"
                              + "|".join(BUKAN_NAMA_DIRI) + r")\s*\)")
# SG-04: token berhuruf kapital minimal dua dan minimal separuhnya kapital: UMKM, IoT, BUMDes
POLA_TOKEN = re.compile(r"\b[A-Z][A-Za-z0-9]{1,7}\b")
ROMAWI = re.compile(r"[IVXLCDM]+")
# ponytail: daftar tetap; tambah di sini bila singkatan yang dikenal luas pembaca ilmiah ikut ditandai
SINGKATAN_UMUM = set("""RI DKI DIY NTB NTT TK SD SMP SMA SMK MI MTs MA MHz GHz MW GW MWh GWh MPa GPa OK DNA RNA PCR COVID
    DOI ISBN ISSN URL HTTP HTTPS PDF API USB GPS LED LCD CPU GPU RAM PC TV IP WIB WITA WIT UTC IEEE ISO SPSS WHO
    MIT GPL LGPL AGPL BSD CC0""".split())


def baris_kapital(t, pos):
    """Baris judul berhuruf kapital semua (BAB I PENDAHULUAN) tidak diperiksa untuk singkatan."""
    awal, akhir = t.rfind("\n", 0, pos) + 1, t.find("\n", pos)
    huruf = [c for c in t[awal:akhir if akhir >= 0 else None] if c.isalpha()]
    return len(huruf) > 3 and all(c.isupper() for c in huruf)


def singkatan(t):
    """SG-04, SG-05, SG-06. Kembalikan daftar temuan."""
    baris = lambda pos: t.count("\n", 0, pos) + 1
    hasil, pertama = [], {}
    for m in POLA_AKRONIM.finditer(t):
        if not baris_kapital(t, m.start()):
            hasil.append((baris(m.start()), "SG-05", "K", m.group(0), "akronim: " + AKRONIM[m.group(0)]))
    for m in POLA_KEPANJANGAN.finditer(t):
        kep, sing = m.group(0).split("(")
        # buang kata awal kalimat yang bukan bagian kepanjangan ("Namun Usaha Mikro, …"): ambil kata isi
        # sebanyak huruf kapital singkatan (UMKM -> 4, BUMDes -> 4)
        isi = [k for k in re.finditer(r"[A-Z][a-z]+", kep)]
        n = sum(c.isupper() for c in sing)
        if 2 <= n < len(isi):
            kep = kep[isi[-n].start():]
        if len(re.findall(r"[A-Z][a-z]+", kep)) >= 2:
            hasil.append((baris(m.start()), "SG-06", "G", " ".join((kep + "(" + sing).split()),
                          "kepanjangan singkatan bukan nama diri ditulis huruf kecil: " + " ".join(kep.lower().split())))
    for m in POLA_TOKEN.finditer(t):
        w = m.group(0)
        besar = sum(c.isupper() for c in w)
        sesudah = t[m.end():m.end() + 2]
        if (besar < 2 or besar * 2 < sum(c.isalpha() for c in w) or w in SINGKATAN_UMUM or ROMAWI.fullmatch(w)
                or w in AKRONIM or baris_kapital(t, m.start()) or re.match(r"-\d", sesudah)  # KE-01, COVID-19
                or (len(w) > 3 and any(c.isdigit() for c in w))  # ESP32, STM32; K3 dan B3 tetap diperiksa
                or re.search(r"\bCC[\s-]+(?:(?:BY|NC|ND|SA)[\s-]*)*$", t[max(0, m.start() - 20):m.start()])  # CC BY-SA
                or t[t.rfind("\n", 0, m.start()) + 1:].lstrip().startswith("|")  # baris tabel
                or re.search(r"\[[^\]]*$", t[max(0, m.start() - 200):m.start()])  # [PERLU DATA: …], [NAMA ALAT]
                or (w.isupper() and re.match(r"\s+[A-Z]{3,}\b", t[m.end():]))):  # label: TIDAK DITEMUKAN
            continue
        pertama.setdefault(w, []).append(m.start())
    for w, posisi in pertama.items():
        def menjelaskan(i):  # "(…, UMKM)" atau "UMKM (kepanjangan)"
            return bool(re.search(r"\([^()\n]*$", t[max(0, i - 120):i]) and re.match(r"\s*[)\],;]", t[i + len(w):])) \
                or bool(re.match(r"\s*\((?!\s*\d)", t[i + len(w):]))
        if menjelaskan(posisi[0]):
            continue
        ket = ("dijelaskan setelah dipakai; pindahkan kepanjangan ke kemunculan pertama"
               if any(map(menjelaskan, posisi[1:])) else
               "belum dijelaskan: tulis kepanjangan (SINGKATAN) pada kemunculan pertama, kecuali sudah di bagian sebelumnya")
        hasil.append((baris(posisi[0]), "SG-04", "G", w, ket))
    return hasil


def kalimat_panjang(teks, t, maks=35):
    """KL-01 (G): kalimat lebih dari maks kata. Blok dipisah di baris kosong, butir, judul, dan tabel teks asli."""
    hasil, awal = [], 0
    for m in list(BATAS_BLOK.finditer(teks)) + [None]:
        akhir = m.start() if m else len(t)
        blok = t[awal:akhir]
        if "|" not in teks[awal:akhir]:
            for k in re.finditer(r"[^.!?]+[.!?]?", blok):  # titik desimal dan singkatan memotong: hanya mengurangi temuan
                kata = re.findall(r"[^\W\d_]+", k.group(0))
                if len(kata) > maks:
                    pos = awal + k.start() + len(k.group(0)) - len(k.group(0).lstrip())
                    hasil.append((t.count("\n", 0, pos) + 1, "KL-01", "G", " ".join(kata[:6]) + " …",
                                  f"{len(kata)} kata; pecah menjadi dua kalimat atau lebih"))
        awal = akhir
    return hasil


KUTIPAN = re.compile(r'"[^"\n]{3,}"|“[^”]{3,}”')
SITASI = re.compile(r"\[\d+(?:\s*[-–,]\s*\d+)*\]"  # [3], [3-5], [1, 4]
                    r"|(?:[A-Z][\w'-]+(?:\s+(?:et al\.|dkk\.)|\s+(?:&|dan)\s+[A-Z][\w'-]+)?\s+)?"
                    r"\((?=[^()]*\b(?:19|20)\d{2}[a-z]?\b)[^()\n]{1,200}\)")  # (Nama, 2020), Nama (2020)
ANGKA = re.compile(r"(?:[<>≤≥]\s*)?(?<![\w.,])\d+(?:[.,]\d+)*(?:\s?%)?")


def fakta(teks):
    """Ambil kutipan, sitasi, dan angka (berurutan; yang sudah diambil dibuang) sebagai multiset."""
    hasil = {}
    for jenis, rx in (("KUTIPAN", KUTIPAN), ("SITASI", SITASI), ("ANGKA", ANGKA)):
        hasil[jenis] = Counter(re.sub(r"\s+", "" if jenis == "ANGKA" else " ", m.group(0)) for m in rx.finditer(teks))
        teks = rx.sub(" ", teks)
    return hasil


def banding(asli, hasil):
    """Kembalikan daftar (jenis, keterangan) untuk fakta yang hilang atau bertambah."""
    # ponytail: dibandingkan sebagai multiset, posisi tidak dicek; angka yang ditulis ulang dengan huruf ikut terlapor hilang
    a, h = fakta(asli), fakta(hasil)
    laporan = []
    for jenis in a:
        hilang, baru = list((a[jenis] - h[jenis]).elements()), list((h[jenis] - a[jenis]).elements())
        if jenis == "ANGKA":  # 0.5 -> 0,5 adalah koreksi EYD yang sah; laporkan terpisah
            for x in list(hilang):
                y = x.translate(str.maketrans(".,", ",."))
                if y in baru:
                    hilang.remove(x)
                    baru.remove(y)
                    laporan.append(("PEMISAH", f"{x} -> {y} (cek: koreksi desimal atau nilai berubah?)"))
        laporan += [(jenis, f"hilang: {x}") for x in hilang] + [(jenis, f"baru: {x}") for x in baru]
    return laporan


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
        "Berdasarkan uraian tersebut, maka perlu dilakukan penelitian.": "KE-15",
        "Kami melakukan pengukuran tegangan.": "NM-01",
        "Nilai galat mengalami penurunan.": "NM-01",
        "Hal ini membuktikan bahwa tidur menyebabkan nilai naik.": "KK-01",
        " ".join(["kata"] * 36) + ".": "KL-01",
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
        "Data dikumpulkan dengan kuisioner untuk menguji hirarki dan kelembaban.": "KB-01",
        "Sistem antrian ini handal untuk melatih kemampuan berfikir.": "KB-01",
        "Peneliti mengkategorikan dan mempublikasikan hasil.": "KB-01",
        "Galat turun, sehingga akurasi naik.": "EJ-10",
        "Hal ini benar. Hal ini salah. Hal ini lagi.": "AI-15",
        "Antar muka dibuat dengan Qt.": "EJ-05",
        "Non parametrik dipakai.": "EJ-05",
        "Pengujian pada suhu 25 C.": "EJ-09",
        "Karyawan itu diPHK tahun lalu.": "SG-01",
        "Omzet UMKMnya naik.": "SG-01",
        "Bahan, alat, dll disiapkan.": "SG-02",
        "Data 2019 s/d 2021 dipakai.": "SG-02",
        "Usaha mikro, kecil, dan menengah (UMKM) tumbuh. UMKM-UMKM itu kecil.": "SG-03",
        "Data UMKM diambil dari BPS.": "SG-04",
        "Data UMKM diambil. Usaha mikro, kecil, dan menengah (UMKM) tumbuh.": "SG-04",
        "Data dari BAPPENAS dipakai.": "SG-05",
        "Perkembangan IPTEK pesat.": "SG-05",
        "Usaha Mikro, Kecil, dan Menengah (UMKM) tumbuh.": "SG-06",
        "Catu daya 3.3V dipakai.": "EJ-08",
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
        "Data diolah oleh Tri Wahyuni dan Dwi Santoso.",
        "Data diolah.\n\n## Daftar Pustaka\n\nSmith, J. (2020). Multi agent systems for inter vehicle use.",
        "DAFTAR PUSTAKA\nGarcia, L. (2019). Ultra wideband sensing. Respon sistem.",
        "Suhu 25 °C dipakai.",
        "Karyawan itu di-PHK (pemutusan hubungan kerja). Omzet usaha mikro, kecil, dan menengah (UMKM) dan UMKM-nya naik.",
        "Bahan, alat, dll. disiapkan dari 2019 s.d. 2021 (Santoso dkk., 2020).",
        "Usaha mikro, kecil, dan menengah (UMKM) tumbuh. Banyak UMKM kecil.",
        "Data diambil dari Badan Pusat Statistik (BPS). BPS mencatat kenaikan.",
        "*Internet of Things* (IoT) dipakai. Sistem IoT ini murah.",
        "Bab IV membahas hasil pada frekuensi 433 MHz.",
        "BAB I PENDAHULUAN DAN BAPPENAS",
        "Data dari Bappenas dan puskesmas dipakai.",
        "Sistem memakai ESP32 dan modul LoRa (*long range*).",
        "Artikel ini berlisensi CC BY-SA 4.0 dan CC BY-NC-ND, sedangkan kodenya MIT dan GPL.",
        "Sampel diambil dari siswa SD/MI, SMP/MTs, dan SMA/MA.",
        "Prevalensi masih tinggi [PERLU DATA: angka\nterbaru dan sumbernya, misalnya SSGI].",
        " ".join(["kata"] * 35) + ".",
        "- " + " ".join(["butir"] * 20) + "\n- " + " ".join(["butir"] * 20),
        "| " + " | ".join(["sel"] * 40) + " |",
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
    # nomor baris dan saran dinamis
    h = periksa("Baris satu.\nDalam Tabel 2 menunjukkan hasil.")
    if [x[0] for x in h if x[1] == "KE-01"] != [2]:
        gagal += 1
        print("GAGAL nomor baris KE-01:", h)
    h = {x[1]: x for x in periksa("Catu daya 3.3V dipakai.")}
    if h.get("EJ-08", ("",) * 5)[3:] != ("3.3V", "beri spasi antara angka dan lambang satuan: 3.3 V") \
            or not h.get("EJ-07", ("",) * 5)[4].endswith("3,3V"):
        gagal += 1
        print("GAGAL saran dinamis:", h)
    h = [x for x in periksa("Namun Usaha Mikro, Kecil, dan Menengah (UMKM) sulit.") if x[1] == "SG-06"]
    if [x[3] for x in h] != ["Usaha Mikro, Kecil, dan Menengah (UMKM)"]:
        gagal += 1
        print("GAGAL kepanjangan SG-06:", h)
    # berkas .docx: nomor baris = nomor paragraf, dan --banding mendukung .docx
    with tempfile.TemporaryDirectory() as d:
        ns = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
        def buat(nama, par):
            with zipfile.ZipFile(Path(d) / nama, "w") as z:
                z.writestr("word/document.xml", f"<w:document {ns}><w:body>"
                           + "".join(f"<w:p><w:r><w:t>{p}</w:t></w:r></w:p>" for p in par) + "</w:body></w:document>")
        buat("uji.docx", ["Paragraf pertama bersih.", "Dari hasil pengujian menunjukkan analisa salah."])
        buat("hasil.docx", ["Paragraf pertama bersih dan galat 1,5%.", "Hasil pengujian menunjukkan analisis benar."])
        h_docx = [(x[0], x[1]) for x in periksa(baca(Path(d) / "uji.docx"))]
        if h_docx != [(2, "KB-01"), (2, "KE-01")] or banding(baca(Path(d) / "uji.docx"), baca(Path(d) / "hasil.docx")) != [("ANGKA", "baru: 1,5%")]:
            gagal += 1
            print("GAGAL docx:", h_docx)
    # banding: (asli, hasil, laporan yang diharapkan)
    kasus_banding = [
        ("Galat turun dari 4,8% menjadi 1,2% (p < 0,01).", "Galat turun dari 4,8% ke 1,2% (p < 0,01).", []),
        ("Galat turun dari 4,8% menjadi 1,2%.", "Galat turun dari 4,8% menjadi 1,5%.",
         [("ANGKA", "hilang: 1,2%"), ("ANGKA", "baru: 1,5%")]),
        ("Nilai p < 0,05.", "Nilai p > 0,05.", [("ANGKA", "hilang: <0,05"), ("ANGKA", "baru: >0,05")]),
        ("Tegangan 0.5 V.", "Tegangan 0,5 V.", [("PEMISAH", "0.5 -> 0,5 (cek: koreksi desimal atau nilai berubah?)")]),
        ("Hal ini sesuai (Santoso, 2020) dan [3].", "Temuan ini sesuai dengan [3].", [("SITASI", "hilang: (Santoso, 2020)")]),
        ("Menurut Santoso (2020), galat kecil.", "Santoso (2021) menemukan galat kecil.",
         [("SITASI", "hilang: Santoso (2020)"), ("SITASI", "baru: Santoso (2021)")]),
        ('Informan berkata, "Dana telat, kami berhenti."', 'Informan berkata, "Dana terlambat, kami berhenti."',
         [("KUTIPAN", 'hilang: "Dana telat, kami berhenti."'), ("KUTIPAN", 'baru: "Dana terlambat, kami berhenti."')]),
    ]
    for asli, hasil, harap in kasus_banding:
        if sorted(banding(asli, hasil)) != sorted(harap):
            gagal += 1
            print(f"GAGAL banding: {asli!r} -> {banding(asli, hasil)}")
    galat = validasi()
    for g in galat:
        print("GAGAL validasi:", g)
    total = len(salah) + len(benar) + 4 + len(kasus_banding)
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
    if argv[0] == "--banding":
        if len(argv) != 3:
            print("pemakaian: periksa.py --banding asli.md hasil.md")
            return 2
        laporan = banding(*(baca(n) for n in argv[1:]))
        for jenis, ket in laporan:
            print(f"[{jenis}] {ket}")
        print("Angka, sitasi, dan kutipan sama." if not laporan else f"{len(laporan)} perbedaan; periksa satu per satu.")
        return 1 if any(j != "PEMISAH" for j, _ in laporan) else 0
    abaikan = set()
    if argv[0] == "--abaikan":
        abaikan, argv = set(argv[1].split(",")), argv[2:]
    ada_k = False
    for nama in (p for a in argv for p in (sorted(map(str, Path().glob(a))) if "*" in a or "?" in a else [a])):
        teks = baca(nama)
        temuan = [x for x in periksa(teks) if x[1] not in abaikan]
        for baris, id_, lab, cuplikan, saran in temuan:
            ada_k |= lab == "K"
            print(f"{nama}:{baris}: [{id_} {lab}] {cuplikan!r}: {saran}")
        if temuan:
            jumlah = Counter(x[2] for x in temuan)
            print(f"{nama}: {len(temuan)} temuan (" + ", ".join(f"{l} {jumlah[l]}" for l in ("K", "G", "AI") if jumlah[l]) + ")")
    return 1 if ada_k else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.exit(main(sys.argv[1:]))
