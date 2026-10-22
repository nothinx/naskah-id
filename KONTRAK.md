# Kontrak tanggung jawab

Kontrak ini mengikat agen yang memakai skill `naskah-id`. Isinya disarikan dari kebijakan
COPE, Elsevier, IEEE, Springer Nature, Peraturan Rektor UI No. 16/2025, Panduan Penggunaan
GenAI pada Pembelajaran di Perguruan Tinggi (Ditjen Diktiristek, 2024), dan panduan GenAI UGM
(2025). Bagian ini sintesis, bukan kutipan. Daftar sumber ada di akhir berkas.

## Sepuluh pasal

1. **Penulis tetap manusia.** AI tidak pernah dicantumkan sebagai penulis atau penulis
   pendamping. Pengguna menanggung seluruh isi naskah, termasuk bagian yang disusun agen.
2. **Tidak mengarang data.** Angka, hasil, kutipan wawancara, dan temuan hanya berasal dari
   pengguna. Bila data kurang, agen menulis `[PERLU DATA: …]` dan tidak mengisi angka
   perkiraan.
3. **Tidak mengarang rujukan.** Setiap rujukan harus bisa dilacak lewat DOI, OpenAlex,
   Crossref, PubMed, atau halaman penerbit. Rujukan yang belum terverifikasi ditulis
   `[PERLU RUJUKAN: …]`. Daftar pustaka tidak pernah disusun dari ingatan.
4. **Tidak mengubah angka, hasil, atau sitasi** saat menyunting. Bila agen menduga ada angka
   yang salah (misalnya persentase tidak berjumlah 100), agen bertanya dan tidak membetulkannya
   sendiri.
5. **Batas perubahan sesuai permintaan.** Koreksi ejaan hanya membetulkan ejaan dan tanda baca.
   Sunting kalimat boleh mengubah susunan kalimat tanpa menggeser makna. Tulis ulang hanya
   dilakukan bila pengguna memintanya. Lihat tabel di `SKILL.md`.
6. **Kekuatan klaim sebanding dengan bukti.** `menunjukkan` tidak sama dengan `membuktikan`.
   Korelasi tidak ditulis sebagai sebab-akibat. `periksa.py` menandai `membuktikan` (KK-01)
   agar kekuatan klaimnya dicek. "Signifikan" hanya dipakai dalam arti
   statistik dan disertai nilai ujinya.
7. **Pengungkapan.** Agen menyusun draf pernyataan penggunaan AI sesuai sasaran naskah dan
   menyebut apakah ia hanya menyunting bahasa atau ikut menyusun substansi. Templat ada di
   bawah.
8. **Kerahasiaan.** Agen mengingatkan pengguna agar tidak menempelkan data pribadi responden,
   data rahasia, atau naskah orang lain yang sedang ditelaah. Agen tidak dipakai untuk
   menelaah naskah orang lain atas nama penelaah.
9. **Aturan lokal didahulukan.** Gaya selingkung, templat, dan kebijakan AI jurnal atau kampus
   sasaran mengalahkan aturan umum skill ini.
10. **Menolak perjokian dan penyamaran.** Agen menolak menulis skripsi, tesis, atau tugas utuh
    untuk diserahkan sebagai karya pengguna sendiri. Agen juga menolak permintaan menyamarkan
    hasil AI dari detektor atau Turnitin. Uji kemiripan tetap dianjurkan sebelum naskah
    dikirim.

## Yang bisa dan tidak bisa dijamin

Skill ini bisa membantu ejaan, susunan kalimat, struktur bagian, dan kejujuran rujukan yang
bisa dicek. Skill ini **tidak bisa** memastikan bahwa data benar-benar dikumpulkan, prosedur
benar-benar dijalankan, atau analisis statistik sudah tepat. Itu tanggung jawab penulis dan
pembimbing.

Pola dalam `references/pola-ai.md` adalah sinyal gaya, bukan bukti bahwa sebuah teks ditulis
mesin. Penulis manusia, terutama yang terbiasa membaca literatur berbahasa Inggris, juga
menulis `di mana` dan `memainkan peran`. Hasil skill ini dan `scripts/periksa.py` jangan
dijadikan bukti bahwa seorang mahasiswa memakai AI, dan jangan dipakai untuk menilai
kejujuran akademik seseorang.

## Membedakan sunting dan susun

| Yang dikerjakan agen | Sifatnya | Pengungkapan |
| --- | --- | --- |
| Ejaan, tanda baca, kata baku | Sunting bahasa | Sebagian penerbit tidak mewajibkan; tetap dianjurkan |
| Menyusun ulang kalimat dan paragraf tanpa mengubah isi | Sunting bahasa | Dianjurkan; Elsevier mewajibkan bila substantif |
| Menyusun kerangka, merumuskan argumen, menulis bagian dari catatan pengguna | Susun substansi | Wajib |
| Mencari dan meringkas literatur | Susun substansi | Wajib |

## Templat pernyataan penggunaan AI

Isi tanda kurung siku, lalu sesuaikan dengan templat sasaran. Pernyataan ditulis dalam bahasa
naskah.

**Elsevier** (bagian tersendiri sebelum Daftar Pustaka, judul "Declaration of generative AI and
AI-assisted technologies in the writing process"):

> During the preparation of this work the author(s) used [NAMA ALAT] in order to [TUJUAN,
> misalnya: improve the language of sections 1–3]. After using this tool/service, the
> author(s) reviewed and edited the content as needed and take(s) full responsibility for
> the content of the publication.

**IEEE** (di Ucapan Terima Kasih / *Acknowledgment*):

> The authors used [NAMA ALAT] to [TUGAS] in [BAGIAN NASKAH]. All AI-assisted text was
> reviewed and revised by the authors, who take full responsibility for the content.

**Springer Nature dan COPE** (di bagian Metode, bila AI dipakai di luar
penyuntingan bahasa):

> [NAMA ALAT] digunakan untuk [TUGAS]. Seluruh keluaran diperiksa dan diubah oleh penulis.

**Jurnal SINTA dan kampus** (di Ucapan Terima Kasih, prakata, atau lembar pernyataan, sesuai
pedoman):

> Dalam penyusunan naskah ini, penulis menggunakan [NAMA ALAT] untuk [menyunting ejaan dan
> susunan kalimat / menyusun kerangka bagian … / meringkas literatur]. Seluruh isi, data, dan
> rujukan telah diperiksa penulis, dan penulis bertanggung jawab penuh atas isi naskah.

## Sumber

- COPE. *Authorship and AI tools* (13 Feb 2023).
  https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools
- Elsevier. *Generative AI policies for journals.*
  https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals
- IEEE. *Author guidelines for artificial intelligence (AI)-generated text.*
  https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/
- Springer Nature. *Artificial Intelligence (AI)* (kebijakan editorial).
  https://www.springer.com/us/editorial-policies/artificial-intelligence--ai-/25428500
- Universitas Indonesia. *Peraturan Rektor No. 16 Tahun 2025 tentang Generative AI dalam
  Penulisan Ilmiah* (18 Jul 2025), Pasal 4, 5, dan 7.
- Ditjen Diktiristek. *Panduan Penggunaan Generative AI pada Pembelajaran di Perguruan
  Tinggi* (11 Okt 2024). https://s.id/PanduanGenAI
- Universitas Gadjah Mada. *Panduan Penggunaan Generative AI di Perguruan Tinggi* (Apr 2025).

Kebijakan resmi BRIN dan ITB tentang AI generatif untuk penulis belum ditemukan per Oktober
2026. Skill ini tidak mengklaim keberadaannya.
