# Alat riset pendamping

Skill ini bekerja tanpa alat apa pun, tetapi rujukan hanya bisa dicari dan dicek bila ada alat
pencarian. Berkas ini dipakai agen untuk menawarkan penyambungan alat kepada pengguna, dan
dipakai pengguna untuk menyambungkannya sendiri.

| Alat | Gunanya | Akun | Cara tersedia |
| --- | --- | --- | --- |
| OpenAlex dan Crossref | cari karya, abstrak, entri APA/IEEE/BibTeX, cek satu rujukan atau seluruh daftar pustaka, siapa yang mengutip | tidak perlu; kunci API OpenAlex gratis dianjurkan | `scripts/openalex.py`, ikut terpasang bersama skill |
| Consensus | sintesis temuan: "apa kata riset tentang X" | akun Consensus | server MCP |
| alphaXiv | praterbit arXiv beserta ringkasan | akun alphaXiv | server MCP |
| PubMed | literatur kesehatan dan biomedis | tidak perlu | konektor claude.ai |

## OpenAlex dan Crossref (selalu tersedia)

```bash
python scripts/openalex.py cari "stunting pola asuh" --tahun 2020-2026
python scripts/openalex.py cek "Judul persis artikel" --penulis "Santoso, Dewi" --tahun 2021
python scripts/openalex.py daftar pustaka.txt
python scripts/openalex.py doi 10.33007/ska.v14i2.3525
python scripts/openalex.py rujukan 10.33007/ska.v14i2.3525 --gaya apa
python scripts/openalex.py bib 10.33007/ska.v14i2.3525
python scripts/openalex.py dikutip 10.33007/ska.v14i2.3525
python scripts/openalex.py istilah "catu daya" "power supply" --bidang teknik
```

Jalankan dari folder skill (misalnya `.agents/skills/naskah-id` atau `.claude/skills/naskah-id`).
Hanya butuh Python 3.7 atau lebih baru. Tanpa kunci API, kuota
harian OpenAlex kecil; bila muncul galat kuota, buat kunci gratis di
https://openalex.org/settings/api lalu simpan sebagai variabel lingkungan `OPENALEX_API_KEY`:

```bash
setx OPENALEX_API_KEY "<kunci>"            # Windows; buka terminal baru sesudahnya
export OPENALEX_API_KEY="<kunci>"          # macOS/Linux; tambahkan ke ~/.bashrc atau ~/.zshrc
```

Karya yang tidak ada di OpenAlex dicari di Crossref, tempat sebagian besar jurnal SINTA ber-DOI
terdaftar. Galat kuota (HTTP 429) dicoba ulang otomatis.

- `cek` keluar dengan kode 0 bila judul, penulis, dan tahun yang diberikan cocok, dan 1 bila
  meragukan. Selisih tahun satu dianggap cocok (terbit daring lebih dulu) dan diberi catatan.
- `daftar` membaca satu entri per baris (nomor `[1]` atau `1.` boleh ada) dan memberi OK, RAGU,
  atau TIDAK DITEMUKAN per entri, lengkap dengan metadata yang ditemukan. RAGU berarti ada karya
  yang mirip tetapi judul, penulis pertama, atau tahunnya tidak sesuai: tanda khas rujukan
  karangan, tetapi juga bisa salah ketik.
- `rujukan` mencetak entri APA 7 atau IEEE (gaya naskah Indonesia: *dkk.*, *hlm.*). Huruf miring
  ditandai `*…*`. Bila metadata penulis memuat nama kampus atau deretan inisial, keluar
  `PERINGATAN: metadata penulis`; sebagian jurnal OJS mengirim afiliasi sebagai nama penulis.

- `istilah` menghitung karya berbahasa Indonesia yang memakai tiap bentuk istilah di judul dan
  abstraknya, lalu memberi putusan dominan, bersaing, atau data kurang. Parameter dan batasnya
  ada di `references/istilah.md`.

Kueri bahasa Inggris memberi hasil terbanyak; ulangi dengan kueri bahasa Indonesia untuk
jurnal lokal. Jurnal tanpa DOI sering tidak terindeks; cek di laman OJS jurnalnya atau di
Garuda (https://garuda.kemdiktisaintek.go.id/).

## Consensus dan alphaXiv

**Claude Code, dipasang sebagai plugin:** kedua server sudah tercantum di `.mcp.json` plugin ini
dan ikut terpasang. Ketik `/mcp`, pilih servernya, lalu masuk dengan akun masing-masing.

**Claude Code, dipasang lewat `npx skills` atau disalin manual:**

```bash
claude mcp add --transport http --scope user consensus https://mcp.consensus.app/mcp
claude mcp add --transport http --scope user alphaxiv https://api.alphaxiv.org/mcp/v1
```

Lalu ketik `/mcp` di sesi Claude Code untuk masuk.

**Codex:**

```bash
codex mcp add consensus --url https://mcp.consensus.app/mcp
codex mcp add alphaxiv --url https://api.alphaxiv.org/mcp/v1
codex mcp login consensus
codex mcp login alphaxiv
```

**claude.ai dan Claude Desktop:** buka pengaturan konektor, cari Consensus dan alphaXiv di
direktori konektor, lalu sambungkan. Bila tidak ada di direktori, tambahkan sebagai konektor
kustom dengan URL di atas.

### Agen lain

Konfigurasi di bawah mengikuti format yang didokumentasikan tiap agen, tetapi **belum diuji**
oleh pengelola repo. Bila agen menolak, cek dokumentasi terbarunya: nama kolom URL berbeda-beda
antaragen. Setelah server ditambahkan, login dilakukan lewat menu MCP agen itu.

**Cursor**: `~/.cursor/mcp.json` (semua proyek) atau `.cursor/mcp.json` (satu proyek):

```json
{
  "mcpServers": {
    "consensus": { "url": "https://mcp.consensus.app/mcp" },
    "alphaxiv": { "url": "https://api.alphaxiv.org/mcp/v1" }
  }
}
```

**Gemini CLI**: `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "consensus": { "httpUrl": "https://mcp.consensus.app/mcp" },
    "alphaxiv": { "httpUrl": "https://api.alphaxiv.org/mcp/v1" }
  }
}
```

**GitHub Copilot di VS Code**: `.vscode/mcp.json`:

```json
{
  "servers": {
    "consensus": { "type": "http", "url": "https://mcp.consensus.app/mcp" },
    "alphaxiv": { "type": "http", "url": "https://api.alphaxiv.org/mcp/v1" }
  }
}
```

**Windsurf**: `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "consensus": { "serverUrl": "https://mcp.consensus.app/mcp" },
    "alphaxiv": { "serverUrl": "https://api.alphaxiv.org/mcp/v1" }
  }
}
```

**OpenCode**: `opencode.json` di proyek atau `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "consensus": { "type": "remote", "url": "https://mcp.consensus.app/mcp" },
    "alphaxiv": { "type": "remote", "url": "https://api.alphaxiv.org/mcp/v1" }
  }
}
```

Bila berkas konfigurasi itu sudah ada, gabungkan entrinya; jangan menimpa seluruh berkas.

## PubMed

Di claude.ai dan Claude Desktop, aktifkan konektor PubMed dari direktori konektor. Untuk agen
lain, pakai OpenAlex: sebagian besar artikel yang terindeks PubMed juga ada di OpenAlex.

## Untuk agen: kapan menawarkan penyambungan

- Tawarkan hanya saat pekerjaan memang butuh rujukan: menulis tinjauan pustaka, latar
  belakang, pembahasan, atau mengecek daftar pustaka. Jangan menawarkan saat pengguna hanya
  meminta koreksi ejaan.
- Tawarkan sekali per sesi. Sebutkan alat yang belum tersedia, satu kalimat tentang gunanya,
  dan perintah atau potongan konfigurasi yang sesuai dengan agen yang sedang dipakai. Jangan
  menjalankan perintah pemasangan atau mengubah berkas konfigurasi tanpa persetujuan pengguna.
- Bila pengguna setuju dan agen bisa menjalankan perintah, pasang dengan perintah resmi agen
  itu (`claude mcp add`, `codex mcp add`). Untuk agen yang memakai berkas konfigurasi, baca dulu
  berkasnya lalu tambahkan entri tanpa menghapus server lain.
- Bila pengguna menolak atau belum sempat, lanjutkan dengan `scripts/openalex.py`. Bila Python
  juga tidak tersedia, pakai penanda `[PERLU RUJUKAN: …]`.
- Login akun dilakukan pengguna sendiri. Agen tidak meminta atau menyimpan kata sandi.
