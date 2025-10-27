class Univariate():
    
    def quanQual(dataset):
        qual = []
        quan = []
        for columnName in dataset.columns:
            if (dataset[columnName].dtype == 'O'):
                qual.append(columnName)
            else:
                quan.append(columnName)  
        return quan,qual
            
            
        