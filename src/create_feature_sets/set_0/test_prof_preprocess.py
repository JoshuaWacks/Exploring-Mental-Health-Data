import pandas as pd

class TestPreprocess:
    def __init__(self, df,cols_to_drop,imputer,cat_encoding_type,is_student):
        self.df = df
        self.cols_to_drop = cols_to_drop
        self.imputer = imputer
        self.cat_encoding_type = cat_encoding_type
        self.is_student = is_student
        

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
    
    def __fix_invalid_profression(self):
        self.df.loc[self.df['Profession'] == 'Medical Doctor','Profession'] = 'Doctor'

    def __fix_invalid_sleep_duration(self):
        self.df.loc[self.df['Sleep Duration'] == '2-3 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '3-4 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '1-2 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '4-5 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '4-6 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '1-6 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '2-3 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == 'Unhealthy','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '3-6 hours','Sleep Duration'] = 'Less than 5 hours'
        self.df.loc[self.df['Sleep Duration'] == '1-3 hours','Sleep Duration'] = 'Less than 5 hours'


        self.df.loc[self.df['Sleep Duration'] == '6-8 hours','Sleep Duration'] = '7-8 hours'
        self.df.loc[self.df['Sleep Duration'] == '10-6 hours','Sleep Duration'] = '7-8 hours'
        self.df.loc[self.df['Sleep Duration'] == '9-6 hours','Sleep Duration'] = '7-8 hours'
        self.df.loc[self.df['Sleep Duration'] == 'Moderate','Sleep Duration'] = '7-8 hours'


        self.df.loc[self.df['Sleep Duration'] == '6-7 hours','Sleep Duration'] = '5-6 hours'
        self.df.loc[self.df['Sleep Duration'] == '9-5 hours','Sleep Duration'] = '5-6 hours'
        self.df.loc[self.df['Sleep Duration'] == '9-5 hours','Sleep Duration'] = '5-6 hours'
        self.df.loc[self.df['Sleep Duration'] == '9-5','Sleep Duration'] = '5-6 hours'

        self.df.loc[self.df['Sleep Duration'] == '9-11 hours','Sleep Duration'] = 'More than 8 hours'
        self.df.loc[self.df['Sleep Duration'] == '8-9 hours','Sleep Duration'] = 'More than 8 hours'
        self.df.loc[self.df['Sleep Duration'] == '10-11 hours','Sleep Duration'] = 'More than 8 hours'
        self.df.loc[self.df['Sleep Duration'] == '8 hours','Sleep Duration'] = 'More than 8 hours'

    def __fix_invalid_dietary_habits(self):
        self.df.loc[self.df['Dietary Habits'] == 'More Healthy','Dietary Habits'] = 'Healthy'
        self.df.loc[self.df['Dietary Habits'] == 'Less than Healthy','Dietary Habits'] = 'Unhealthy'
        self.df.loc[self.df['Dietary Habits'] == 'No Healthy','Dietary Habits'] = 'Unhealthy'
        self.df.loc[self.df['Dietary Habits'] == 'Less Healthy','Dietary Habits'] = 'Unhealthy'

    def __fix_invalid_degrees(self):
        self.df.loc[self.df['Degree'] == 'Doctor','Degree'] = 'MD'

    def fix_erronous_data(self):

        if not self.is_student:
            self.__fix_invalid_profression()

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