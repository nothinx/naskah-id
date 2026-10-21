# Contoh sebelum dan sesudah

Paragraf buatan sendiri untuk menunjukkan cara kerja skill di berbagai bidang. Semua nama,
angka, dan rujukan di sini fiktif. Perhatikan bahwa versi sesudah tidak menambah fakta yang
tidak ada di versi sebelum: angka yang muncul di versi natural sudah ada di versi kaku, dan
informasi yang kurang diganti penanda.

Contoh kutipan dari artikel jurnal sungguhan, beserta lisensinya, ada di `contoh/korpus/`.

## 1. Pendahuluan (teknik)

<!-- periksa:abaikan -->
> **Kaku:** Di era digital ini, tidak dapat dipungkiri bahwa teknologi Internet of Things
> memainkan peran yang sangat penting dalam berbagai macam bidang kehidupan. Hal ini
> menunjukkan bahwa diperlukan adanya suatu sistem di mana data hasil uji emisi kendaraan,
> yang saat ini masih dicatat manual dan memakan waktu sekitar 15 menit per kendaraan, dapat
> dipantau secara real-time. Oleh karena itu, dalam penelitian ini membahas perancangan sistem
> pemantauan uji emisi.
<!-- periksa:lanjut -->

> **Natural:** Hasil uji emisi kendaraan masih dicatat manual dan memakan waktu sekitar 15 menit
> per kendaraan. Penelitian ini merancang sistem berbasis *Internet of Things* (IoT) untuk
> memantau hasil uji emisi secara langsung (*real-time*).

Yang diubah: pembuka kosmik dan penegas dibuang (AI-01, AI-03), `memainkan peran` (AI-05),
`berbagai macam` (KE-06), `di mana` (AI-14), dan subjek yang hilang (KE-01). Angka 15 menit
berasal dari versi kaku.

## 2. Metode (teknik)

<!-- periksa:abaikan -->
> **Kaku:** Telah dilakukan pengukuran terhadap tegangan keluaran oleh peneliti dengan
> menggunakan osiloskop, yang mana pengukuran tersebut dilakukan sebanyak 3 kali pengulangan
> di mana setiap pengulangan dilakukan pada suhu 25 derajat Celcius.
<!-- periksa:lanjut -->

> **Natural:** Tegangan keluaran diukur dengan osiloskop sebanyak tiga kali pada suhu 25 °C.

Satu kalimat 32 kata menjadi 12 kata tanpa kehilangan informasi. Pasif "diukur" dipertahankan
karena ini prosedur.

## 3. Hasil (teknik)

<!-- periksa:abaikan -->
> **Kaku:** Dari hasil pengujian menunjukkan bahwa nilai error rata-rata mengalami penurunan
> dari 4,8% menjadi 1,2% yang sangat signifikan sekali (uji-t, p < 0,01) setelah filter Kalman
> diterapkan untuk meredam derau sensor. Hal ini menunjukkan bahwa metode yang diusulkan adalah merupakan metode yang
> efektif.
<!-- periksa:lanjut -->

> **Natural:** Setelah filter Kalman diterapkan, galat rata-rata turun dari 4,8% menjadi 1,2%
> (uji-*t*, *p* < 0,01). Penurunan ini menunjukkan bahwa filter Kalman efektif meredam derau
> pembacaan sensor.

"Filter Kalman" dipertahankan karena itu istilah yang lazim di jurnal teknik. "Error" diganti
"galat", padanan yang sudah hidup di bidang ini. `Sangat signifikan sekali` menjadi nilai uji
saja (AI-12, KE-04).

## 4. Tinjauan pustaka (teknik)

<!-- periksa:abaikan -->
> **Kaku:** Menurut Santoso [1] mengatakan bahwa sensor ultrasonik akurat untuk jarak di bawah
> 4 m. Selain itu, menurut Putri [2] menyatakan bahwa sensor ultrasonik murah. Selain itu,
> menurut Hadi [3] mengatakan bahwa sensor ultrasonik terpengaruh suhu, sehingga Hadi menambahkan
> kompensasi suhu yang menurunkan galat hingga separuhnya.
<!-- periksa:lanjut -->

> **Natural:** Sensor ultrasonik murah dan cukup akurat untuk jarak di bawah 4 m [1], [2].
> Kelemahannya, cepat rambat bunyi bergantung pada suhu sehingga Hadi [3] menambahkan
> kompensasi suhu dan menurunkan galat hingga separuhnya.

Sumber dikelompokkan menurut temuan. Sitasi [1], [2], dan [3] tetap melekat pada klaim yang
sama seperti di versi kaku.

## 5. Simpulan (teknik)

<!-- periksa:abaikan -->
> **Kaku:** Dengan demikian dapat disimpulkan bahwa secara keseluruhan sistem yang dirancang
> telah berhasil berjalan dengan baik pada 48 dari 50 uji dan dapat menjadi salah satu solusi
> yang inovatif. Adapun 2 kegagalan terjadi pada saat sinyal seluler lemah.
<!-- periksa:lanjut -->

> **Natural:** Sistem bekerja sesuai rancangan pada 48 dari 50 uji. Dua kegagalan terjadi saat
> sinyal seluler lemah. [PERLU DATA: rencana penanganan sinyal lemah, bila ingin dijadikan
> saran]

## 6. Latar belakang (kesehatan masyarakat)

<!-- periksa:abaikan -->
> **Kaku:** Seiring dengan perkembangan zaman, stunting masih menjadi permasalahan yang sangat
> krusial di Indonesia. Hal ini dapat dilihat dari prevalensi stunting yang masih tinggi. Selain
> itu, stunting memberikan pengaruh terhadap perkembangan kognitif anak. Oleh karena itu,
> diperlukan adanya upaya pencegahan yang efektif, efisien, dan inovatif.
<!-- periksa:lanjut -->

> **Natural:** Prevalensi *stunting* pada balita Indonesia masih tinggi [PERLU DATA: angka
> prevalensi terbaru dan sumbernya, misalnya SSGI]. *Stunting* memengaruhi perkembangan kognitif
> anak [PERLU RUJUKAN: dampak stunting pada perkembangan kognitif]. [PERLU DATA: bentuk upaya
> pencegahan yang diteliti]

Versi kaku tidak memuat angka prevalensi, jadi versi natural tidak mengarangnya. Kalimat
"diperlukan upaya pencegahan yang efektif, efisien, dan inovatif" tidak berisi apa pun yang bisa
diuji sehingga diganti penanda: pengguna perlu menyebut upaya apa yang diteliti.

## 7. Hasil (sosiologi, kualitatif)

<!-- periksa:abaikan -->
> **Kaku:** Berdasarkan pada hasil wawancara yang telah dilakukan oleh peneliti terhadap para
> informan-informan, dapat diketahui bahwa peran tokoh adat adalah merupakan faktor yang sangat
> penting sekali dalam penyelesaian konflik lahan. Hal ini sebagaimana yang disampaikan oleh
> informan 3 (Ketua Adat): "Kalau sudah dibawa ke balai, orang malu melawan."
<!-- periksa:lanjut -->

> **Natural:** Menurut para informan, tokoh adat berperan penting dalam penyelesaian konflik
> lahan. Informan 3 (ketua adat) mengatakan, "Kalau sudah dibawa ke balai, orang malu melawan."

Kutipan informan tidak disunting sama sekali, termasuk ragam lisannya. "Ketua Adat" ditulis
huruf kecil karena tidak diikuti nama orang.

## 8. Metode (pendidikan)

<!-- periksa:abaikan -->
> **Kaku:** Adapun penelitian ini adalah merupakan penelitian tindakan kelas yang dilaksanakan
> dalam 2 siklus, di mana setiap siklusnya terdiri dari tahap perencanaan, pelaksanaan,
> observasi, dan refleksi. Subyek penelitian adalah 32 siswa kelas V SD Negeri 4 Contoh.
<!-- periksa:lanjut -->

> **Natural:** Penelitian tindakan kelas ini dilaksanakan dalam dua siklus. Setiap siklus
> terdiri atas perencanaan, pelaksanaan, observasi, dan refleksi. Subjek penelitian adalah 32
> siswa kelas V SD Negeri 4 Contoh.

## 9. Pembahasan (sejarah)

<!-- periksa:abaikan -->
> **Kaku:** Lebih dari sekadar dokumen administratif, arsip residen ini adalah cermin dari
> kompleksitas relasi kuasa kolonial. Tidak dapat dipungkiri bahwa arsip tersebut ditulis dari
> sudut pandang pemerintah kolonial, yang mana hal ini perlu diperhatikan. Dalam arsip tertulis
> "de inlandsche hoofden waren onwillig" (para kepala pribumi enggan).
<!-- periksa:lanjut -->

> **Natural:** Arsip residen ini ditulis dari sudut pandang pemerintah kolonial sehingga
> keengganan para kepala pribumi yang dicatatnya ("de inlandsche hoofden waren onwillig") perlu
> dibaca bersama sumber lain. [PERLU RUJUKAN: sumber pembanding, misalnya babad atau surat
> kabar sezaman]

Ejaan lama dalam kutipan arsip dipertahankan. Kalimat panjang wajar dalam naskah sejarah
selama induk kalimatnya jelas.

## 10. Abstrak (keperawatan)

<!-- periksa:abaikan -->
> **Kaku:** Kecemasan pre operasi merupakan masalah yang sering dialami pasien. Penelitian ini
> bertujuan untuk mengetahui pengaruh terapi musik terhadap kecemasan pasien pre operasi.
> Metode yang digunakan adalah quasi eksperimen dengan 40 responden. Hasil penelitian
> menunjukkan bahwa terdapat pengaruh yang sangat signifikan (p = 0,001). Dengan demikian
> terapi musik dapat menjadi solusi yang inovatif.
<!-- periksa:lanjut -->

> **Natural:** Kecemasan praoperasi sering dialami pasien bedah. Penelitian ini menguji
> pengaruh terapi musik terhadap kecemasan pasien praoperasi dengan desain kuasi-eksperimen
> pada 40 responden. Terapi musik berpengaruh signifikan terhadap skor kecemasan (*p* = 0,001).
> [PERLU DATA: skor kecemasan sebelum dan sesudah, instrumen yang dipakai] Terapi musik dapat
> dipertimbangkan sebagai intervensi pendamping sebelum operasi.

"Pre operasi" menjadi "praoperasi" (bentuk terikat serangkai). Arah pengaruh ("menurunkan")
tidak ditulis karena versi kaku hanya menyebut "terdapat pengaruh". Bila pengguna
mengonfirmasi bahwa skor turun, abstrak boleh memakai "menurunkan" beserta angkanya.
