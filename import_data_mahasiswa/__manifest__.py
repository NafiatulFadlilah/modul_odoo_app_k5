{
    "name": "Import Data Mahasiswa",
    "version": "1.0.1",
    "category": "Tools",
    "author": "Ibnu Tsalis Assalam",
    "summary": "A module to manage academic data imported from CSV files",
    "depends": ["base"],
    "data": [
        # "views/csv_import_view.xml",
        # "views/mahasiswa_view.xml",
        "views/akademik_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
}
