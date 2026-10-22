# Uji pada abstrak nyata: pendidikan jasmani

Uji ini menjalankan skill pada satu abstrak terbitan dengan pekerjaan **sunting**. Tujuannya
memeriksa apakah kontrak skill bekerja: angka tetap, tidak ada fakta baru, dan hal yang tidak
bisa diputuskan agen dikembalikan ke penulis.

Sumber: Saryono, Broto, D. P., Sridadi, & Adriansyah, R. B. (2024). Penggunaan media
pembelajaran berbasis ICT pada guru PJOK sekolah menengah pertama. *Jurnal Pendidikan Jasmani
Indonesia*, 20(1). https://doi.org/10.21831/jpji.v20i1.76029. CC BY-SA 4.0. Abstrak bahasa
Indonesia diambil dari OpenAlex dan dikutip utuh.

## Teks asli

<!-- periksa:abaikan -->
> Penelitian ini bertujuan untuk mengetahui seberapa tinggi tingkat penggunaan media
> pembelajaran berbasis ICT oleh Guru pendidikan jasmani olahraga dan kesehatan di sekolah
> SMP/MTs sederajat se-Kecamatan Banguntapan. Penelitian ini merupakan penelitian deskriptif
> kuantitatif. Metode yang digunakan dalam penelitian ini yaitu metode survei dengan pengambilan
> data menggunakan angket. Populasi dalam penelitian ini adalah Guru PJOK SMP se-Kecamatan
> Banguntapan sejumlah 25 guru dari 10 sekolah. Sampel penelitian ditentukan dengan mengambil
> seluruh subyek responden atau sampel jenuh sejumlah 25 guru. Teknik penggumpulan data
> menggunakan angket. Hasil uji reliabilitas penelitian ini adalah 0,927. Hasil uji validitas
> dengan uji instrumen menunjukan nilai r tabel 0,381 Uji instrumen dilakukan di SMP/MTs
> sekecamatan Imogiri. Analisis data menggunakan analisis statistik deskriptif dengan
> persentase. Hasil penelitian diketahui tingkat penggunaan media pembelajaran berbasis ICT oleh
> Guru PJOK di sekolah SMP/MTs sederajat se-Kecamatan Banguntapan menunjukan hasil dengan
> kategori sangat baik 1 orang (4%), kategori baik 5 orang (20%), kategori sedang 12 orang (48%),
> kategori rendah 5 orang (20%), dan kategori sangat rendah 2 orang (8%). Berdasarkan hasil
> penelitian menyimpulkan bahwa nilai rata-rata penggunaan media berbasis ICT oleh Guru PJOK di
> SMP/MTs sederajat se-Kecamatan Banguntapan, Bantul Yogyakarta termasuk dalam kategori sedang.
<!-- periksa:lanjut -->

## Keluaran `periksa.py`

```
[KB-01 K] 'subyek': baku: subjek
[KB-01 K] 'menunjukan': baku: menunjukkan   (2 kali)
[KL-01 G] 'Hasil penelitian diketahui tingkat penggunaan media …': 41 kata; pecah menjadi dua kalimat atau lebih
[KE-01 K] 'Berdasarkan hasil penelitian menyimpulkan': subjek hilang karena kata depan
```

Kalimat `Hasil penelitian diketahui …` tertangkap karena panjangnya (41 kata), sedangkan
ketidakbersubjekannya baru terlihat saat dibaca (SG-04 juga menandai `PJOK`, yang belum diberi
singkatan pada kemunculan pertama, dan `ICT`). Lima masalah lain tetap terlewat:
`penggumpulan` (salah ketik), `sekecamatan` (seharusnya se-Kecamatan), `Guru` berhuruf kapital
di tengah kalimat, titik yang hilang sesudah `0,381`, dan `Teknik pengumpulan data menggunakan
angket` yang mengulang kalimat ketiga. Pemeriksa regex memang hanya penyaring awal.

## Hasil sunting (CC BY-SA 4.0, olahan)

> Penelitian ini bertujuan mengukur tingkat penggunaan media pembelajaran berbasis ICT oleh guru
> pendidikan jasmani, olahraga, dan kesehatan (PJOK) di SMP/MTs sederajat se-Kecamatan
> Banguntapan. Penelitian deskriptif kuantitatif ini memakai metode survei dengan angket sebagai
> alat pengumpul data. Populasinya adalah guru PJOK SMP se-Kecamatan Banguntapan, yaitu 25 guru
> dari 10 sekolah, dan seluruhnya dijadikan sampel (sampel jenuh). Instrumen diuji di SMP/MTs
> se-Kecamatan Imogiri dengan koefisien reliabilitas 0,927 dan nilai r tabel 0,381 pada uji
> validitas. Data dianalisis dengan statistik deskriptif berupa persentase. Tingkat penggunaan
> media berbasis ICT tergolong sangat baik pada 1 guru (4%), baik pada 5 guru (20%), sedang pada
> 12 guru (48%), rendah pada 5 guru (20%), dan sangat rendah pada 2 guru (8%). Rata-rata
> penggunaan media berbasis ICT oleh guru PJOK di SMP/MTs sederajat se-Kecamatan Banguntapan,
> Bantul, Yogyakarta, termasuk kategori sedang.

## Pemeriksaan kontrak

| Pemeriksaan | Hasil |
| --- | --- |
| Angka tetap | 25, 10, 0,927, 0,381, 1 (4%), 5 (20%), 12 (48%), 5 (20%), 2 (8%) muncul persis sama |
| Tidak ada fakta baru | Tidak ada. "Orang" menjadi "guru" karena populasinya guru |
| Kekuatan klaim | Tidak berubah; "termasuk kategori sedang" dipertahankan |
| Istilah bidang | "ICT" dipertahankan sesuai judul artikel; tidak dipaksa menjadi "TIK" |
| Panjang | 188 kata menjadi 132 kata |

## Dikembalikan ke penulis

Dua hal tidak diputuskan agen karena menyangkut isi:

1. "Nilai r tabel 0,381" adalah nilai kritis, bukan hasil uji validitas. Abstrak biasanya
   melaporkan rentang r hitung butir. `[PERLU DATA: rentang r hitung butir angket]`
2. Kategori "sangat baik" sampai "sangat rendah" memakai dua skala (baik/rendah). Bila
   instrumen memang memakai label itu, biarkan; bila tidak, penulis perlu menyeragamkannya.
