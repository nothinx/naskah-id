# Catatan sementara

Pekerjaan yang belum selesai setelah rilis 1.1.0 (22 Oktober 2026). Hapus butir yang sudah
dikerjakan; hapus berkas ini bila kosong.

## Belum dikerjakan

- [ ] **Eval penuh.** Sebanyak 20 kasus di `evals/cases.json` belum pernah dijalankan semuanya. Jalankan
  dengan dan tanpa skill, lalu bandingkan skornya:
  `python evals/jalankan.py --agen "claude -p" --penilai "claude -p" --hasil evals/hasil/dengan-skill`.
  Kira-kira 50 panggilan model.
- [ ] **SG-04 berisik di dokumen teknis.** Pada dokumen repo ini SG-04 memberi sekitar 80 temuan
  (MCP, SINTA, COPE tanpa kepanjangan) sehingga CI memakai `--abaikan SG-04`. Uji pada naskah
  ilmiah nyata sebelum memutuskan perlu disaring lagi atau tidak.
- [ ] **Klaim uji abstrak di README** ("menemukan 4, melewatkan 6") berasal dari versi sebelum
  1.0.0. Hitung ulang dengan `periksa.py` sekarang.
- [ ] **Daftar singkatan** di `references/singkatan.md` belum seluruhnya diverifikasi ke sumber
  resmi; yang sudah: nama lembaga yang berubah, BLUe, SRUT, TPA, SKI 2023. Cek kepanjangan
  lainnya, terutama bidang kesehatan dan pendidikan.

## Batas yang diterima

- `openalex.py istilah` bergantung pada cakupan OpenAlex atas jurnal Indonesia dan ikut
  menghitung frasa yang lebih panjang (*interface* menghitung *user interface*).
- Jurnal tanpa DOI tidak bisa diverifikasi otomatis; Garuda tidak punya API.
- Metadata penulis sebagian jurnal OJS rusak sejak di penerbit; skrip hanya memperingatkan.
