# Riwayat versi

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/). Versi mengikuti
[Semantic Versioning](https://semver.org/lang/id/).

## Belum dirilis

### Diuji

- Eval penuh 25 kasus: tanpa skill 75/76, dengan skill 76/76 kriteria penilai (agen Gemini 4
  Argon tanpa akses perintah, penilai Claude Opus). Selisihnya belum bermakna.

### Ditambahkan

- Dukungan berkas `.docx` di `scripts/periksa.py` (termasuk `--banding`) memakai pustaka standar
  Python; teks diambil per paragraf dari `word/document.xml` dengan nomor baris sama dengan nomor
  paragraf.
- Daftar kata tidak baku di `references/kata-baku.md` dan pola KB-01 di `scripts/periksa.py`
  diperluas dengan bentuk yang sering muncul di skripsi dan jurnal (antara lain *hierarki*,
  *kuesioner*, *andal*, *berpikir*, *antrean*, *kelembapan*, *pernapasan*, *saraf*, *karier*, dan
  peluluhan k/p/s/t seperti *mengategorikan*, *mengomunikasikan*, *memublikasikan*).
- Lima kasus eval baru: kalke halus, kata tidak baku beruntun, klise AI, *signifikan* yang sah
  secara statistik, serta awalan di- dan kata depan; total 25.
- `SKILL.md` kini meminta agen mengingatkan bahwa rujukan wajib dibaca sebelum dikutip dan teks
  dari alat AI wajib diungkapkan, serta tetap membantu naskah berbahasa Inggris sebagai
  penyunting umum. Bilangan yang ditulis dengan huruf sesuai EYD V tidak dianggap mengubah angka.
- Templat laporan masalah di `.github/ISSUE_TEMPLATE/` (`pola-baru.yml`, `salah-positif.yml`, dan
  `config.yml`).

### Diperbaiki

- SG-04 di `scripts/periksa.py` tidak lagi menandai nama lisensi (`CC BY`, `CC BY-SA`,
  `CC BY-NC`, `MIT`, `GPL`, dsb.), jenjang madrasah (`MI`, `MTs`, `MA`), dan singkatan di dalam
  penanda `[PERLU DATA: …]` yang terpotong ganti baris.
- KL-01 di `scripts/periksa.py` tidak lagi memotong kalimat panjang pada pergantian baris di
  dalam kutipan blok (`>`).
- Hasil uji pada `contoh/korpus/uji-abstrak-pendidikan.md`, `README.md`, dan
  `contoh/readme-ini.md` diperbarui sesuai keluaran `periksa.py` terkini (menemukan 5 masalah,
  melewatkan 5 lainnya).
- Kepanjangan singkatan kesehatan dan pendidikan di `references/singkatan.md` diverifikasi ke
  regulasi kementerian/lembaga dan KBBI (*dengue* pada DBD tidak dicetak miring karena sudah
  terserap di KBBI; bentuk KBBI *ibtidaiah/sanawiah/aliah* dan bentuk regulasi
  *ibtidaiyah/tsanawiyah/aliyah* untuk MI, MTs, MA dicatat beserta sumbernya).
- Sumber regulasi RSUD, JKN, KKN, LPPM, dan MBKM di `references/singkatan.md` dibetulkan setelah
  dicek ke naskah peraturannya; *celsius* ditulis berhuruf kecil sesuai KBBI.
- `evals/jalankan.py` mencari pola `tidak_boleh_ada` hanya di teks hasil, bukan di catatan
  perubahan yang wajar mengutip teks asli (judul *Catatan*, *Daftar*, *Ringkasan*, atau *Rincian
  perubahan*). Kriteria angka dan nama alat di dua kasus eval dibetulkan.

## 1.1.0 (22 Oktober 2026)

### Ditambahkan

- `openalex.py istilah`: mengukur keterpakaian bentuk istilah (padanan, serapan, asing) di karya
  berbahasa Indonesia per bidang, lalu memberi putusan dominan, bersaing, atau data kurang,
  dibedakan untuk teks baru dan suntingan.
- `references/istilah.md`: urutan pertimbangan istilah asing dan hasil pengukuran 26 pasang
  istilah dari teknik, informatika, kesehatan, sosial, dan manajemen.
- `references/singkatan.md`: kaidah EYD V untuk singkatan dan akronim, singkatan yang sering
  muncul per bidang, singkatan bermakna ganda, dan nama lembaga yang berubah.
- Pola singkatan di `periksa.py`: SG-01 tanda hubung imbuhan (`di-PHK`), SG-02 titik singkatan
  umum (`dll.`, `s.d.`), SG-05 huruf kapital akronim (`Bappenas`, `iptek`) sebagai K; SG-03
  jamak berulang, SG-04 singkatan belum dijelaskan, SG-06 kepanjangan bukan nama diri berhuruf
  kapital sebagai G.
- Opsi `periksa.py --abaikan KODE,…`.
- Tiga kasus eval baru (istilah dan singkatan); total 20.

### Diperbaiki

- Nama lembaga di `references/singkatan.md` diverifikasi: SKI 2023 menggabungkan Riskesdas dan
  SSGI; bentuk Kemdiktisaintek dan Kemendiktisaintek sama-sama dipakai.

## 1.0.0 (22 Oktober 2026)

### Ditambahkan

- `periksa.py --banding asli hasil` melaporkan angka, sitasi, dan kutipan yang hilang atau
  bertambah setelah penyuntingan. Perubahan pemisah desimal dilaporkan terpisah.
- `openalex.py daftar` mengecek seluruh daftar pustaka dan memberi OK, RAGU, atau TIDAK
  DITEMUKAN per entri.
- `openalex.py cek --penulis --tahun` sehingga judul asli dengan penulis atau tahun karangan
  tidak lolos.
- `openalex.py rujukan --gaya apa|ieee|bib` mencetak entri daftar pustaka siap tempel.
- Crossref sebagai cadangan OpenAlex, terutama untuk jurnal SINTA ber-DOI.
- Peringatan bila metadata penulis memuat afiliasi (masalah umum pada jurnal OJS).
- Pola baru di `periksa.py`: NM-01 nominalisasi, KK-01 klaim `membuktikan`, KL-01 kalimat
  lebih dari 35 kata (ketiganya G), dan KE-15 kini mencakup `Berdasarkan …, maka`.
- Ringkasan jumlah temuan per label di akhir keluaran `periksa.py`.
- `evals/jalankan.py`: menjalankan agen apa pun lewat stdin, cek otomatis, dan model penilai.
  Kasus eval bertambah dari 12 menjadi 17, dengan kolom `bahan`, `harus_ada`, dan
  `tidak_boleh_ada`.
- Panduan naskah panjang di `SKILL.md`.

### Diperbaiki

- Nomor baris temuan KE-01 tidak lagi meleset ke baris sebelumnya.
- EJ-05 menangkap bentuk terikat di awal kalimat (`Antar muka`) tanpa menandai nama orang
  (`Tri`, `Dwi`, `Eka`).
- Bagian Daftar Pustaka, Referensi, dan Abstract dilewati agar judul berbahasa Inggris tidak
  ditandai.
- Saran EJ-07 dan EJ-08 memakai teks yang ditemukan, bukan contoh tetap; `3.3V` ditangkap utuh.
- EJ-09 menangkap `25 C`.
- `openalex.py`: galat jaringan tidak lagi berupa traceback, HTTP 429/5xx dicoba ulang,
  `dikutip` tanpa argumen tidak lagi crash.

## 0.2.0

- Alat riset OpenAlex, server MCP Consensus dan alphaXiv, dukungan berbagai agen.

## 0.1.0

- Rilis awal skill `naskah-id`.
