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
            
            
    def frequency(columnName,dataset):
        freq_table = pd.DataFrame(columns = ["Unique_values", "Frequency", "Relative_Frequency", "Cusum_Frequency"])
        freq_table["Unique_values"] = dataset[columnName].value_counts().index
        freq_table["Frequency"] = dataset[columnName].value_counts().values
        freq_table["Relative_Frequency"] = freq_table["Frequency"]/103
        freq_table["Cusum_Frequency"] = freq_table["Relative_Frequency"].cumsum()
        return freq_table

    def Univariate(quan,dataset,pd):
        tbl_format_IQR = pd.DataFrame(index=["Mean", "Median", "Mode","Q1:25%","Q2:50%","Q3:75%","Q4:100%","IQR",             "1.5IQR","LesserOutlier","GreaterOutlier","min","max","kurtosis","skew"], columns = quan)

        for columnName in quan:
            tbl_format_IQR[columnName]["Mean"] = dataset[columnName].mean()
            tbl_format_IQR[columnName]["Median"] = dataset[columnName].median()
            tbl_format_IQR[columnName]["Mode"] = dataset[columnName].mode()[0]
           
            #So we accesing the salary value from the table directly dataset.describe
            tbl_format_IQR[columnName]["Q1:25%"] = dataset.describe()[columnName]["25%"]
            tbl_format_IQR[columnName]["Q2:50%"] = dataset.describe()[columnName]["50%"]
            tbl_format_IQR[columnName]["Q3:75%"] = dataset.describe()[columnName]["75%"]
            tbl_format_IQR[columnName]["Q4:100%"] = dataset.describe()[columnName]["max"]
            #IQR = Q3-Q1
            tbl_format_IQR[columnName]["IQR"] = tbl_format_IQR[columnName]["Q3:75%"] - tbl_format_IQR[columnName]["Q1:25%"]
            tbl_format_IQR[columnName]["1.5IQR"] = 1.5 * tbl_format_IQR[columnName]["IQR"]
            #Lesser = Q1-1.5IQR
            tbl_format_IQR[columnName]["LesserOutlier"] = tbl_format_IQR[columnName]["Q1:25%"] - tbl_format_IQR[columnName]["1.5IQR"]
            #Greater = Q3+1.5IQR
            tbl_format_IQR[columnName]["GreaterOutlier"] = tbl_format_IQR[columnName]["Q3:75%"] + tbl_format_IQR[columnName]["1.5IQR"]
            tbl_format_IQR[columnName]["min"] = dataset.describe()[columnName]["min"]
            tbl_format_IQR[columnName]["max"] = dataset.describe()[columnName]["max"]
            tbl_format_IQR[columnName]["skew"] = dataset[columnName].skew()
            tbl_format_IQR[columnName]["kurtosis"] = dataset[columnName].kurtosis()

        return tbl_format_IQR


    def FindOutliers(quan, tbl_format_IQR):
        #Finding outliers

        lesserOutlier = []
        greaterOutlier =[]
        
        for columnName in quan:
            if tbl_format_IQR[columnName]["min"] < tbl_format_IQR[columnName]["LesserOutlier"]:
                lesserOutlier.append(columnName)
            if tbl_format_IQR[columnName]["GreaterOutlier"] < tbl_format_IQR[columnName]["max"]:
                greaterOutlier.append(columnName)
        
        print(lesserOutlier,"\n",greaterOutlier)

        return lesserOutlier,greaterOutlier

    def ReplaceOutliers(lesserOutlier, greaterOutlier, dataset, tbl_format_IQR):
        for colName in lesserOutlier:
            dataset[colName][dataset[colName] < tbl_format_IQR[colName]["LesserOutlier"]] = tbl_format_IQR[colName]["LesserOutlier"]
    
        for columnName in greaterOutlier:
            dataset[columnName][dataset[columnName]>tbl_format_IQR[columnName]["GreaterOutlier"]] = tbl_format_IQR[columnName]["GreaterOutlier"]