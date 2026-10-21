# naskah-id

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

Skill ini **bukan** alat untuk meloloskan teks dari detektor AI atau Turnitin, dan **bukan**
detektor AI. Pola bahasa tidak bisa membuktikan siapa yang menulis sebuah teks, jadi jangan
memakai skill ini untuk menuduh mahasiswa.

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

### Lewat `npx skills` (Claude Code, Codex, Cursor, Gemini CLI, dan agen lain)

Butuh Node.js 18 atau lebih baru.

```bash
npx skills add nothinx/naskah-id        # untuk proyek di folder ini saja
npx skills add nothinx/naskah-id -g     # untuk semua proyek
```

Perintah ini menanyakan agen mana yang dipasangi. Untuk memperbarui skill, jalankan ulang
perintah yang sama.

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
Claude Code atau `~/.cursor/skills` untuk Cursor. Di Windows, `~` berarti folder pengguna
(`C:\Users\<nama-pengguna>`). Berkas `agents/openai.yaml` untuk Codex sudah disertakan. Untuk
memperbarui, jalankan `git pull` di folder itu.

### Claude.ai

1. Buat ZIP berisi folder `naskah-id` yang di dalamnya langsung ada `SKILL.md`. ZIP unduhan
   GitHub berisi folder `naskah-id-main`; ubah dulu nama foldernya menjadi `naskah-id`, lalu
   kompres ulang.
2. Di Claude.ai, buka pengaturan, bagian skill, lalu unggah ZIP itu sebagai skill kustom.
   Bila diminta, aktifkan dulu fitur eksekusi kode.

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

Untuk mencari rujukan, skill menganjurkan Consensus, OpenAlex, PubMed, arXiv, Crossref, dan
Garuda atau SINTA. Skill tetap berfungsi tanpa alat-alat itu.

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
| `references/sitasi.md` | Kejujuran rujukan, cara mengecek, gaya sitasi |
| `references/bagian-naskah.md` | Abstrak, pendahuluan, tinjauan pustaka, metode, hasil, simpulan |
| `contoh/` | Paragraf sebelum dan sesudah dari teknik, kesehatan, sosial, pendidikan, sejarah |
| `scripts/periksa.py` | Pemeriksa pola berbasis regex, hanya pustaka standar Python |
| `evals/cases.json` | Kasus uji perilaku agen beserta kriteria lulus |

## Pemeriksa cepat

`scripts/periksa.py` menyaring pola kaidah dan klise mesin tanpa memanggil model apa pun.

```bash
python scripts/periksa.py naskah.md
python scripts/periksa.py --tes
```

Contoh keluaran:

```
naskah.md:4: [KE-01 K] 'Dari hasil pengujian menunjukkan': subjek hilang karena kata depan; ...
naskah.md:9: [KB-01 K] 'analisa': baku: analisis
```

Pemeriksa ini sengaja sederhana. Pada [uji abstrak nyata](contoh/korpus/uji-abstrak-pendidikan.md),
ia menemukan 4 masalah dan melewatkan 6 lainnya yang baru tertangkap saat dibaca. Pada README
versi sebelumnya, ia tidak menemukan apa pun, padahal ada lima kesalahan isi. Pakai pemeriksa
sebagai penyaring awal, lalu baca setiap temuan dalam konteksnya.

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

Struktur repo terinspirasi dari [blader/humanizer](https://github.com/blader/humanizer),
[hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop),
[conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing), dan
[AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer).
Teks repo ini ditulis sendiri untuk bahasa Indonesia, kecuali kutipan berlisensi CC BY-SA di
`contoh/korpus/` yang atribusinya dicantumkan per kutipan.

## Kontribusi

Laporan paling berguna ada dua jenis:

- **Pola baru.** Sertakan contoh nyata (boleh disamarkan), versi perbaikannya, dan dasar
  kaidahnya bila ada (EYD V, KBBI, atau tata bahasa baku).
- **Salah positif.** Kalimat benar yang ditandai `periksa.py` atau dikoreksi agen. Sertakan
  kalimatnya dan alasan kenapa itu benar.

Sebelum mengirim perubahan, jalankan `python scripts/periksa.py --tes` dan periksa berkas
Markdown repo dengan `periksa.py`. Repo ini tidak boleh melanggar katalognya sendiri.

## Lisensi

MIT, kecuali isi `contoh/korpus/` yang berasal dari artikel berlisensi CC BY-SA dan karena
itu dirilis dengan CC BY-SA 4.0.

## English summary

`naskah-id` is an agent skill for writing and editing Indonesian academic texts (journal
articles, theses, grant proposals) in natural, standard Indonesian (EYD V, KBBI). It never
changes numbers, results, or citations, never invents references, and is not a tool for
evading AI detectors. Install with `npx skills add nothinx/naskah-id`. MIT licensed.
