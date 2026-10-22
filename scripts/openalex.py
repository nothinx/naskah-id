"""OpenAlex CLI: cari, verifikasi, dan kutip karya ilmiah (stdlib saja).

  python scripts/openalex.py cari "vehicle speedometer calibration" [--tahun 2018-2026] [--n 10] [--oa] [--urut sitasi]
  python scripts/openalex.py doi 10.1109/ACCESS.2020.2970143        # detail + abstrak
  python scripts/openalex.py bib 10.1109/xxx W2741809807 ...         # BibTeX (DOI atau id OpenAlex)
  python scripts/openalex.py cek "Judul persis paper" [--doi 10.x]  # verifikasi sitasi: ada / tidak
  python scripts/openalex.py dikutip W2741809807 [--n 10]            # karya yang mengutip
  python scripts/openalex.py --tes

Tanpa kunci, kuota harian OpenAlex kecil. Kunci API gratis: https://openalex.org/settings/api
  Windows:      setx OPENALEX_API_KEY "<kunci>"   (buka terminal baru setelahnya)
  macOS/Linux:  export OPENALEX_API_KEY="<kunci>"  (tambahkan ke ~/.bashrc atau ~/.zshrc)
"""
import json, os, re, sys, urllib.error, urllib.parse, urllib.request
from difflib import SequenceMatcher

API = "https://api.openalex.org"
KEY = os.environ.get("OPENALEX_API_KEY", "")
sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
FIELDS = "id,doi,title,publication_year,authorships,primary_location,cited_by_count,open_access,type,biblio,abstract_inverted_index"


def get(path, **q):
    q = {k: v for k, v in q.items() if v not in (None, "")}
    if KEY:
        q["api_key"] = KEY
    url = f"{API}{path}?{urllib.parse.urlencode(q)}"
    req = urllib.request.Request(url, headers={"User-Agent": "naskah-id/0.1 (+https://github.com/nothinx/naskah-id)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        hint = "" if KEY else " (OPENALEX_API_KEY belum diset; kuota tanpa kunci kecil)"
        sys.exit(f"OpenAlex HTTP {e.code}: {e.read()[:200].decode(errors='replace')}{hint}")


def work_path(ident):
    ident = ident.strip()
    if re.match(r"^W\d+$", ident, re.I):
        return f"/works/{ident.upper()}"
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", ident, flags=re.I)
    return f"/works/doi:{doi}"


def abstrak(inv):
    if not inv:
        return ""
    pos = sorted((i, w) for w, idx in inv.items() for i in idx)
    return " ".join(w for _, w in pos)


def penulis(w, maks=None):
    names = [a["author"]["display_name"] for a in w.get("authorships") or []]
    if maks and len(names) > maks:
        return ", ".join(names[:maks]) + " et al."
    return ", ".join(names)


def venue(w):
    src = ((w.get("primary_location") or {}).get("source") or {})
    return src.get("display_name") or ""


def ringkas(w):
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    oa = " [OA]" if (w.get("open_access") or {}).get("is_oa") else ""
    return (f"- {w.get('title')} ({w.get('publication_year')})\n"
            f"  {penulis(w, 3)} — {venue(w)}\n"
            f"  doi:{doi or '-'}  id:{w['id'].rsplit('/', 1)[-1]}  sitasi:{w.get('cited_by_count', 0)}{oa}")


def bibtex(w):
    authors = [a["author"]["display_name"] for a in w.get("authorships") or []]
    first = re.sub(r"\W", "", (authors[0].split()[-1] if authors else "anon")).lower()
    word = next((t for t in re.findall(r"[a-z]+", (w.get("title") or "").lower()) if len(t) > 3), "x")
    year = w.get("publication_year") or ""
    kind = {"article": "article", "book": "book", "book-chapter": "incollection",
            "dissertation": "phdthesis"}.get(w.get("type"), "misc")
    if kind == "article" and any(k in venue(w).lower() for k in ("conference", "proceedings")):
        kind = "inproceedings"
    b = w.get("biblio") or {}
    pages = "--".join(p for p in (b.get("first_page"), b.get("last_page")) if p)
    f = {"title": "{" + (w.get("title") or "") + "}", "author": " and ".join(authors), "year": year,
         ("booktitle" if kind in ("inproceedings", "incollection") else "journal"): venue(w),
         "volume": b.get("volume"), "number": b.get("issue"), "pages": pages,
         "doi": (w.get("doi") or "").replace("https://doi.org/", "")}
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in f.items() if v)
    return f"@{kind}{{{first}{year}{word},\n{body}\n}}"


def main(a):
    def opt(name, default=None):
        if name in a:
            i = a.index(name); v = a[i + 1] if i + 1 < len(a) else ""; del a[i:i + 2]; return v
        return default
    flag = lambda n: (a.remove(n) or True) if n in a else False

    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    cmd, a = a[0], a[1:]
    n = opt("--n", "10")
    if cmd == "cari":
        tahun, urut, oa = opt("--tahun"), opt("--urut"), flag("--oa")
        filt = [f"publication_year:{tahun}"] if tahun else []
        if oa:
            filt.append("is_oa:true")
        r = get("/works", search=" ".join(a), per_page=n, select=FIELDS, filter=",".join(filt),
                sort="cited_by_count:desc" if urut == "sitasi" else None)
        print(f"{r['meta']['count']} hasil")
        for w in r["results"]:
            print(ringkas(w))
    elif cmd == "doi":
        for ident in a:
            w = get(work_path(ident), select=FIELDS)
            print(ringkas(w) + "\n  " + (abstrak(w.get("abstract_inverted_index")) or "(abstrak tidak tersedia)") if w else f"TIDAK DITEMUKAN: {ident}")
    elif cmd == "bib":
        for ident in a:
            w = get(work_path(ident), select=FIELDS)
            print(bibtex(w) if w else f"% TIDAK DITEMUKAN: {ident}", end="\n\n")
    elif cmd == "cek":
        doi, judul = opt("--doi"), " ".join(a)
        if doi:
            w = get(work_path(doi), select=FIELDS)
            if not w:
                print(f"TIDAK ADA: doi {doi} tidak dikenal OpenAlex"); sys.exit(1)
            s = SequenceMatcher(None, judul.lower(), (w["title"] or "").lower()).ratio() if judul else 1
            print(("COCOK" if s > 0.85 else f"DOI ADA, JUDUL BEDA (kemiripan {s:.2f})") + "\n" + ringkas(w))
            sys.exit(0 if s > 0.85 else 1)
        r = get("/works", search=judul, per_page=5, select=FIELDS)
        best = max(r["results"], key=lambda w: SequenceMatcher(None, judul.lower(), (w["title"] or "").lower()).ratio(), default=None)
        s = SequenceMatcher(None, judul.lower(), (best["title"] or "").lower()).ratio() if best else 0
        print(("COCOK" if s > 0.9 else f"TIDAK PASTI (kemiripan terbaik {s:.2f}): jangan dikutip sebelum dicek manual")
              + ("\n" + ringkas(best) if best else ""))
        sys.exit(0 if s > 0.9 else 1)
    elif cmd == "dikutip":
        wid = work_path(a[0]).rsplit("/", 1)[-1]
        if not wid.startswith("W"):
            wid = get(work_path(a[0]), select="id")["id"].rsplit("/", 1)[-1]
        r = get("/works", filter=f"cites:{wid}", per_page=n, select=FIELDS, sort="cited_by_count:desc")
        print(f"{r['meta']['count']} karya mengutip {wid}")
        for w in r["results"]:
            print(ringkas(w))
    else:
        sys.exit(f"perintah tak dikenal: {cmd}\n{__doc__}")


def tes():
    assert abstrak({"world": [1], "hello": [0], "again": [2]}) == "hello world again"
    assert work_path("w123") == "/works/W123"
    assert work_path("https://doi.org/10.1/ab") == "/works/doi:10.1/ab"
    w = {"title": "Deep learning for speed", "publication_year": 2021, "type": "article",
         "authorships": [{"author": {"display_name": "Budi Santoso"}}],
         "primary_location": {"source": {"display_name": "IEEE Access"}},
         "biblio": {"volume": "9", "first_page": "1", "last_page": "9"}, "doi": "https://doi.org/10.1/x"}
    b = bibtex(w)
    assert b.startswith("@article{santoso2021deep,") and "pages = {1--9}" in b and "doi = {10.1/x}" in b, b
    print("ok")


if __name__ == "__main__":
    tes() if sys.argv[1:] == ["--tes"] else main(sys.argv[1:])
