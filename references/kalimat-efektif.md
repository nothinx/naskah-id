# Kalimat efektif

Kalimat efektif memuat satu gagasan dengan subjek dan predikat yang jelas, tanpa kata yang
mubazir. Rujukan utama: *Tata Bahasa Baku Bahasa Indonesia* (Alwi dkk., ed. IV, 2017) dan
*Kalimat Efektif Bahasa Indonesia* (Pusat Bahasa, 1995). Kode KE-xx sama dengan keluaran
`scripts/periksa.py`.

## Subjek hilang

### KE-01 · Kata depan di depan subjek (K)

- **Waspadai:** Dari hasil … menunjukkan; Dalam penelitian ini membahas; Pada Gambar 3 memperlihatkan; Bagi peserta yang …; Menurut X mengatakan; Berdasarkan hasil penelitian menyimpulkan
- **Masalahnya:** kata depan mengubah calon subjek menjadi keterangan sehingga kalimat tidak
  bersubjek. Buang kata depannya, atau pertahankan kata depan dan ubah verbanya menjadi pasif.
- **Sebelum:** Dari hasil analisis menunjukkan bahwa kepuasan pasien rendah.
- **Sesudah:** Hasil analisis menunjukkan bahwa kepuasan pasien rendah.
- **Sebelum:** Dalam penelitian ini membahas peran pesantren dalam ekonomi desa.
- **Sesudah:** Penelitian ini membahas peran pesantren dalam ekonomi desa. *Atau:* Dalam penelitian ini dibahas peran pesantren dalam ekonomi desa.
- **Sebelum:** Menurut Koentjaraningrat mengatakan bahwa kebudayaan memiliki tujuh unsur.
- **Sesudah:** Menurut Koentjaraningrat, kebudayaan memiliki tujuh unsur.

### Kalimat tanpa pelaku dan tanpa pasif (K)

- **Sebelum:** Untuk mengukur tekanan darah menggunakan tensimeter digital.
- **Sesudah:** Tekanan darah diukur dengan tensimeter digital.

### Pasif bertumpuk (G)

- **Sebelum:** Pengujian dilakukan oleh peneliti terhadap instrumen yang telah disusun oleh tim yang dibentuk oleh jurusan.
- **Sesudah:** Tim jurusan menyusun instrumen, lalu peneliti mengujinya.

### Pembuka "Adapun" (G)

- **Sebelum:** Adapun tujuan penelitian ini adalah untuk mengetahui pengaruh …
- **Sesudah:** Penelitian ini bertujuan mengukur pengaruh …

## Perangkai

| Kode | Kaku atau salah | Baku | Label |
| --- | --- | --- | --- |
| KE-10 | `berdasarkan pada hasil uji` | berdasarkan hasil uji | K |
| | `terdiri dari tiga bab` | terdiri atas tiga bab (anjuran Badan Bahasa) | G |
| KE-11 | `antara A dengan B` | antara A dan B | K |
| KE-12 | `baik A ataupun B`, `baik A dan B` | baik A maupun B | K |
| KE-13 | `bukan A, tetapi B` | bukan A, melainkan B; tidak A, tetapi B | K |
| KE-14 | `Meskipun mahal, tetapi awet.` | Meskipun mahal, alat ini awet. | K |
| KE-15 | `Karena hujan, maka panen gagal.`, `Berdasarkan uraian di atas, maka …` | Karena hujan, panen gagal. Berdasarkan uraian di atas, … | K |
| | `Jika …, maka …` | "maka" boleh, tetapi biasanya mubazir | G |
| KE-16 | `Sehingga …` / `Sedangkan …` di awal kalimat | gabungkan dengan kalimat sebelumnya, atau pakai Akibatnya / Adapun | K |
| KE-17 | `lebih baik dari` | lebih baik daripada | K |
| | `Daripada itu, …` | Selain itu, … | K |
| | `Namun demikian, …` | Namun, … / Meskipun demikian, … | G |
| | `Dikarenakan …` | Karena … | G |
| | `dalam rangka meningkatkan` | untuk meningkatkan | G |

### "sehingga" tanpa koma

"Sehingga" adalah konjungsi intrakalimat. EYD V (Tanda Koma, kaidah 4) menyatakan bahwa koma
tidak dipakai bila induk kalimat mendahului anak kalimat. EYD V tidak menyebut "sehingga"
secara khusus, tetapi anak kalimat akibat yang diawali "sehingga" mengikuti kaidah itu, jadi tulis "Galat menurun sehingga akurasi naik", bukan dengan koma sebelum
"sehingga". Bila ingin memulai kalimat baru, pakai "Akibatnya," atau "Karena itu,".

Koma tetap dipakai sebelum konjungsi pertentangan: "tetapi", "melainkan", "sedangkan".

## Nominalisasi

Kode NM-01 (G). Verba penopang ("melakukan", "mengalami", "memberikan") ditambah nomina membuat kalimat
panjang tanpa menambah makna. Pakai verbanya langsung.

| Kaku | Ringkas |
| --- | --- |
| `melakukan analisis terhadap data` | menganalisis data |
| `melakukan pengukuran` | mengukur |
| `melakukan perbandingan antara` | membandingkan |
| `mengalami peningkatan` | meningkat |
| `mengalami penurunan sebesar 5%` | turun 5% |
| `memberikan pengaruh terhadap` | memengaruhi |
| `telah dilakukan pengujian terhadap sampel` | sampel diuji |
| `Penelitian ini bertujuan untuk mengetahui` | Penelitian ini bertujuan mengukur / menguji / membandingkan |

Nominalisasi tetap wajar bila nominanya memang pokok bahasan: "Pengukuran dilakukan dua kali
sehari" bisa dipertahankan bila paragraf itu membahas prosedur pengukuran.

## Pleonasme

| Kode | Pleonasme | Pilih salah satu |
| --- | --- | --- |
| KE-02 | `adalah merupakan` | adalah; merupakan |
| KE-03 | `agar supaya`, `demi untuk`, `sejak dari` | agar; supaya; demi; untuk; sejak |
| KE-04 | `sangat penting sekali` | sangat penting; penting sekali |
| KE-05 | `para peneliti-peneliti`, `banyak data-data` | para peneliti; banyak data |
| KE-06 | `berbagai macam metode` | berbagai metode; bermacam-macam metode |
| KE-07 | `naik ke atas`, `mundur ke belakang` | naik; mundur |
| KE-08 | `saling tolong-menolong` | tolong-menolong; saling menolong |
| KE-09 | `seperti: A, B, dan lain-lain` | seperti A dan B; antara lain A dan B |
| | `masih … hingga kini` | masih …; … hingga kini |
| | `Dengan demikian dapat disimpulkan bahwa` | Jadi, …; Simpulannya, … |

## Panjang dan kepaduan

Kode KL-01 (G): kalimat lebih dari 35 kata ditandai `periksa.py`.

- Satu kalimat, satu gagasan. Kalimat di atas 35 kata hampir selalu bisa dipecah.
- Variasikan panjang kalimat. Temuan sering paling kuat dalam kalimat pendek.
- Unsur yang setara ditulis dalam bentuk yang sama (kesejajaran): "mengumpulkan, mengolah,
  dan menganalisis data", bukan campuran verba dan nomina seperti "pengumpulan, mengolah, dan
  analisis data".
- Pakai "bahwa" sesudah verba yang memperkenalkan isi klausa: "Hasil ini menunjukkan bahwa
  dosis berpengaruh." Jangan menyisipkannya di tempat lain hanya agar kalimat terdengar
  formal. Bandingkan "Diketahui bahwa kadar gula responden tinggi" dengan versi yang lebih
  ringkas: "Kadar gula responden tinggi."
