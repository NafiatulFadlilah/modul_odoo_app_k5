# Import the odoo models module
from odoo import models, fields, api
# Import the numpy and pandas libraries
# import numpy as np
# import pandas as pd
# Import the base64 library
import base64

# Define the class for the wizard_readCsv model
class Wizard_readCsv(models.TransientModel):
    # Define the name of the model
    _name = "wizard.readcsv"
    # Define the description of the model
    _description = "Wizard to read csv file as input for the selection calculation"

    # Define the fields for the model
    # The file field will store the binary data of the csv file
    file = fields.Binary(string="File CSV", required=True)
    # The filename field will store the name of the csv file
    filename = fields.Char(string="Filename")

    # Define a method to read the csv file and return the dataframe
    @api.model
    def read_csv(self):
        # Decode the binary data of the file field
        data = base64.b64decode(self.file)
        # Read the csv file as a dataframe
        df = pd.read_csv(data)
        # Return the dataframe
        return df

    # Define a method to get the criteria and alternatives from the dataframe
    @api.model
    def get_criteria_alternatives(self):
        # Define the criteria and alternatives
        criteria = ["Nilai Prestasi", "Manajemen Proyek", "Keamanan Informasi", "E-Business", "Pemrograman Platform Bergerak (Mobile)", "Sistem Pendukung Keputusan", "Pengolahan Citra Digital", "Proyek Tingkat III", "Alpaku"]
        alternatives = df["Nama"]

        # Extract the decision matrix from the dataframe
        matrix = df[criteria].to_numpy()

        # Return the criteria, alternatives, and matrix
        return criteria, alternatives, matrix

    # Define a method to calculate the weights using ROC method
    @api.model
    def calculate_weights(self):
        # Define the rank of the criteria
        rank = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # Calculate the length of the rank list
        n = len(rank)
        # Initialize an empty list for the weights
        weights = []
        # Loop through each value in the rank list
        for i in rank:
            # Calculate the weight for each value
            w = sum([1 / (n - j + 1) for j in range(i, n + 1)]) / n
            # Append the weight to the list
            weights.append(w)
        # Convert the list to a numpy array
        weights = np.array(weights)
        # Return the weights
        return weights

    # Define a method to normalize the matrix using vector normalization
    @api.model
    def normalize_matrix(self):
        # Get the matrix from the get_criteria_alternatives method
        criteria, alternatives, matrix = self.get_criteria_alternatives()
        # Normalize the matrix using vector normalization
        norm_matrix = matrix / np.sqrt(np.sum(matrix ** 2, axis=0))
        # Return the normalized matrix
        return norm_matrix

    # Define a method to calculate the weighted normalized matrix
    @api.model
    def calculate_weighted_matrix(self):
        # Get the normalized matrix from the normalize_matrix method
        norm_matrix = self.normalize_matrix()
        # Get the weights from the calculate_weights method
        weights = self.calculate_weights()
        # Calculate the weighted normalized matrix
        weighted_matrix = norm_matrix * weights
        # Return the weighted normalized matrix
        return weighted_matrix

    # Define a method to separate the benefit and cost criteria from the weighted matrix
    @api.model
    def separate_benefit_cost(self):
        # Get the weighted normalized matrix from the calculate_weighted_matrix method
        weighted_matrix = self.calculate_weighted_matrix()
        # Separate the benefit and cost criteria from the weighted matrix
        benefit_criteria = weighted_matrix[:, :-1]  # All columns except the last one
        cost_criteria = weighted_matrix[:, -1]  # The last column
        # Return the benefit and cost criteria
        return benefit_criteria, cost_criteria

    # Define a method to calculate the MOORA ratio for each alternative
    @api.model
    def calculate_ratio(self):
        # Get the benefit and cost criteria from the separate_benefit_cost method
        benefit_criteria, cost_criteria = self.separate_benefit_cost()
        # Calculate the MOORA ratio for each alternative
        ratio = np.sum(benefit_criteria, axis=1) - cost_criteria
        # Return the ratio
        return ratio

    # Define a method to rank the alternatives based on the MOORA ratio
    @api.model
    def rank_alternatives(self):
        # Get the alternatives and ratio from the get_criteria_alternatives and calculate_ratio methods
        criteria, alternatives, matrix = self.get_criteria_alternatives()
        ratio = self.calculate_ratio()
        # Create a dataframe with the alternative and ratio columns
        rank_df = pd.DataFrame({"Alternative": alternatives, "Ratio": ratio})
        # Sort the dataframe by the ratio column in descending order
        rank_df = rank_df.sort_values(by="Ratio", ascending=False)
        # Reset the index of the dataframe
        rank_df = rank_df.reset_index(drop=True)
        # Return the dataframe
        return rank_df
    
    # Define a method to display the ranking result
    @api.model
    def display_result(self):
        # Get the dataframe from the rank_alternatives method
        rank_df = self.rank_alternatives()
        # Print the result
        print("The ranking of the alternatives based on the MOORA method are:")
        print(rank_df)

# Define the class for the rank_model model
class Rank_model(models.Model):
    # Define the name of the model
    _name = "rank.model"
    # Define the description of the model
    _description = "Model to store the ranking result"

    # Define the fields for the model
    # The name field will store the name of the alternative
    name = fields.Char(string="Name", required=True)
    # The ratio field will store the MOORA ratio of the alternative
    ratio = fields.Float(string="Ratio", required=True)
    # The rank field will store the rank of the alternative
    rank = fields.Integer(string="Rank", required=True)

    # Define a method to create records from the rank_df dataframe
    @classmethod
    def create_from_df(cls, rank_df):
        # Ensure that only one record is created
        self.ensure_one()
        # Loop through each row of the dataframe
        for index, row in rank_df.iterrows():
            # Create a dictionary with the field values
            vals = {
                "name": row["Alternative"],
                "ratio": row["Ratio"],
                "rank": index + 1
            }
            # Create a record with the dictionary
            cls.create(vals)

