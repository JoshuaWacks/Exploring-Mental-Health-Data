import pandas as pd

class StudentPreprocessSet0:
    def __init__(self, df,cols_to_drop,imputer,cat_encoding_type):
        self.df = df
        self.cols_to_drop = cols_to_drop
        self.imputer = imputer
        self.cat_encoding_type = cat_encoding_type
        

    def preprocess(self):
        # First fix the incorrectly captured data
        self.fix_erronous_data()
        
        # Get the numeric and categorical data
        self.numeric_cols,self.categorical_cols = self.get_column_types()

        # Fill in missing values
        self.fill_in_missing_numerical_values()
        self.fill_in_missing_cat_values()

        # Encoding categorical data
        self.encode_cat_data()

    def drop_cols(self):
        for col in self.cols_to_drop:
            self.df.drop(columns=col,inplace=True)

    def get_column_types(self):
        categorical_cols = []
        numeric_cols = []

        for col in self.df.columns:
            if self.df[col].dtype == object:
                categorical_cols.append(col)
            else:
                numeric_cols.append(col)

        return numeric_cols,categorical_cols
    
    def __fix_invalid_cities(self):
        
        invalid_values = ['3.0']
        self.df = self.df[~self.df['City'].isin(invalid_values)]

    def __fix_invalid_sleep_duration(self):
        self.df.loc[self.df['Sleep Duration'] == '10-11 hours','Sleep Duration'] = 'More than 8 hours'
        self.df.loc[self.df['Sleep Duration'] == '2-3 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '3-4 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '1-2 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '4-5 hours','Sleep Duration'] = 'Less than 5 hours'

        self.df.loc[self.df['Sleep Duration'] == 'Moderate','Sleep Duration'] = '7-8 hours'
        self.df.loc[self.df['Sleep Duration'] == '8 hours','Sleep Duration'] = 'More than 8 hours'

        self.df.loc[self.df['Sleep Duration'] == '6-7 hours','Sleep Duration'] = '5-6 hours'

        invalid_values = ['40-45 hours','55-66 hours','than 5 hours','45']
        self.df = self.df[~self.df['Sleep Duration'].isin(invalid_values)]

    def __fix_invalid_dietary_habits(self):
        self.df.loc[self.df['Dietary Habits'] == 'Less than Healthy','Dietary Habits'] = 'Unhealthy'
        self.df.loc[self.df['Dietary Habits'] == 'No Healthy','Dietary Habits'] = 'Unhealthy'
        self.df.loc[self.df['Dietary Habits'] == 'Less Healthy','Dietary Habits'] = 'Unhealthy'


        invalid_values = ['3','Mihir','1.0','M.Tech','Male','Yes','2']
        self.df = self.df[~self.df['Dietary Habits'].isin(invalid_values)]

    def __fix_invalid_degrees(self):
        invalid_values = ['B','24','7.06','M','20','0',]
        self.df = self.df[~self.df['Degree'].isin(invalid_values)]

    def fix_erronous_data(self):

        self.__fix_invalid_cities()
        self.__fix_invalid_sleep_duration()
        self.__fix_invalid_dietary_habits()
        self.__fix_invalid_degrees()
    
    def fill_in_missing_numerical_values(self):

        for col in self.numeric_cols:
            if sum(pd.isnull(self.df[col])) > 0:
                self.df[col] = self.imputer.fit_transform(self.df[[col]])

    def fill_in_missing_cat_values(self):

        for col in self.categorical_cols:
            self.df[col] = self.df[col].fillna(self.df[col].mode().iloc[0])
    
    def encode_cat_data(self):

        if self.cat_encoding_type == 'frequency':
            for col in self.categorical_cols:
                freq = self.df[col].value_counts(normalize= True)
                self.df[col] = self.df[col].map(freq)