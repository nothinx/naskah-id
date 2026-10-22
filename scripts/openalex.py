"""Cari, verifikasi, dan kutip karya ilmiah lewat OpenAlex, dengan Crossref sebagai cadangan (stdlib saja).

  python scripts/openalex.py cari "vehicle speedometer calibration" [--tahun 2018-2026] [--n 10] [--oa] [--urut sitasi]
  python scripts/openalex.py doi 10.1109/ACCESS.2020.2970143          # detail + abstrak
  python scripts/openalex.py bib 10.1109/xxx W2741809807 ...           # BibTeX (DOI atau id OpenAlex)
  python scripts/openalex.py rujukan 10.1109/xxx --gaya apa|ieee|bib   # entri daftar pustaka siap tempel
  python scripts/openalex.py cek "Judul persis" [--doi 10.x] [--penulis "Santoso, Dewi"] [--tahun 2021]
  python scripts/openalex.py daftar pustaka.txt                        # cek seluruh daftar pustaka, satu entri per baris
  python scripts/openalex.py dikutip W2741809807 [--n 10]              # karya yang mengutip
  python scripts/openalex.py istilah "catu daya" "power supply" [--bidang teknik] [--tahun 2019-2026]
                                                                       # istilah mana yang hidup di karya berbahasa Indonesia
  python scripts/openalex.py --tes

Karya yang tidak ada di OpenAlex dicari di Crossref; jurnal SINTA ber-DOI umumnya terdaftar di sana.
Kode keluar: 0 cocok/berhasil, 1 meragukan atau tidak ditemukan, 2 galat jaringan atau pemakaian.

Tanpa kunci, kuota harian OpenAlex kecil. Kunci API gratis: https://openalex.org/settings/api
  Windows:      setx OPENALEX_API_KEY "<kunci>"   (buka terminal baru setelahnya)
  macOS/Linux:  export OPENALEX_API_KEY="<kunci>"  (tambahkan ke ~/.bashrc atau ~/.zshrc)
"""
import json, os, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from difflib import SequenceMatcher

API = "https://api.openalex.org"
CROSSREF = "https://api.crossref.org"
KEY = os.environ.get("OPENALEX_API_KEY", "")
UA = "naskah-id/1.0 (+https://github.com/nothinx/naskah-id)"
FIELDS = "id,doi,title,publication_year,authorships,primary_location,cited_by_count,open_access,type,biblio,abstract_inverted_index"


class GalatJaringan(Exception):
    pass


def get(url, **q):
    """GET JSON. None bila 404; GalatJaringan untuk galat lain (kuota, server, koneksi)."""
    q = {k: v for k, v in q.items() if v not in (None, "")}
    if KEY and url.startswith(API):
        q["api_key"] = KEY
    req = urllib.request.Request(f"{url}?{urllib.parse.urlencode(q)}", headers={"User-Agent": UA})
    for coba in range(4):  # 429 dan 5xx dicoba ulang dengan jeda bertambah
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if (e.code == 429 or e.code >= 500) and coba < 3:
                time.sleep(min(float(e.headers.get("Retry-After") or 2 ** coba), 30))
                continue
            hint = " (OPENALEX_API_KEY belum diset; kuota tanpa kunci kecil)" if url.startswith(API) and not KEY else ""
            raise GalatJaringan(f"{url.split('/')[2]} HTTP {e.code}{hint}")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise GalatJaringan(f"tidak bisa menghubungi {url.split('/')[2]}: {getattr(e, 'reason', e)}")


# --- normalisasi: OpenAlex dan Crossref menjadi satu bentuk "karya" ---

def bersih_doi(s):
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", (s or "").strip(), flags=re.I)


def dari_openalex(w):
    b = w.get("biblio") or {}
    inv = w.get("abstract_inverted_index") or {}
    return {
        "sumber": "OpenAlex", "id": w["id"].rsplit("/", 1)[-1], "doi": bersih_doi(w.get("doi")),
        "judul": w.get("title") or "", "tahun": w.get("publication_year"),
        "penulis": [a["author"]["display_name"] for a in w.get("authorships") or []],
        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
        "vol": b.get("volume"), "no": b.get("issue"), "hal": [p for p in (b.get("first_page"), b.get("last_page")) if p],
        "jenis": w.get("type"), "sitasi": w.get("cited_by_count", 0), "oa": (w.get("open_access") or {}).get("is_oa"),
        "abstrak": " ".join(k for _, k in sorted((i, k) for k, idx in inv.items() for i in idx)),
    }


def dari_crossref(m):
    tgl = (m.get("published") or m.get("issued") or {}).get("date-parts") or [[None]]
    jenis = {"journal-article": "article", "proceedings-article": "proceedings", "book-chapter": "book-chapter",
             "book": "book", "dissertation": "dissertation"}.get(m.get("type"), m.get("type"))
    return {
        "sumber": "Crossref", "id": "", "doi": bersih_doi(m.get("DOI")),
        "judul": " ".join((m.get("title") or [""])[0].split()), "tahun": tgl[0][0],
        "penulis": [" ".join(p for p in (a.get("given"), a.get("family")) if p) or a.get("name", "")
                    for a in m.get("author") or []],
        "venue": (m.get("container-title") or [""])[0], "vol": m.get("volume"), "no": m.get("issue"),
        "hal": [p for p in (m.get("page") or "").replace("–", "-").split("-") if p][:2],
        "jenis": jenis, "sitasi": m.get("is-referenced-by-count", 0), "oa": None,
        "abstrak": re.sub(r"<[^>]+>", "", m.get("abstract") or "").strip(),
    }


def ambil(ident):
    """Satu karya dari DOI atau id OpenAlex; DOI yang tak dikenal OpenAlex dicari di Crossref."""
    ident = ident.strip()
    if re.match(r"^W\d+$", ident, re.I):
        w = get(f"{API}/works/{ident.upper()}", select=FIELDS)
        return dari_openalex(w) if w else None
    doi = bersih_doi(ident)
    try:
        w = get(f"{API}/works/doi:{doi}", select=FIELDS)
        if w:
            return dari_openalex(w)
    except GalatJaringan:
        pass  # kuota OpenAlex habis atau server sibuk: Crossref masih bisa menjawab
    m = get(f"{CROSSREF}/works/{urllib.parse.quote(doi)}")
    return dari_crossref(m["message"]) if m else None


def cari_judul(judul, cukup, n=10):
    """Kandidat dari OpenAlex; Crossref ikut dicari bila OpenAlex gagal atau tidak ada kandidat yang cukup(k)."""
    hasil = []
    try:
        r = get(f"{API}/works", search=judul, per_page=n, select=FIELDS)
        hasil = [dari_openalex(w) for w in r["results"]]
    except GalatJaringan:
        pass
    if not any(map(cukup, hasil)):
        r = get(f"{CROSSREF}/works", **{"query.bibliographic": judul, "rows": n})
        hasil += [dari_crossref(m) for m in (r or {}).get("message", {}).get("items", [])]
    return hasil


# --- pencocokan ---

def norm(s):
    s = unicodedata.normalize("NFKD", re.sub(r"[^\w\s]", " ", s or "")).encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def mirip(a, b):
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def cocokkan(k, judul="", penulis=(), tahun=None, ambang=0.9):
    """Kembalikan daftar alasan tidak cocok; kosong berarti cocok. Selisih tahun 1 hanya catatan."""
    alasan = []
    s = mirip(judul, k["judul"]) if judul else 1
    if s < ambang:
        alasan.append(f"judul beda (kemiripan {s:.2f})")
    nama = norm(" ".join(k["penulis"])).split()
    for p in penulis:
        if p.strip() and not all(t in nama for t in norm(p).split()):
            alasan.append(f"penulis {p.strip()} tidak ada")
    if tahun and k["tahun"] and abs(int(tahun) - int(k["tahun"])) > 1:
        alasan.append(f"tahun {tahun} ≠ {k['tahun']}")
    return alasan


AFILIASI = re.compile(r"\b(?:universitas|university|univ|fakultas|faculty|jurusan|program studi|prodi|department|departemen"
                      r"|institut|institute|politeknik|sekolah tinggi|indonesia)\b", re.I)


def penulis_rusak(k):
    """Metadata penulis yang memuat afiliasi atau deretan inisial; terjadi pada sebagian jurnal OJS."""
    return any(AFILIASI.search(n) or len(re.findall(r"\b[A-Z]\.", n)) >= 4 or len(n.split()) > 6 for n in k["penulis"])


PERINGATAN_PENULIS = "PERINGATAN: metadata penulis tampak memuat afiliasi; salin nama penulis dari PDF artikelnya."


def tebak_judul(baris):
    """Judul dari entri daftar pustaka: dalam tanda petik (IEEE) atau sesudah (tahun). (APA)."""
    m = re.search(r'["“]([^"”]{10,})["”]', baris) or re.search(r"\((?:19|20)\d{2}[a-z]?\)\.?\s+(.{10,}?)[.?!](?:\s|$)", baris)
    return m.group(1).strip(" ,.") if m else baris


def calon_entri(e):
    """Kandidat karya untuk satu entri: DOI bila ada, lalu Crossref, lalu OpenAlex (praterbit arXiv tidak ada di Crossref)."""
    doi = re.search(r"10\.\d{4,9}/[^\s,;]+", e)
    calon = [ambil(doi.group(0).rstrip("."))] if doi else []
    calon = [c for c in calon if c]
    if not any(not nilai_entri(e, c) for c in calon):
        r = get(f"{CROSSREF}/works", **{"query.bibliographic": e, "rows": 3})
        calon += [dari_crossref(m) for m in (r or {}).get("message", {}).get("items", [])]
    if not any(not nilai_entri(e, c) for c in calon):
        try:
            r = get(f"{API}/works", search=tebak_judul(e), per_page=5, select=FIELDS)
            calon += [dari_openalex(w) for w in (r or {}).get("results", [])]
        except GalatJaringan:
            pass
    return calon


def cakupan(judul, baris):
    """Porsi judul yang muncul di baris daftar pustaka (0..1)."""
    j, b = norm(judul), norm(baris)
    if not j:
        return 0
    return sum(m.size for m in SequenceMatcher(None, j, b, autojunk=False).get_matching_blocks()) / len(j)


def nilai_entri(baris, k):
    """Alasan entri daftar pustaka tidak cocok dengan karya k; kosong berarti cocok."""
    alasan = []
    c = cakupan(k["judul"], baris)
    if c < 0.9:
        alasan.append(f"judul tidak cocok (cakupan {c:.2f})")
    if k["penulis"]:
        akhir = norm(k["penulis"][0]).split()[-1:]
        if akhir and akhir[0] not in norm(baris).split():
            alasan.append(f"penulis pertama {k['penulis'][0]} tidak disebut")
    tahun_baris = {int(t) for t in re.findall(r"\b(?:19|20)\d{2}\b", baris)}
    if k["tahun"] and not any(abs(t - k["tahun"]) <= 1 for t in tahun_baris):
        alasan.append(f"tahun {k['tahun']} tidak disebut")
    return alasan


# --- keluaran ---

def ringkas(k):
    oa = " [OA]" if k["oa"] else ""
    nama = ", ".join(k["penulis"][:3]) + (" et al." if len(k["penulis"]) > 3 else "")
    return (f"- {k['judul']} ({k['tahun']})\n  {nama} — {k['venue']}\n"
            f"  doi:{k['doi'] or '-'}  id:{k['id'] or '-'}  sitasi:{k['sitasi']}  sumber:{k['sumber']}{oa}")


def pisah_nama(n):
    """'Budi Santoso' -> ('Santoso', 'Budi'); nama tunggal -> ('Sugiyono', '')."""
    t = n.split()
    return (t[-1], " ".join(t[:-1])) if t else ("", "")


def inisial(depan):
    return " ".join("-".join(b[0] + "." for b in kata.split("-") if b) for kata in depan.split())


def bibtex(k):
    first = re.sub(r"\W", "", pisah_nama(k["penulis"][0])[0] if k["penulis"] else "anon").lower()
    word = next((t for t in norm(k["judul"]).split() if len(t) > 3), "x")
    kind = {"article": "article", "proceedings": "inproceedings", "book": "book", "book-chapter": "incollection",
            "dissertation": "phdthesis"}.get(k["jenis"], "misc")
    if kind == "article" and any(s in k["venue"].lower() for s in ("conference", "proceedings", "prosiding", "seminar")):
        kind = "inproceedings"
    f = {"title": "{" + k["judul"] + "}", "author": " and ".join(k["penulis"]), "year": k["tahun"],
         ("booktitle" if kind in ("inproceedings", "incollection") else "journal"): k["venue"],
         "volume": k["vol"], "number": k["no"], "pages": "--".join(k["hal"]), "doi": k["doi"]}
    body = ",\n".join(f"  {a} = {{{v}}}" for a, v in f.items() if v)
    return f"@{kind}{{{first}{k['tahun'] or ''}{word},\n{body}\n}}"


def apa(k):
    """APA 7. Huruf miring ditandai *…* (Markdown)."""
    nama = [f"{b}, {inisial(d)}".rstrip(", ") for b, d in map(pisah_nama, k["penulis"])]
    if len(nama) > 20:
        nama = nama[:19] + ["… " + nama[-1]]
        penulis = ", ".join(nama)
    else:
        penulis = nama[0] if len(nama) == 1 else ", ".join(nama[:-1]) + ", & " + nama[-1] if nama else ""
    judul = k["judul"].rstrip(".")
    s = f"{penulis} ({k['tahun'] or 't.t.'}). {judul}." if penulis else f"{judul}. ({k['tahun'] or 't.t.'})."
    if k["venue"]:
        s += f" *{k['venue']}*"
        s += f", *{k['vol']}*" if k["vol"] else ""
        s += f"({k['no']})" if k["no"] else ""
        s += ", " + "–".join(k["hal"]) if k["hal"] else ""
        s += "."
    return s + (f" https://doi.org/{k['doi']}" if k["doi"] else "")


def ieee(k):
    """IEEE gaya naskah Indonesia (dkk., hlm.); ganti ke et al./pp. bila templat berbahasa Inggris."""
    nama = [" ".join(filter(None, (inisial(d), b))) for b, d in map(pisah_nama, k["penulis"])]
    if len(nama) > 6:
        penulis = nama[0] + " dkk."
    else:
        penulis = nama[0] if len(nama) == 1 else ", ".join(nama[:-1]) + (", dan " if len(nama) > 2 else " dan ") + nama[-1] if nama else ""
    bagian = [f"{penulis}, \"{k['judul'].rstrip('.')},\"", f"*{k['venue']}*" if k["venue"] else "",
              f"vol. {k['vol']}" if k["vol"] else "", f"no. {k['no']}" if k["no"] else "",
              ("hlm. " + "–".join(k["hal"])) if k["hal"] else "", str(k["tahun"] or "")]
    s = ", ".join(b for b in bagian[1:] if b)
    return f"{bagian[0]} {s}" + (f", doi: {k['doi']}." if k["doi"] else ".")


GAYA = {"apa": apa, "ieee": ieee, "bib": bibtex}

# --- keterpakaian istilah ---

BIDANG = {  # nama bidang -> id field OpenAlex
    "teknik": 22, "elektro": 22, "mesin": 22, "sipil": 22, "informatika": 17, "komputer": 17, "kedokteran": 27,
    "kesehatan": 27, "keperawatan": 29, "farmasi": 30, "kedokteran-gigi": 35, "profesi-kesehatan": 36, "sosial": 33,
    "pendidikan": 33, "hukum": 33, "ekonomi": 20, "manajemen": 14, "bisnis": 14, "akuntansi": 14, "psikologi": 32,
    "pertanian": 11, "biologi": 11, "lingkungan": 23, "kimia": 16, "teknik-kimia": 15, "fisika": 31,
    "matematika": 26, "statistik": 26, "energi": 21, "material": 25, "humaniora": 12, "sejarah": 12,
    "kebumian": 19, "veteriner": 34, "biokimia": 13, "mikrobiologi": 24, "keputusan": 18, "neurosains": 28,
}
MIN_DATA = 20


def putusan(hitung):
    """hitung: {istilah: (n_judul, n_judul_abstrak)}. Kembalikan (dasar, {istilah: pangsa}, kalimat putusan)."""
    for i, dasar in ((0, "judul"), (1, "judul+abstrak")):
        total = sum(h[i] for h in hitung.values())
        if total >= MIN_DATA:
            pangsa = {t: h[i] / total for t, h in hitung.items()}
            break
    else:
        return None, {}, (f"Data kurang (< {MIN_DATA} karya). Ikuti gaya selingkung atau pilihan penulis; "
                          "jangan mengganti istilah berdasarkan data ini.")
    utama = max(pangsa, key=pangsa.get)
    catatan = " Abstrak sering berbahasa Inggris, jadi bentuk Inggris terhitung lebih." if dasar != "judul" else ""
    if pangsa[utama] >= 0.6:
        i = 0 if dasar == "judul" else 1
        mati = [t for t, v in pangsa.items() if v < 0.05 and hitung[t][i] < 10]
        jarang = [t for t, v in pangsa.items() if v < 0.25 and t not in mati]
        kal = f"\"{utama}\" dominan ({pangsa[utama]:.0%} {dasar}). Untuk teks baru, pakai bentuk ini."
        if jarang:
            kal += f" {', '.join(jarang)} jarang tetapi masih dipakai: pada suntingan, pertahankan pilihan penulis."
        if mati:
            kal += f" {', '.join(mati)} hampir tidak dipakai: pada suntingan, sarankan bentuk dominan (jangan langsung ganti)."
    else:
        kal = (f"Bersaing: tidak ada bentuk yang mencapai 60% ({dasar}). Keduanya hidup; pertahankan pilihan penulis "
               "dan sebut bentuk lain dalam kurung pada kemunculan pertama.")
    return dasar, pangsa, kal + catatan


# --- perintah ---

def main(a):
    def opt(name, default=None):
        if name in a:
            i = a.index(name); v = a[i + 1] if i + 1 < len(a) else ""; del a[i:i + 2]; return v
        return default
    flag = lambda n: (a.remove(n) or True) if n in a else False

    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return 0
    cmd, a = a[0], a[1:]
    n = opt("--n", "10")
    if cmd == "cari":
        tahun, urut, oa = opt("--tahun"), opt("--urut"), flag("--oa")
        filt = [f"publication_year:{tahun}"] if tahun else []
        if oa:
            filt.append("is_oa:true")
        r = get(f"{API}/works", search=" ".join(a), per_page=n, select=FIELDS, filter=",".join(filt),
                sort="cited_by_count:desc" if urut == "sitasi" else None)
        print(f"{r['meta']['count']} hasil")
        for w in r["results"]:
            print(ringkas(dari_openalex(w)))
        return 0
    if cmd in ("doi", "bib", "rujukan"):
        gaya = opt("--gaya", "bib" if cmd == "bib" else "apa")
        if gaya not in GAYA or not a:
            print(f"pemakaian: {cmd} <DOI|id> ... [--gaya apa|ieee|bib]"); return 2
        kode = 0
        for ident in a:
            k = ambil(ident)
            if not k:
                print(f"TIDAK DITEMUKAN: {ident}"); kode = 1
            elif cmd == "doi":
                print(ringkas(k) + "\n  " + (k["abstrak"] or "(abstrak tidak tersedia)"))
            else:
                print(GAYA[gaya](k), end="\n\n" if gaya == "bib" else "\n")
                if penulis_rusak(k):
                    print(("% " if gaya == "bib" else "") + PERINGATAN_PENULIS)
        return kode
    if cmd == "cek":
        doi, tahun = opt("--doi"), opt("--tahun")
        penulis = [p for p in (opt("--penulis") or "").split(",") if p.strip()]
        judul = " ".join(a)
        if not judul and not doi:
            print("pemakaian: cek \"judul\" [--doi …] [--penulis \"A, B\"] [--tahun 2021]"); return 2
        if doi:
            k = ambil(doi)
            if not k:
                print(f"TIDAK ADA: doi {doi} tidak dikenal OpenAlex maupun Crossref"); return 1
            alasan = cocokkan(k, judul, penulis, tahun, ambang=0.85)
        else:
            calon = cari_judul(judul, lambda c: not cocokkan(c, judul, penulis, tahun))
            if not calon:
                print("TIDAK DITEMUKAN di OpenAlex maupun Crossref: jangan dikutip sebelum dicek manual"); return 1
            # urutan: cocok penuh, lalu paling sedikit alasan, lalu judul paling mirip
            k = min(calon, key=lambda c: (len(cocokkan(c, judul, penulis, tahun)), -mirip(judul, c["judul"])))
            alasan = cocokkan(k, judul, penulis, tahun)
        catatan = f" (catatan: tahun terbit {k['tahun']}, rujukan menulis {tahun})" if tahun and k["tahun"] and int(tahun) != k["tahun"] else ""
        if not alasan:
            print("COCOK" + catatan)
        else:
            print("TIDAK PASTI: " + "; ".join(alasan) + ". Jangan dikutip sebelum dicek manual.")
            if all(x.startswith("tahun") for x in alasan):
                print("Judul dan penulis cocok; tahun di basis data bisa salah (praterbit, terbit ulang). Cek di laman penerbit.")
        print(ringkas(k))
        if penulis_rusak(k):
            print(PERINGATAN_PENULIS)
        return 0 if not alasan else 1
    if cmd == "daftar":
        if not a:
            print("pemakaian: daftar <berkas>  (satu entri per baris; - untuk stdin)"); return 2
        teks = sys.stdin.read() if a[0] == "-" else open(a[0], encoding="utf-8").read()
        entri = [re.sub(r"^\s*(?:\[\d+\]|\d+[.)]|[-*])\s*", "", b).strip() for b in teks.splitlines()]
        entri = [e for e in entri if len(e) >= 30]
        hitung = {"OK": 0, "RAGU": 0, "TIDAK DITEMUKAN": 0, "GALAT": 0}
        for i, e in enumerate(entri, 1):
            try:
                calon = calon_entri(e)
            except GalatJaringan as g:
                calon, status, ket = None, "GALAT", f"\n    {g}; ulangi nanti"
            if calon is None:
                pass
            elif not calon:
                status, ket = "TIDAK DITEMUKAN", ""
            else:
                k = min(calon, key=lambda c: (len(nilai_entri(e, c)), -cakupan(c["judul"], e)))
                alasan = nilai_entri(e, k)
                status = "OK" if not alasan else "RAGU"
                ket = f"\n    -> {apa(k)}" + (f"\n    {'; '.join(alasan)}" if alasan else "")
                ket += f"\n    {PERINGATAN_PENULIS}" if penulis_rusak(k) else ""
            hitung[status] += 1
            print(f"[{i}] {status}: {e[:90]}{'…' if len(e) > 90 else ''}{ket}")
        print(f"\n{len(entri)} entri: " + ", ".join(f"{v} {s}" for s, v in hitung.items() if v))
        print("RAGU dan TIDAK DITEMUKAN bukan bukti rujukan palsu: jurnal tanpa DOI sering tidak terindeks. Cek di laman jurnal atau Garuda.")
        return 0 if hitung["OK"] == len(entri) else 1
    if cmd == "istilah":
        bidang, tahun = opt("--bidang"), opt("--tahun", "2019-2026")
        if len(a) < 2 or (bidang and not bidang.isdigit() and bidang not in BIDANG):
            print("pemakaian: istilah \"bentuk 1\" \"bentuk 2\" ... [--bidang " + "|".join(sorted(set(BIDANG))) + "] [--tahun 2019-2026]")
            return 2
        dasar_f = f"language:id,publication_year:{tahun}"
        if bidang:
            dasar_f += f",primary_topic.field.id:{bidang if bidang.isdigit() else BIDANG[bidang]}"
        hitung = {}
        for t in a:
            frasa = '"' + t.replace('"', "") + '"'
            hitung[t] = tuple(get(f"{API}/works", filter=f"{dasar_f},{kol}.search:{frasa}", per_page=1, select="id")["meta"]["count"]
                              for kol in ("title", "title_and_abstract"))
        dasar, pangsa, kal = putusan(hitung)
        print(f"Karya berbahasa Indonesia di OpenAlex, {tahun}" + (f", bidang {bidang}" if bidang else "") + ":")
        print(f"  {'istilah':28} {'judul':>7} {'judul+abstrak':>14} {'pangsa':>7}")
        for t, (nj, na) in hitung.items():
            print(f"  {t:28} {nj:>7} {na:>14} {pangsa.get(t, 0):>7.0%}")
        print("Putusan: " + kal)
        print("Gaya selingkung jurnal sasaran tetap didahulukan. Kriteria lain: references/istilah.md.")
        return 0
    if cmd == "dikutip":
        if not a:
            print("pemakaian: dikutip <DOI|id>"); return 2
        k = ambil(a[0])
        if not k or not k["id"]:
            print(f"TIDAK DITEMUKAN di OpenAlex: {a[0]}"); return 1
        r = get(f"{API}/works", filter=f"cites:{k['id']}", per_page=n, select=FIELDS, sort="cited_by_count:desc")
        print(f"{r['meta']['count']} karya mengutip {k['id']}")
        for w in r["results"]:
            print(ringkas(dari_openalex(w)))
        return 0
    print(f"perintah tak dikenal: {cmd}\n{__doc__}")
    return 2


def tes():
    oa = dari_openalex({
        "id": "https://openalex.org/W1", "doi": "https://doi.org/10.1/x", "title": "Deep learning for speed",
        "publication_year": 2021, "type": "article", "cited_by_count": 3,
        "authorships": [{"author": {"display_name": "Budi Santoso"}}, {"author": {"display_name": "Citra Ayu Dewi"}}],
        "primary_location": {"source": {"display_name": "IEEE Access"}},
        "biblio": {"volume": "9", "issue": "2", "first_page": "1", "last_page": "9"},
        "abstract_inverted_index": {"world": [1], "hello": [0]}})
    assert oa["abstrak"] == "hello world" and oa["doi"] == "10.1/x" and oa["id"] == "W1", oa
    b = bibtex(oa)
    assert b.startswith("@article{santoso2021deep,") and "pages = {1--9}" in b and "doi = {10.1/x}" in b, b
    assert apa(oa) == "Santoso, B., & Dewi, C. A. (2021). Deep learning for speed. *IEEE Access*, *9*(2), 1–9. https://doi.org/10.1/x", apa(oa)
    assert ieee(oa) == 'B. Santoso dan C. A. Dewi, "Deep learning for speed," *IEEE Access*, vol. 9, no. 2, hlm. 1–9, 2021, doi: 10.1/x.', ieee(oa)
    cr = dari_crossref({"DOI": "10.33/ska.1", "title": ["Pola  asuh dan stunting"], "type": "journal-article",
                        "published": {"date-parts": [[2020, 5]]}, "author": [{"given": "Sri", "family": "Wahyuni"}],
                        "container-title": ["Jurnal Kesehatan"], "volume": "4", "page": "10–20",
                        "abstract": "<jats:p>Isi.</jats:p>"})
    assert (cr["judul"], cr["tahun"], cr["hal"], cr["abstrak"]) == ("Pola asuh dan stunting", 2020, ["10", "20"], "Isi."), cr
    assert apa(cr) == "Wahyuni, S. (2020). Pola asuh dan stunting. *Jurnal Kesehatan*, *4*, 10–20. https://doi.org/10.33/ska.1", apa(cr)
    assert apa(dict(cr, penulis=["Sugiyono"])).startswith("Sugiyono (2020).")
    # cek: judul, penulis, tahun
    assert cocokkan(oa, "Deep Learning for Speed.", ["Santoso"], "2021") == []
    assert cocokkan(oa, "Deep learning for speed", [], "2022") == []  # selisih 1 tahun: terbit daring lebih dulu
    assert cocokkan(oa, "Deep learning for speed", ["Wibowo"], "2018") == ["penulis Wibowo tidak ada", "tahun 2018 ≠ 2021"]
    assert cocokkan(oa, "Machine learning in agriculture")[0].startswith("judul beda")
    assert cocokkan(cr, "Pola asuh dan stunting", ["Wahyuni"]) == []
    # daftar: entri dinilai terhadap metadata
    baris = "Santoso, B., & Dewi, C. A. (2021). Deep learning for speed. IEEE Access, 9(2), 1-9."
    assert nilai_entri(baris, oa) == []
    assert nilai_entri(baris.replace("Santoso", "Wibowo").replace("2021", "2015"), oa) == [
        "penulis pertama Budi Santoso tidak disebut", "tahun 2021 tidak disebut"]
    assert nilai_entri("Santoso (2021). Machine vision for rice grading. Jurnal X.", oa)[0].startswith("judul tidak cocok")
    assert tebak_judul("Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. arXiv preprint.") \
        == "Adam: A method for stochastic optimization"
    assert tebak_judul('[4] D. Kingma, "Adam: A method for stochastic optimization," arXiv, 2014.') \
        == "Adam: A method for stochastic optimization"
    assert apa(dict(cr, penulis=[])).startswith("Pola asuh dan stunting. (2020).")
    assert not penulis_rusak(oa) and not penulis_rusak(cr)
    assert penulis_rusak(dict(cr, penulis=["P. P. S. P. S. S. P. U. A. P. Indonesia"]))
    assert penulis_rusak(dict(cr, penulis=["Jurusan Gizi Fakultas Kesehatan"]))
    # istilah: ambang 60%, data kurang, cadangan judul+abstrak
    assert putusan({"catu daya": (84, 397), "power supply": (54, 516)})[2].startswith('"catu daya" dominan (61% judul)')
    d, pg, kal = putusan({"stunting": (8027, 10185), "tengkes": (6, 17)})
    assert d == "judul" and kal.startswith('"stunting" dominan') and "tengkes hampir tidak dipakai" in kal, kal
    assert "pembelajaran mesin jarang tetapi masih dipakai" in putusan({"pembelajaran mesin": (49, 399), "machine learning": (561, 1834)})[2]
    assert putusan({"filter kalman": (15, 25), "tapis kalman": (4, 4), "penapis kalman": (0, 0)})[2].startswith('"filter kalman" dominan')
    assert putusan({"a": (50, 0), "b": (45, 0)})[2].startswith("Bersaing")
    assert putusan({"a": (3, 30), "b": (2, 10)})[0] == "judul+abstrak"
    assert putusan({"a": (1, 2), "b": (0, 3)})[0] is None
    assert norm("Analisis Ćevapi—Uji") == "analisis cevapi uji"
    print("ok")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    if sys.argv[1:] == ["--tes"]:
        tes()
    else:
        try:
            sys.exit(main(sys.argv[1:]))
        except GalatJaringan as e:
            print(f"Galat jaringan: {e}", file=sys.stderr)
            sys.exit(2)
