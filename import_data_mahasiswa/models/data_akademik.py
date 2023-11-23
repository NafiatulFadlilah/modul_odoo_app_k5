# import library yang dibutuhkan
import csv
import base64
from io import StringIO
from odoo import models, fields, api, exceptions
from .json_field import JsonField

# definisikan class WizardReadCSV yang merupakan models.TransientModel
class WizardDataAkademikCSV(models.TransientModel):
    # nama tabel di database
    _name = 'wizard.dataakademik.csv'
    # nama yang ditampilkan di odoo
    _description = 'Wizard Baca Data Akademik Mahasiswa dari CSV'

    # definisikan field file_path yang bertipe Char
    file_csv = fields.Binary(string='File CSV', required=True)

    # definisikan fungsi untuk membaca data dari file .csv
    def read_csv(self):
        # ambil objek dari models mahasiswa.data
        akademik = self.env['mahasiswa.dataakademik']
        # ambil nilai dari field file_path
        file_csv = self.file_csv
        # panggil fungsi read_csv dari models mahasiswa.data dengan parameter file_path
        akademik.read_csv(file_csv)
        # kembalikan action untuk menutup wizard
        # akademik.action_akademik()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mahasiswa.dataakademik',
            'view_mode': 'tree,form',
            'view_type': 'form'
        }

# definisikan class Mahasiswa yang merupakan models.Model
class DataAkademik(models.Model):
    # nama tabel di database
    _name = 'mahasiswa.dataakademik'
    # nama yang ditampilkan di odoo
    _description = 'Data Akademik Mahasiswa'

    # definisikan field-field yang ada di tabel
    nim = fields.Char(string='NIM', required=True)
    nama = fields.Char(string='Nama', required=True)
    nilai = JsonField(string="Kumpulan Nilai")
    prestasi = fields.Integer(string='Total Prestasi', required=True)
    kompen = fields.Integer(string='Total Kompen', required=True)

    # definisikan fungsi untuk membaca data dari file .csv
    @api.model
    def read_csv(self, file_csv):
        # buka file .csv dengan mode 'r' (read)
        csv_data = base64.b64decode(file_csv).decode("utf-8")
        reader = csv.reader(csv_data.splitlines(), delimiter=",")
        # lewati baris pertama yang berisi header
        header = next(reader)
        # iterasi setiap baris di file
        for row in reader:
            # ambil data dari setiap kolom
            nim = row[0]
            nama = row[1]
            nilai = {}
            for n in range(3,len(header)-2):
                nilai[header[n]] = float(row[n])
            prestasi = 1 #sementara 1
            alpaku = int(row[len(row)-1])
            # buat record baru di tabel dengan data yang dibaca
            record = self.search([('nim', '=', nim)])
            # jika record tidak ditemukan, buat record baru dengan data yang dibaca
            if not record:
                self.create({
                    'nim': nim,
                    'nama': nama,
                    'nilai': nilai,
                    'prestasi': prestasi,
                    'kompen': alpaku,
                })
            else:    
                record.write({
                    'nama': nama,
                    'nilai': nilai,
                    'prestasi': prestasi,
                    'kompen': alpaku,
                })

    def action_akademik(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('import_data_mahasiswa.action_akademik').read()[0]
    
    # definisikan fungsi untuk memanggil action untuk membuka wizard untuk read_csv
    def action_akademik_read_csv(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('import_data_mahasiswa.action_akademik_read_csv').read()[0]
