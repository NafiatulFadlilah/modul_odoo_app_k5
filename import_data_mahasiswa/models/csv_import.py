from odoo import models, fields, api

class CsvImport(models.Model):
    _name = "csv.import"
    _description = "CSV Import"

    name = fields.Char(string="Name", required=True)
    csv_file = fields.Binary(string="CSV File", required=True)
    csv_filename = fields.Char(string="CSV Filename")
    state = fields.Selection([ 
        ("draft", "Draft"),
        ("done", "Done"),
    ], string="State", default="draft")

    @api.model
    def create(self, vals):
        # Override the create method to import data from the csv file
        record = super(CsvImport, self).create(vals)
        record.import_data()
        return record

    def import_data(self):
        # Import data from the csv file
        import csv
        import base64
        csv_data = base64.b64decode(self.csv_file).decode("utf-8")
        reader = csv.reader(csv_data.splitlines(), delimiter=",")
        header = next(reader) # Skip the header row
        for row in reader:
            # Create or update a record based on the csv row
            # You can customize this logic according to your needs
            # For example, you can use the external ID or a unique field to identify the record
            # You can also use the Odoo API methods such as search, write, or unlink
            # Here we assume the first column is the external ID and the rest are the field values
            ext_id = row[0]
            values = dict(zip(header[1:], row[1:]))
            record = self.env.ref(ext_id, raise_if_not_found=False)
            if record:
                # Update the existing record
                record.write(values)
            else:
                # Create a new record
                self.env["model.name"].create(values)
        # Change the state to done
        self.state = "done"
