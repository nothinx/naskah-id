# naskah-id

[![GitHub stars](https://img.shields.io/github/stars/nothinx/naskah-id?style=flat&logo=github)](https://github.com/nothinx/naskah-id/stargazers)
[![Versi](https://img.shields.io/github/v/tag/nothinx/naskah-id?label=versi)](CHANGELOG.md)
[![Lisensi: MIT](https://img.shields.io/badge/lisensi-MIT-blue)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-npx%20skills%20add-black)](#pemasangan)

Skill agen AI untuk menulis dan menyunting karya ilmiah berbahasa Indonesia: artikel jurnal,
skripsi, tesis, proposal hibah, dan laporan penelitian. Ejaan dan kata mengikuti EYD V dan
KBBI. Angka, hasil, dan sitasi Anda tidak diubah.

README ini juga disunting dengan skill ini. Catatan lengkapnya, termasuk lima kesalahan yang
ditemukan di versi sebelumnya, ada di [contoh/readme-ini.md](contoh/readme-ini.md).

## Lima tanda terkuat

Kelima tanda ini sering membuat naskah Indonesia terasa ditulis mesin atau diterjemahkan kata
per kata. Penulis manusia juga memakainya, jadi anggap ini kebiasaan yang perlu diperbaiki,
bukan bukti. Pada setiap contoh, versi kedua hanya memakai fakta yang sudah ada di versi
pertama.

**1. Pembuka kosmik**

<!-- periksa:abaikan -->
> Di era digital ini, tidak dapat dipungkiri bahwa Puskesmas di Kabupaten X masih mencatat kunjungan ibu hamil di buku register.
<!-- periksa:lanjut -->

> Puskesmas di Kabupaten X masih mencatat kunjungan ibu hamil di buku register.

**2. Subjek hilang karena kata depan**

<!-- periksa:abaikan -->
> Dari hasil analisis menunjukkan bahwa kepuasan pasien rendah.
<!-- periksa:lanjut -->

> Hasil analisis menunjukkan bahwa kepuasan pasien rendah.

**3. Perangkai tiruan bahasa Inggris**

<!-- periksa:abaikan -->
> Penelitian dilakukan di Desa Sukamaju di mana kelompok tani memainkan peran penting dalam distribusi pupuk.
<!-- periksa:lanjut -->

> Penelitian dilakukan di Desa Sukamaju, tempat kelompok tani berperan penting dalam distribusi pupuk.

**4. "Hal ini" dan penghubung yang sama di setiap paragraf**

<!-- periksa:abaikan -->
> Kadar hemoglobin responden rendah. Hal ini menunjukkan bahwa asupan zat besi kurang. Selain itu, …
<!-- periksa:lanjut -->

> Kadar hemoglobin responden rendah. Kadar serendah ini menunjukkan bahwa asupan zat besi kurang.

**5. Klaim digelembungkan**

<!-- periksa:abaikan -->
> Rerata skor naik dari 61,2 menjadi 74,5 dengan peningkatan yang sangat signifikan (p < 0,001) sehingga model ini merupakan solusi yang inovatif.
<!-- periksa:lanjut -->

> Rerata skor naik dari 61,2 menjadi 74,5 (*p* < 0,001).

Klaim `solusi yang inovatif` dibuang karena tidak ada data yang mendukungnya. Bila sebuah
kalimat butuh angka yang belum Anda berikan, skill menulis `[PERLU DATA: …]` dan tidak
mengarang angka.

## Apa ini dan apa yang bukan

Skill ini memperbaiki ejaan dan kalimat, menyusun bagian naskah dari bahan yang Anda berikan,
dan menandai klaim yang belum didukung rujukan.

Skill ini tidak dibuat untuk mengakali Turnitin atau detektor AI. Skill ini juga bukan
detektor AI. Gaya bahasa tidak bisa menunjukkan apakah sebuah tulisan dibuat oleh manusia
atau AI, jadi hasilnya jangan dijadikan bukti bahwa seorang mahasiswa memakai AI.

Agen yang memakai skill ini terikat [kontrak tanggung jawab](KONTRAK.md):

- tidak mengarang data, hasil, kutipan, atau rujukan;
- tidak mengubah angka, hasil, atau sitasi saat menyunting;
- tidak menulis ulang bila Anda hanya meminta koreksi;
- menolak perjokian skripsi dan permintaan menyamarkan hasil AI;
- menyusun draf pernyataan penggunaan AI sesuai format jurnal atau kampus Anda.

Bila tidak ada rujukan yang terverifikasi, agen menulis `[PERLU RUJUKAN: …]`. Penanda itu
memang tidak enak dilihat, tetapi jauh lebih aman daripada rujukan yang tampak meyakinkan dan
ternyata tidak ada.

## Pemasangan

### Lewat `npx skills` (cara utama, untuk semua agen)

Butuh Node.js 18 atau lebih baru. Satu perintah ini bekerja untuk Claude Code, Codex, Cursor,
Gemini CLI, GitHub Copilot, Windsurf, OpenCode, Cline, Kiro, Antigravity, dan puluhan agen
lain yang mendukung format Agent Skills.

```bash
npx skills add nothinx/naskah-id        # untuk proyek di folder ini saja
npx skills add nothinx/naskah-id -g     # untuk semua proyek
```

Tanpa opsi tambahan, perintah ini menanyakan agen mana yang dipasangi. Untuk langsung memilih
agen, tambahkan `-a` diikuti nama agen, dipisah spasi:

| Agen | Nama untuk `-a` | Lokasi skill di proyek |
| --- | --- | --- |
| Claude Code | `claude-code` | `.claude/skills/naskah-id` |
| Codex | `codex` | `.agents/skills/naskah-id` |
| Cursor | `cursor` | `.agents/skills/naskah-id` |
| Gemini CLI | `gemini-cli` | `.agents/skills/naskah-id` |
| GitHub Copilot | `github-copilot` | `.agents/skills/naskah-id` |
| OpenCode | `opencode` | `.agents/skills/naskah-id` |
| Cline | `cline` | `.agents/skills/naskah-id` |
| Antigravity | `antigravity` | `.agents/skills/naskah-id` |
| Windsurf | `windsurf` | `.windsurf/skills/naskah-id` |
| Kiro | `kiro-cli` | `.kiro/skills/naskah-id` |

```bash
npx skills add nothinx/naskah-id -a claude-code codex cursor gemini-cli github-copilot -y
```

Lokasi di tabel adalah hasil pemasangan tingkat proyek yang diuji pada 22 Oktober 2026. Daftar
lengkap nama agen muncul bila `-a` diberi nama yang tidak dikenal. Untuk memperbarui:
`npx skills update naskah-id`.

### Claude Code sebagai plugin

Ketik di dalam sesi Claude Code:

```
/plugin marketplace add nothinx/naskah-id
/plugin install naskah-id@naskah-id
```

Untuk memperbarui: `/plugin marketplace update naskah-id`.

### Salin manual (Codex dan agen lain)

```bash
git clone https://github.com/nothinx/naskah-id.git ~/.codex/skills/naskah-id
```

Ganti `~/.codex/skills` dengan folder skill agen Anda, misalnya `~/.claude/skills` untuk
Claude Code atau `~/.agents/skills`, folder bersama yang dibaca Codex, Gemini CLI, GitHub
Copilot, dan agen lain yang mengikuti format Agent Skills. Di Windows, `~` berarti folder pengguna
(`C:\Users\<nama-pengguna>`). Berkas `agents/openai.yaml` untuk Codex sudah disertakan. Untuk
memperbarui, jalankan `git pull` di folder itu.

### Claude.ai

1. Buat ZIP berisi folder `naskah-id` yang di dalamnya langsung ada `SKILL.md`. ZIP unduhan
   GitHub berisi folder `naskah-id-main`; ubah dulu nama foldernya menjadi `naskah-id`, lalu
   kompres ulang.
2. Di Claude.ai, buka pengaturan, bagian skill, lalu unggah ZIP itu sebagai skill kustom.
   Bila diminta, aktifkan dulu fitur eksekusi kode.

### Aplikasi Gemini (Gems)

Aplikasi chat Gemini, baik versi web maupun desktop, tidak membaca folder skill yang dipasang
lewat `npx skills`. Folder itu hanya dibaca Gemini CLI. Untuk memakai skill ini di aplikasi chat,
buat Gem:

1. Di aplikasi Gemini, buka **Gems**, lalu buat Gem baru, misalnya dengan nama `naskah-id`.
2. Salin seluruh isi `SKILL.md` ke kolom instruksi.
3. Unggah berkas di folder `references/` sebagai pengetahuan Gem.

Di Gem, skill hanya bekerja sebagai aturan bahasa dan rujukan. `scripts/periksa.py`,
`scripts/openalex.py`, dan server MCP tidak bisa dijalankan, jadi pemeriksaan otomatis dan
pencarian rujukan tidak tersedia.

### Alat riset (opsional)

Untuk mencari dan mengecek rujukan, skill memakai alat berikut:

- **OpenAlex**: `scripts/openalex.py` ikut terpasang dan langsung bisa dipakai, tanpa akun.
- **Consensus dan alphaXiv**: server MCP yang perlu login. Pada plugin Claude Code, keduanya
  ikut terpasang lewat `.mcp.json`; ketik `/mcp` untuk masuk.
- **PubMed**: konektor claude.ai.

Bila alat itu belum tersambung, agen menawarkan cara menyambungkannya saat pertama kali
pekerjaan Anda butuh rujukan. Perintah dan potongan konfigurasi untuk Claude Code, Codex,
claude.ai, Cursor, Gemini CLI, GitHub Copilot, Windsurf, dan OpenCode ada di
[references/alat-riset.md](references/alat-riset.md).

### Cek pemasangan

Mulai sesi baru, lalu minta: `Cek ejaan kalimat ini: Data di analisis dengan SPSS.` Agen yang
memuat skill akan mengoreksi `di analisis` menjadi "dianalisis" tanpa mengubah bagian lain.

Pemeriksa `scripts/periksa.py` bersifat opsional dan butuh Python 3.7 atau lebih baru, tanpa
pustaka tambahan.

## Cara pakai

Minta saja dengan bahasa biasa. Skill akan dimuat bila permintaan Anda menyangkut naskah ilmiah
berbahasa Indonesia.

| Anda menulis | Yang dikerjakan agen |
| --- | --- |
| "Cek ejaan bab 3 ini, jangan ubah kalimatnya." | Koreksi: ejaan, tanda baca, kata baku. Perubahan dilaporkan satu per satu. |
| "Rapikan bahasa latar belakang ini, terasa kaku." | Sunting: susunan kalimat, perangkai, pleonasme, klise. Isi tidak berubah. |
| "Tulis ulang paragraf tinjauan pustaka ini supaya tidak menyitir satu per satu." | Tulis ulang: struktur paragraf berubah, sitasi tetap melekat pada klaimnya. |
| "Buat abstrak dari hasil berikut, target jurnal SINTA 2 bidang kesehatan." | Tulis: abstrak dari bahan Anda, dengan penanda untuk data yang kurang. |
| "Saya pakai AI untuk merapikan bab 2. Apa yang harus saya cantumkan?" | Draf pernyataan penggunaan AI sesuai sasaran. |

Sebutkan jurnal atau kampus sasaran bila ada. Bila agen punya akses web, ia membaca templat dan
beberapa artikel terbitan jurnal itu lebih dulu untuk mengikuti struktur, gaya sitasi, sudut
pandang, dan istilah bidangnya. Bila tidak, agen mengatakan bahwa konvensi jurnal belum dicek.

## Cara kerja

1. **Kenali sasaran.** Jenis naskah, jurnal atau kampus, gaya sitasi.
2. **Tandai.** Masalah dibagi tiga: K (kaidah, wajib diperbaiki), G (gaya, anjuran), dan AI
   (klise mesin). Sebelum menandai, agen memeriksa daftar konvensi yang harus dipertahankan:
   pasif di bab Metode, "penelitian ini", istilah asing yang lazim di bidangnya, hedging yang
   sah, dan "signifikan" dalam arti statistik.
3. **Draf.** Perbaikan sesuai batas pekerjaan.
4. **Periksa fakta.** Draf dibandingkan dengan teks asli: angka, nama, dan sitasi harus sama,
   tidak ada fakta baru, kekuatan klaim tidak naik.
5. **Serahkan.** Teks, catatan perubahan, penanda yang tersisa, dan draf pernyataan penggunaan
   AI.

Untuk mencari rujukan, skill memakai `scripts/openalex.py`, ditambah Consensus, alphaXiv,
PubMed, Crossref, dan Garuda atau SINTA bila tersedia. Tanpa alat apa pun, skill tetap bekerja
dan menandai klaim yang belum berujukan dengan `[PERLU RUJUKAN: …]`.

## Isi repo

| Berkas | Isi |
| --- | --- |
| `SKILL.md` | Kontrak ringkas, batas perubahan, alur kerja, tanda terkuat |
| `KONTRAK.md` | Kontrak tanggung jawab lengkap dan templat pernyataan penggunaan AI |
| `references/pola-ai.md` | Katalog pola AI dan kalke Inggris: Waspadai, Masalahnya, Sebelum, Sesudah |
| `references/pertahankan.md` | Konvensi ilmiah yang jangan dikoreksi |
| `references/kalimat-efektif.md` | Subjek hilang, perangkai, nominalisasi, pleonasme |
| `references/ejaan-eyd-v.md` | Kata depan, gabungan kata, angka, satuan, tanda koma, huruf miring |
| `references/kata-baku.md` | Kata tidak baku yang sering muncul di naskah |
| `references/istilah.md` | Parameter menimbang padanan istilah asing dan data keterpakaiannya |
| `references/singkatan.md` | Kaidah singkatan dan akronim, daftar singkatan, nama lembaga yang berubah |
| `references/sitasi.md` | Kejujuran rujukan, cara mengecek, gaya sitasi |
| `references/bagian-naskah.md` | Abstrak, pendahuluan, tinjauan pustaka, metode, hasil, simpulan |
| `contoh/` | Paragraf sebelum dan sesudah dari teknik, kesehatan, sosial, pendidikan, sejarah |
| `references/alat-riset.md` | Cara menyambungkan OpenAlex, Consensus, alphaXiv, dan PubMed |
| `scripts/periksa.py` | Pemeriksa pola berbasis regex dan pembanding fakta asli/hasil, hanya pustaka standar Python |
| `scripts/openalex.py` | Cari, cek, dan kutip karya lewat OpenAlex dan Crossref, hanya pustaka standar Python |
| `.mcp.json` | Server MCP Consensus dan alphaXiv untuk plugin Claude Code |
| `evals/cases.json` | Kasus uji perilaku agen beserta kriteria lulus dan cek otomatis |
| `evals/jalankan.py` | Runner eval: menjalankan agen, mengecek otomatis, dan memanggil model penilai |
| `CHANGELOG.md` | Riwayat versi |

## Pemeriksa cepat

`scripts/periksa.py` menyaring pola kaidah dan klise mesin tanpa memanggil model apa pun.

```bash
python scripts/periksa.py naskah.md
python scripts/periksa.py --banding asli.md hasil.md   # angka, sitasi, kutipan yang berubah
python scripts/periksa.py --tes
```

Contoh keluaran:

```
naskah.md:4: [KE-01 K] 'Dari hasil pengujian menunjukkan': subjek hilang karena kata depan; ...
naskah.md:9: [KB-01 K] 'analisa': baku: analisis
naskah.md:12: [NM-01 G] 'mengalami penurunan': nominalisasi; pakai verbanya langsung ...
naskah.md: 3 temuan (K 2, G 1)
```

Label K (kaidah) membuat kode keluar 1. Label G (gaya) dan AI (klise mesin) hanya anjuran.
Bagian Daftar Pustaka, Referensi, dan Abstract dilewati.

`--banding` membandingkan teks asli dengan hasil suntingan:

```
[SITASI] hilang: (Santoso, 2020)
[ANGKA] hilang: 1,2%
[ANGKA] baru: 1,3%
[PEMISAH] 0.5 -> 0,5 (cek: koreksi desimal atau nilai berubah?)
```

Pemeriksa ini sengaja sederhana. Pada [uji abstrak nyata](contoh/korpus/uji-abstrak-pendidikan.md),
ia menemukan 4 masalah dan melewatkan 6 lainnya yang baru tertangkap saat dibaca. Pada README
versi sebelumnya, ia tidak menemukan apa pun, padahal ada lima kesalahan isi. Pakai pemeriksa
sebagai penyaring awal, lalu baca setiap temuan dalam konteksnya.

## Cek daftar pustaka

```bash
python scripts/openalex.py daftar pustaka.txt
```

```
[3] RAGU: Santoso, B., & Wibowo, A. (2019). Pengaruh media sosial terhadap prestasi belajar…
    -> Mukhtar, A., & MD, L. (2020). PENGARUH KOMPETENSI GURU TERHADAP KINERJA GURU …
    judul tidak cocok (cakupan 0.67); penulis pertama Afiah Mukhtar tidak disebut
[5] RAGU: Hinton, G. (2018). Deep residual learning for image recognition. Nature, 12(3), 1-9.
    -> He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition …
    penulis pertama Kaiming He tidak disebut; tahun 2016 tidak disebut
```

RAGU dan TIDAK DITEMUKAN bukan bukti rujukan palsu: jurnal tanpa DOI sering tidak terindeks.

## Menimbang istilah asing

Padanan resmi tidak selalu dipakai pembaca bidangnya. Skill ini mengukurnya:

```bash
python scripts/openalex.py istilah "pembelajaran mesin" "machine learning" --bidang informatika
```

```
  istilah                        judul  judul+abstrak  pangsa
  pembelajaran mesin                49            399      8%
  machine learning                 561           1834     92%
Putusan: "machine learning" dominan (92% judul). Untuk teks baru, pakai bentuk ini.
pembelajaran mesin jarang tetapi masih dipakai: pada suntingan, pertahankan pilihan penulis.
```

Urutan pertimbangan lengkap (gaya selingkung, keterpakaian, ketepatan makna, pembaca,
konsistensi) dan hasil pengukuran 26 pasang istilah ada di
[references/istilah.md](references/istilah.md). Kaidah singkatan dan akronim, daftar singkatan
yang sering muncul, serta nama lembaga yang berubah ada di
[references/singkatan.md](references/singkatan.md).
Perintah lain (`cek`, `rujukan`, `doi`, `bib`, `dikutip`) ada di
[references/alat-riset.md](references/alat-riset.md).

## Menguji skill

```bash
python evals/jalankan.py --agen "claude -p" --hasil evals/hasil/dengan-skill --penilai "claude -p"
```

`--agen` dan `--penilai` menerima perintah apa pun yang membaca prompt dari stdin, jadi agen lain
juga bisa diuji. Untuk melihat manfaat skill, jalankan sekali tanpa skill ke folder lain lalu
bandingkan skornya. Cek otomatis (angka bertahan, pola wajib dan terlarang) berjalan tanpa
penilai; kriteria lainnya butuh penilai atau dibaca manusia.

## Pernyataan penggunaan AI

Bila Anda memakai skill ini untuk naskah yang akan dikirim, cantumkan pernyataan penggunaan AI
sesuai kebijakan sasaran. Contoh untuk jurnal SINTA atau kampus:

> Dalam penyusunan naskah ini, penulis menggunakan [NAMA ALAT] untuk menyunting ejaan dan
> susunan kalimat. Seluruh isi, data, dan rujukan telah diperiksa penulis, dan penulis
> bertanggung jawab penuh atas isi naskah.

Templat untuk Elsevier, IEEE, dan Springer Nature ada di [KONTRAK.md](KONTRAK.md).

## Sumber

- *Ejaan Bahasa Indonesia yang Disempurnakan Edisi V* (Keputusan Kepala Badan Bahasa
  No. 0424/I/BS.00.01/2022). https://ejaan.kemendikdasmen.go.id/
- *Kamus Besar Bahasa Indonesia* daring. https://kbbi.kemendikdasmen.go.id/
- Alwi, H. dkk. *Tata Bahasa Baku Bahasa Indonesia*, ed. IV. Badan Bahasa, 2017.
- Pusat Bahasa. *Kalimat Efektif Bahasa Indonesia*, 1995.
- BIPM. *The International System of Units (SI)*, ed. 9.
- Kebijakan AI dari COPE, Elsevier, IEEE, Springer Nature, Universitas Indonesia, UGM, dan
  Ditjen Diktiristek. Rincian di [KONTRAK.md](KONTRAK.md).

Struktur repo terinspirasi dari:

- [blader/humanizer](https://github.com/blader/humanizer)
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)
- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)
- [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer)

Teks repo ini ditulis sendiri untuk bahasa Indonesia, kecuali kutipan berlisensi CC BY-SA di
`contoh/korpus/` yang atribusinya dicantumkan per kutipan.

## Kontribusi

Laporan paling berguna ada dua jenis:

- **Pola baru.** Sertakan contoh nyata (boleh disamarkan), versi perbaikannya, dan dasar
  kaidahnya bila ada (EYD V, KBBI, atau tata bahasa baku).
- **Salah positif.** Kalimat benar yang ditandai `periksa.py` atau dikoreksi agen. Sertakan
  kalimatnya dan alasan kenapa itu benar.

Sebelum mengirim perubahan, jalankan `python scripts/periksa.py --tes`,
`python scripts/openalex.py --tes`, dan `python evals/jalankan.py --tes`, lalu periksa berkas
Markdown repo dengan `periksa.py`. Repo ini tidak boleh melanggar katalognya sendiri.

## Riwayat bintang

<a href="https://star-history.com/#nothinx/naskah-id&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=nothinx/naskah-id&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=nothinx/naskah-id&type=Date" />
    <img alt="Grafik riwayat bintang naskah-id" src="https://api.star-history.com/svg?repos=nothinx/naskah-id&type=Date" />
  </picture>
</a>

## Lisensi

MIT, kecuali isi `contoh/korpus/` yang berasal dari artikel berlisensi CC BY-SA dan karena
itu dirilis dengan CC BY-SA 4.0.

## English summary

`naskah-id` is an agent skill for writing and editing Indonesian academic texts (journal
articles, theses, grant proposals) in natural, standard Indonesian (EYD V, KBBI). It never
changes numbers, results, or citations, never invents references, and is not a tool for
evading AI detectors. Install with `npx skills add nothinx/naskah-id` for Claude Code, Codex,
Cursor, Gemini CLI, GitHub Copilot, Windsurf, OpenCode, and other Agent Skills hosts. It ships
a regex checker with a before/after fact diff (numbers, citations, quotes) and an
OpenAlex/Crossref CLI that verifies whole bibliographies and prints APA/IEEE entries. An eval
runner and MCP setup for Consensus and alphaXiv are included. MIT licensed.
