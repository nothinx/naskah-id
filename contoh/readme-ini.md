# Uji pada README repo ini

README repo ini disunting dengan skill `naskah-id` sendiri, 22 Oktober 2026. Berkas ini mencatat
apa yang ditemukan, agar pembaca bisa menilai cara kerja skill pada teks yang ditulis agen AI.

**Pekerjaan:** tulis ulang. Struktur bagian dipertahankan; kalimat, contoh, dan klaim boleh
diubah, tetapi fakta tentang repo tidak boleh ditambah.

## Langkah 1: `periksa.py`

```
$ python scripts/periksa.py README.md
(tidak ada temuan)
```

Pemeriksa regex tidak menemukan apa pun. Semua masalah di bawah ditemukan dengan membaca teks
mengikuti langkah "Tandai" dan "Periksa fakta" di `SKILL.md`.

## Langkah 2: masalah isi

Kelima masalah ini melanggar kontrak skill, padahal README justru dimaksudkan sebagai contoh
kontrak itu.

| # | Versi sebelumnya | Masalah | Perbaikan |
| --- | --- | --- | --- |
| 1 | Contoh pembuka kosmik: versi kaku tentang "teknologi informasi berkembang pesat", versi natural tentang puskesmas | Versi natural memuat fakta yang tidak ada di versi kaku | Versi kaku diberi fakta puskesmas, lalu versi natural cukup membuang pembukanya |
| 2 | Contoh klaim digelembungkan: versi natural memuat rerata 61,2 dan 74,5 serta "uji-*t* berpasangan" | Angka dan nama uji muncul dari ketiadaan | Angka dipindah ke versi kaku; "uji-*t* berpasangan" dihapus karena tidak pernah disebut |
| 3 | Contoh "hal ini": `menunjukkan bahwa` diganti `sejalan dengan` | Kekuatan klaim berubah. Kontrak hanya melarang klaim dinaikkan, tetapi menurunkannya juga mengubah isi | Verba "menunjukkan" dipertahankan; yang diganti hanya "hal ini" |
| 4 | "Seluruh teks di repo ini ditulis sendiri" | Tidak benar: `contoh/korpus/` memuat kutipan artikel jurnal | Pengecualian untuk kutipan berlisensi disebutkan |
| 5 | "Agen akan membaca templat dan beberapa artikel terbitan jurnal itu" | Janji berlebihan: agen tanpa akses web tidak bisa melakukannya | Ditambah syarat akses web dan apa yang dilakukan agen bila tidak ada |

## Langkah 3: masalah gaya

| # | Versi sebelumnya | Label | Perbaikan |
| --- | --- | --- | --- |
| 6 | "Hasilnya baku …, enak dibaca" | AI (klaim promosi) | "enak dibaca" dibuang karena tidak bisa dibuktikan |
| 7 | "Tanda-tanda ini paling sering membuat naskah …" | AI (klaim digelembungkan) | "paling sering" menjadi "sering"; tidak ada data frekuensi |
| 8 | Contoh perangkai: "tempat orang tua berperan penting" | G (makna kabur) | Ditambah objek: berperan penting dalam distribusi pupuk |
| 9 | "Skill ini membantu Anda menulis lebih baik." | AI (kalimat kosong) | Dihapus; kalimat berikutnya sudah menyebut apa yang dikerjakan |
| 10 | Judul "Apa ini, dan apa yang bukan" | G (tanda baca) | Koma dihapus |

## Langkah 4: periksa fakta

- Perintah pemasangan, nama berkas, dan nama repo sama dengan versi sebelumnya.
- Angka baru di README hanya berasal dari uji yang tercatat: 5 temuan dan 5 yang terlewat pada
  `contoh/korpus/uji-abstrak-pendidikan.md`.

## Langkah 5: masalah yang sama di berkas lain

Setelah masalah 1 sampai 3 ditemukan, semua pasangan contoh di repo diperiksa ulang dengan
pertanyaan yang sama: apakah versi sesudah memuat fakta yang tidak ada di versi sebelum?

- `references/pola-ai.md`: 10 pasangan diperbaiki. Contohnya, versi sesudah untuk tiga sifat
  berderet memuat "akurasi 91%" dan "40 ms" yang tidak ada di versi sebelum. Kini angka itu ada
  di versi sebelum. Pasangan yang perbaikannya memang butuh data baru memakai `[PERLU DATA: …]`.
- `contoh/sebelum-sesudah.md`: 2 pasangan diperbaiki. Contoh 1 memuat "rawan salah salin" yang
  tidak ada di versi kaku, dan contoh 7 mengubah "faktor yang sangat penting" menjadi "penengah
  utama", yang menaikkan klaim.

## Pelajaran untuk skill

Masalah 1 sampai 3 terjadi di contoh yang ditulis agen yang sama dengan agen yang menulis
kontraknya. Kesalahan yang paling mudah terjadi bukan salah ejaan, melainkan versi "sesudah"
yang diam-diam memuat fakta baru agar terlihat lebih meyakinkan. Karena itu langkah "Periksa
fakta" tidak boleh dilewati, juga untuk teks yang ditulis agen sendiri.
