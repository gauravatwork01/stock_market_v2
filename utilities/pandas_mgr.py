





class PandasHelper:


    @staticmethod
    def sort(df, cols:list, ascending:list):
        df = df.sort_values(cols, ascending=ascending)
        return df





