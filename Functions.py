import pandas as pd
import requests as rq

def loadCSV(filePath):
    data=pd.read_csv(filePath)
    df=pd.DataFrame(data)
    return df
    
def loadExcel(filePath):
    data=pd.read_excel(filePath)
    df=pd.DataFrame(data)
    return df

def loadAPI(URL):
    request=rq.get(URL)
    data=request.json()
    df=pd.DataFrame(data)
    return df


class DataF:
    def __init__(self,path,func):
            self.df=func(path)
     
    def get_df(self):
        return self.df
    
    def get_columns(self):
        return list(self.df.columns)
    
    def __getattr__(self, name):
        return getattr(self.df, name)

    def replaceChars(self,col,removedChar,newChar=""):
        
        self.df.iloc[:,col]=self.df.iloc[:,col].astype(str).str.replace(removedChar,newChar,regex=False)
        return (self.df)

    def renameColumn(self,ColNumber,newColName):
        colName=self.df.columns[ColNumber]
        self.df = self.df.rename(columns={colName:newColName})
        return self.df

    def filterNumerical(self,ColNumber,value ,filterType):
        colName=self.df.columns[ColNumber]
        match filterType:
            case "<":
                self.df=self.df[self.df[colName]< value]
        
            case ">":
                self.df=self.df[self.df[colName]> value]
            
            case "<=":
                self.df=self.df[self.df[colName]<= value]
        
            case ">=":
                self.df=self.df[self.df[colName]>= value]

            case "==":
                self.df=self.df[self.df[colName]== value]
        
            case "!=":
                self.df=self.df[self.df[colName]!= value]

    def filterString(self,ColNumber,value ,exactMatch=False):
        colName=self.df.columns[ColNumber]
        if (exactMatch):
            self.df=self.df[ self.df[colName]==value]
        else:
          self.df=self.df[self.df[colName].str.contains(value, case=False, na=False)]

    def filterByDate(self,ColNumber,value,filterType):
        colName=self.df.columns[ColNumber]
        try:
            date=pd.to_datetime(value, format='%Y-%m-%d', errors='raise')
            self.df[colName] = pd.to_datetime(self.df[colName], errors='coerce')
            match filterType:
                case ">":
                    self.df=self.df[self.df[colName]>date]

                case "<":
                    self.df=self.df[self.df[colName]<date]

                case ">=":
                    self.df=self.df[self.df[colName]>=date]

                case "<=":
                    self.df=self.df[self.df[colName]<=date]

                case "==":
                    self.df=self.df[self.df[colName]==date]
                

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

        