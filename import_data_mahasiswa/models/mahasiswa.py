# import library yang dibutuhkan
import csv
import base64
from io import StringIO
from odoo import models, fields, api

# definisikan class Mahasiswa yang merupakan models.Model
class Mahasiswa(models.Model):
    # nama tabel di database
    _name = 'mahasiswa.data'
    # nama yang ditampilkan di odoo
    _description = 'Data Mahasiswa'

    # definisikan field-field yang ada di tabel
    nim = fields.Char(string='NIM', required=True)
    nama = fields.Char(string='Nama', required=True)
    kelas = fields.Char(string='Kelas', required=True)
    semester = fields.Char(string='Semester', required=True)
    ipk = fields.Char(string='IPK', required=True)
    # semester = fields.Integer(string='Semester', required=True)
    # ipk = fields.Float(string='IPK', required=True)
    status = fields.Selection([('aktif', 'Aktif'), ('cuti', 'Cuti'), ('lulus', 'Lulus'), ('drop', 'Drop Out')], string='Status', required=True)
    # tambahkan field baru untuk menyimpan file csv
    csv_file = fields.Binary(string='File CSV', compute='generate_csv')
    file_csv = fields.Binary(string='File CSV')

    # definisikan fungsi untuk membaca data dari file .csv
    @api.model
    def read_csv(self, file_path):
        # buka file .csv dengan mode 'r' (read)
        with open(file_path, 'r') as file:
            # baca file dengan menggunakan csv.reader
            reader = csv.reader(file)
            # lewati baris pertama yang berisi header
            next(reader)
            # iterasi setiap baris di file
            for row in reader:
                # ambil data dari setiap kolom
                nim = row[0]
                nama = row[1]
                kelas = row[2]
                # semester = int(row[3])
                # ipk = float(row[4])
                semester = row[3]
                ipk = row[4]
                status = row[5]
                # buat record baru di tabel dengan data yang dibaca
                self.create({
                    'nim': nim,
                    'nama': nama,
                    'kelas': kelas,
                    'semester': semester,
                    'ipk': ipk,
                    'status': status
                })
    
    # definisikan fungsi untuk mengedit data dari file .csv
    @api.model
    def edit_csv(self, file_path):
        # buka file .csv dengan mode 'r' (read)
        with open(file_path, 'r') as file:
            # baca file dengan menggunakan csv.reader
            reader = csv.reader(file)
            # lewati baris pertama yang berisi header
            next(reader)
            # iterasi setiap baris di file
            for row in reader:
                # ambil data dari setiap kolom
                nim = row[0]
                nama = row[1]
                kelas = row[2]
                semester = int(row[3])
                ipk = float(row[4])
                status = row[5]
                # cari record yang sesuai dengan nim
                record = self.search([('nim', '=', nim)])
                # jika record ditemukan, update data dengan data yang dibaca
                if record:
                    record.write({
                        'nama': nama,
                        'kelas': kelas,
                        'semester': semester,
                        'ipk': ipk,
                        'status': status
                    })
    
    # definisikan fungsi untuk menambahkan data dari file .csv
    @api.model
    def add_csv(self, file_path):
        # buka file .csv dengan mode 'r' (read)
        with open(file_path, 'r') as file:
            # baca file dengan menggunakan csv.reader
            reader = csv.reader(file)
            # lewati baris pertama yang berisi header
            next(reader)
            # iterasi setiap baris di file
            for row in reader:
                # ambil data dari setiap kolom
                nim = row[0]
                nama = row[1]
                kelas = row[2]
                semester = row[3]
                ipk = row[4]
                # semester = int(row[3])
                # ipk = float(row[4])
                status = row[5]
                # cari record yang sesuai dengan nim
                record = self.search([('nim', '=', nim)])
                # jika record tidak ditemukan, buat record baru dengan data yang dibaca
                if not record:
                    self.create({
                        'nim': nim,
                        'nama': nama,
                        'kelas': kelas,
                        'semester': semester,
                        'ipk': ipk,
                        'status': status
                    })
    
    # definisikan fungsi untuk menghasilkan file csv dari data mahasiswa
    @api.depends('nim', 'nama', 'kelas', 'semester', 'ipk', 'status')
    def generate_csv(self):
        # buat objek StringIO untuk menyimpan data csv
        output = StringIO()
        # buat objek csv.writer untuk menulis data csv
        writer = csv.writer(output)
        # tulis baris pertama yang berisi header
        writer.writerow(['nim', 'nama', 'kelas', 'semester', 'ipk', 'status'])
        # iterasi setiap record yang ada di self
        for record in self:
            # tulis data record ke baris selanjutnya
            writer.writerow([record.nim, record.nama, record.kelas, record.semester, record.ipk, record.status])
        # encode data csv ke format base64
        csv_data = base64.b64encode(output.getvalue().encode())
        # kembalikan nilai csv_file dengan data csv yang telah diencode
        self.csv_file = csv_data
