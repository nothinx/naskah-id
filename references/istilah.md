# Istilah asing: diterjemahkan, diserap, atau dipertahankan

Badan Bahasa menganjurkan urutan padanan, lalu serapan, lalu istilah asing bercetak miring.
Urutan itu titik awal, bukan putusan. Padanan yang tidak dipakai pembaca bidangnya membuat
naskah lebih sulit dibaca: *penapis Kalman* tidak muncul satu kali pun di judul karya
berbahasa Indonesia 2019–2026, sedangkan *filter Kalman* muncul 15 kali. Berkas ini memberi
parameter untuk menimbangnya.

## Urutan pertimbangan

Berhenti di langkah pertama yang memberi jawaban.

### 1. Gerbang: yang tidak pernah diterjemahkan

- Nama diri dan eponim: *Kalman*, *Fourier*, *Wilcoxon*, *Newton-Raphson*.
- Nama algoritma, model, produk, dan bahasa pemrograman: *Random Forest*, YOLO, ResNet, Python,
  Arduino, ESP32.
- Standar, kode, dan nomor dokumen: ISO 9001, IEC 61850, SNI ISO/IEC 17025.
- Lambang satuan dan besaran: V, Hz, °C, *p*, *r*.
- Nama variabel, fungsi, perintah, dan berkas: `analogRead()`, `pip install`.
- Nama takson, judul karya, dan kutipan langsung.

Bagian umum dari eponim tetap ditimbang dan mengikuti hukum D-M: *filter Kalman*,
*transformasi Fourier*, *uji Wilcoxon*, *hukum Ohm*. Bila penulis ingin mempertahankan urutan
Inggris, seluruh frasa dicetak miring: *Kalman filter*.

### 2. Gaya selingkung dan pedoman

Glosarium, templat, atau artikel terbaru jurnal sasaran, serta pedoman penulisan kampus,
mengalahkan semua langkah di bawah. Bila jurnal sasaran menulis *machine learning*, pakai itu.

### 3. Keterpakaian: ukur, jangan menebak

```bash
python scripts/openalex.py istilah "catu daya" "power supply" --bidang teknik
```

Perintah ini menghitung karya berbahasa Indonesia di OpenAlex yang memuat tiap bentuk di
judulnya (2019–2026, bisa disaring per bidang), lalu memberi putusan:

| Pangsa bentuk di judul | Putusan untuk teks baru | Putusan pada suntingan |
| --- | --- | --- |
| ≥ 60% | pakai bentuk ini | pertahankan pilihan penulis bila bentuknya masih dipakai |
| 25–60% untuk semua bentuk | bersaing: keduanya hidup | pertahankan pilihan penulis |
| < 25% | jarang, tetapi masih dipakai | pertahankan pilihan penulis |
| < 5% dan < 10 judul | hampir tidak dipakai | sarankan bentuk dominan di catatan, jangan langsung ganti |
| total < 20 karya | data kurang | jangan mengubah apa pun berdasarkan data ini |

Judul dipakai sebagai ukuran utama karena banyak artikel berbahasa Indonesia memiliki abstrak
berbahasa Inggris. Hitungan judul+abstrak dipakai hanya bila judul kurang dari 20 karya, dan
bentuk Inggris terhitung lebih di sana.

Batas ukuran ini:

- Cakupan OpenAlex atas jurnal Indonesia belum lengkap, dan deteksi bahasanya tidak sempurna.
- Pencarian frasa ikut menghitung frasa yang lebih panjang: *interface* ikut menghitung
  *user interface*. Bandingkan bentuk yang setara panjangnya.
- Kata Inggris yang umum (*online*, *framework*) bisa terhitung dari konteks lain.
- Kata Indonesia yang bermakna umum (*daya*, *awan*) tidak bisa diukur sendirian; ukur
  frasanya (*catu daya*, *komputasi awan*).

Bila perintah tidak bisa dijalankan, katakan bahwa keterpakaian belum diukur, lalu pertahankan
pilihan penulis.

### 4. Ketepatan makna

Padanan ditolak, walaupun populer, bila dalam konteks itu:

- bermakna lain yang bisa salah baca. *Luaran* dalam proposal hibah berarti hasil yang
  dijanjikan (publikasi, paten), sedangkan *keluaran* sistem adalah *output* sinyal atau data.
- menyempitkan atau meluaskan makna. *Galat* tepat untuk selisih ukur atau numerik, tetapi
  *error* pada perangkat lunak (*error 404*) bukan galat.
- berbeda antarbidang. *Derau* lazim di buku teks elektro, tetapi *noise* jauh lebih sering di
  judul (90% di bidang teknik).

### 5. Pembaca

Skripsi dan artikel jurnal dibaca orang bidang itu. Laporan untuk pemerintah daerah, Dishub,
atau masyarakat umum dibaca orang di luar bidang: pilih padanan yang dipahami umum dan beri
istilah asing dalam kurung.

### 6. Konsistensi

Satu konsep, satu bentuk, di seluruh naskah. *Basis data* di Bab 2 dan *database* di Bab 4
adalah kesalahan, apa pun pilihannya. Pada naskah panjang, tetapkan daftar istilah sebelum bab
pertama (lihat `SKILL.md`, Naskah panjang).

## Cara menulis setelah memilih

- **Padanan dipilih:** kemunculan pertama memakai padanan dengan istilah asing dalam kurung,
  lalu padanan saja: catu daya (*power supply*).
- **Istilah asing dipilih:** dicetak miring setiap kali muncul, kecuali gaya selingkung
  menentukan lain: *deep learning*, *stakeholder*.
- **Serapan yang sudah ada di KBBI** ditulis tegak: mikrokontroler, sensor, prevalensi.
- **Dengan singkatan:** *Internet of Things* (IoT); kecerdasan buatan (*artificial intelligence*,
  AI). Aturan singkatan ada di `references/singkatan.md`.
- **Imbuhan Indonesia pada kata asing** memakai tanda hubung: di-*upload*. Bila padanannya
  hidup, pakai padanannya: diunggah.

## Pada tiap jenis pekerjaan

| Pekerjaan | Yang dilakukan |
| --- | --- |
| Koreksi | Istilah tidak diganti. Yang dibetulkan hanya ejaan serapan (`sistim` → sistem) dan huruf miring. |
| Sunting | Pilihan penulis dipertahankan. Bentuk yang hampir tidak dipakai atau tidak konsisten diusulkan di catatan, tidak diganti diam-diam. |
| Tulis ulang dan tulis | Ikuti gaya selingkung, lalu putusan keterpakaian, lalu langkah 4–6. |

## Hasil pengukuran (Oktober 2026)

Karya berbahasa Indonesia di OpenAlex, 2019–2026, judul. Angka akan berubah; ukur ulang
sebelum dijadikan dasar keputusan.

| Bidang | Bentuk (jumlah judul, pangsa) | Putusan |
| --- | --- | --- |
| teknik | mikrokontroler 1.518 (91%) · *microcontroller* 142 | padanan serapan dominan |
| teknik | energi terbarukan 125 (83%) · *renewable energy* 25 | padanan dominan |
| teknik | panel surya 165 (82%) · *solar panel* 37 · panel fotovoltaik 0 | padanan dominan |
| teknik | catu daya 45 (50%) · *power supply* 45 (50%) | bersaing |
| teknik | *noise* 44 (90%) · derau 5 | asing dominan |
| teknik | *timer* 39 (87%) · pewaktu 6 | asing dominan |
| semua bidang | filter Kalman 15 · tapis Kalman 4 · penapis Kalman 0 | *filter* dominan |
| informatika | *deep learning* 410 (97%) · pembelajaran mendalam 13 | asing dominan |
| informatika | *framework* 1.674 (96%) · kerangka kerja 61 | asing dominan |
| informatika | *neural network* 1.222 (93%) · jaringan saraf tiruan 85 | asing dominan; padanan masih dipakai |
| informatika | *machine learning* 561 (92%) · pembelajaran mesin 49 | asing dominan; padanan masih dipakai |
| informatika | *cloud computing* 233 (86%) · komputasi awan 37 | asing dominan |
| informatika | *database* 523 (72%) · basis data 205 | asing dominan; padanan masih dipakai |
| informatika | *artificial intelligence* 861 (66%) · kecerdasan buatan 407 · kecerdasan artifisial 30 | asing dominan; *kecerdasan buatan* jauh lebih hidup daripada *kecerdasan artifisial* |
| informatika | *server* 783 · peladen 1 | padanan tidak hidup |
| informatika | *Internet of Things* 174 · internet untuk segala 0 | padanan tidak hidup |
| kesehatan | *stunting* 7.466 · tengkes 5 | padanan resmi belum hidup |
| kesehatan | uji klinis 21 (72%) · *clinical trial* 8 | padanan dominan |
| kesehatan | *gadget* 41 (79%) · gawai 11 | asing dominan |
| sosial | *online* 7.901 (59%) · daring 5.501 (41%) | bersaing |
| sosial | luring 233 (71%) · *offline* 97 | padanan dominan |
| sosial | *stakeholder* 323 (84%) · pemangku kepentingan 63 | asing dominan; padanan masih dipakai |
| manajemen | kepuasan pelanggan 3.684 (82%) · *customer satisfaction* 785 | padanan dominan |
| manajemen | *e-commerce* 1.576 (99%) · perdagangan elektronik 11 · niaga elektronik 0 | asing dominan |
| manajemen | *startup* 280 (95%) · perusahaan rintisan 14 | asing dominan |
| manajemen | *digital marketing* 417 (78%) · pemasaran digital 116 | asing dominan; padanan masih dipakai |

Pola yang terlihat: padanan menang untuk konsep fisik dan konsep yang sudah lama diajarkan
dalam bahasa Indonesia (mikrokontroler, panel surya, kepuasan pelanggan). Istilah asing menang
untuk konsep komputasi yang baru dan cepat berubah. Padanan resmi yang dibuat belakangan
(*tengkes*, *peladen*, *niaga elektronik*) belum dipakai. Pola ini kecenderungan, bukan aturan:
ukur istilah yang sedang dihadapi.
