# Rujukan dan cara menyitir

## Aturan paling keras

1. Rujukan hanya boleh masuk naskah bila keberadaannya sudah dicek dan isinya memang mendukung
   kalimat yang mengutipnya.
2. Daftar pustaka tidak pernah disusun dari ingatan. Judul, penulis, tahun, volume, halaman,
   dan DOI diambil dari metadata, bukan ditebak.
3. Bila belum ada rujukan yang terverifikasi, tulis `[PERLU RUJUKAN: klaim yang perlu didukung]`.
   Penanda ini lebih baik daripada rujukan yang tampak meyakinkan tetapi tidak ada.
4. Saat menyunting, sitasi yang sudah ada tidak diubah, dipindah ke klaim lain, atau dihapus.
   Bila ada sitasi yang tampak keliru (tahun tidak cocok, DOI rusak), tanyakan kepada pengguna.

## Mencari dan mengecek

| Kebutuhan | Alat |
| --- | --- |
| Sintesis temuan: "apa kata riset tentang X" | Consensus |
| Metadata, abstrak, entri APA/IEEE/BibTeX, cek keberadaan, siapa yang mengutip | OpenAlex dan Crossref: `python scripts/openalex.py` (cari, doi, rujukan, bib, cek, daftar, dikutip) |
| Kesehatan dan biomedis | PubMed |
| Praterbit | arXiv, alphaXiv |
| Cek DOI | `openalex.py doi` (otomatis ke Crossref), `doi.org` |
| Jurnal Indonesia | Garuda (garuda.kemdiktisaintek.go.id), SINTA, laman OJS jurnalnya |

Cara mengecek satu rujukan:

1. Jalankan `python scripts/openalex.py cek "judul" --penulis "…" --tahun …`. Untuk seluruh
   daftar pustaka sekaligus: `python scripts/openalex.py daftar pustaka.txt`.
2. Cocokkan nama jurnal, volume, dan halaman dengan metadata yang dicetak.
3. Baca abstraknya. Pastikan klaim di naskah memang ada di sumber, bukan hanya topiknya mirip.
4. Bila tidak ditemukan di mana pun, anggap rujukan itu tidak ada dan beri penanda.

Banyak jurnal Indonesia tidak memiliki DOI atau belum terindeks OpenAlex. Untuk jurnal seperti
itu, cek di laman OJS jurnalnya atau di Garuda. Tidak terindeks tidak sama dengan tidak ada,
tetapi rujukan yang tidak bisa ditemukan di mana pun tetap diberi penanda.

## Gaya sitasi

Ikuti templat jurnal sasaran. Yang paling sering dipakai di Indonesia:

| Gaya | Bidang yang lazim | Dalam teks | Daftar pustaka |
| --- | --- | --- | --- |
| APA 7 | sosial, pendidikan, psikologi, kesehatan masyarakat | (Santoso, 2021); Santoso (2021) | Santoso, B. (2021). Judul artikel. *Nama Jurnal*, *12*(2), 45–60. https://doi.org/… |
| IEEE | teknik, informatika | [1], [2]–[4] | [1] B. Santoso, "Judul artikel," *Nama Jurnal*, vol. 12, no. 2, hlm. 45–60, 2021. |
| Vancouver | kedokteran, keperawatan | angka superskrip atau (1) | 1. Santoso B. Judul artikel. Nama Jurnal. 2021;12(2):45–60. |
| Chicago (catatan kaki) | sejarah, filsafat, kajian agama | catatan kaki bernomor | sesuai panduan jurnal |

Contoh di atas fiktif dan hanya menunjukkan format.

Dalam naskah berbahasa Indonesia, "dkk." dipakai untuk *et al.*, dan "hlm." untuk halaman,
kecuali templat jurnal memakai bentuk Inggris.

## Menyitir dalam kalimat

- Jadikan sumber subjek bila klaimnya khas sumber itu: "Wibowo dkk. [3] mengukur …".
- Untuk fakta yang sudah mapan, cukup cantumkan rujukan di akhir kalimat.
- Pakai verba pelapor yang sesuai: *mengukur, menemukan, mengusulkan, membantah, memperluas,
  mengkritik, merangkum*. "Mengatakan" dan "menyatakan" untuk semua sumber terasa datar.
- Hindari deretan sumber yang masing-masing satu kalimat. Kelompokkan menurut temuan, lalu
  tunjukkan perbedaannya. Lihat contoh tinjauan pustaka di `contoh/`.
- Jangan menulis "Menurut X mengatakan". Pilih salah satu: "Menurut X, …" atau "X mengatakan …".

## Kutipan langsung

Kutipan langsung di bawah empat baris ditulis di dalam teks dengan tanda petik dan nomor
halaman. Kutipan yang lebih panjang ditulis sebagai blok terpisah tanpa tanda petik. Ikuti
batas yang ditetapkan gaya sitasi sasaran. Kutipan tidak pernah disunting.
