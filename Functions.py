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
    def __init__(self,df,path,func):
        df=func(path)
        self.df=df

    def replaceChars(self,col,removedChar,newChar=""):
        self.df[col]=self.df[col].str.replace(removedChar,newChar)
        print(self.df)

    def renameColumn(self,colName,newColName):
        self.df = self.df.rename(columns={colName:newColName})
        print(self.df)

    def filterNumerical(self,colName,value ,filterType):
        match filterType:
            case "<":
                print(self.df[self.df[colName]< value])
        
            case ">":
                print(self.df[self.df[colName]> value])
            
            case "<=":
                print(self.df[self.df[colName]<= value])
        
            case ">=":
                print(self.df[self.df[colName]>= value])

            case "==":
                print(self.df[self.df[colName]== value])
        
            case "!=":
                print(self.df[self.df[colName]!= value])   

    def filterString(self,colName,value ,exactMatch=True):
        if (exactMatch):
            print( self.df[ self.df[colName]==value])
        else:
          print( self.df[self.df[colName].str.contains(value, case=False, na=False)])

    def filterByDate(self,colName,value,filterType):
        try:
            date=pd.to_datetime(value, format='%Y-%m-%d', errors='raise')
            self.df[colName] = pd.to_datetime(self.df[colName], errors='coerce')
            match filterType:
                case ">":
                    print (self.df[self.df[colName]>date])

                case "<":
                    print (self.df[self.df[colName]<date])

                case ">=":
                    print (self.df[self.df[colName]>=date])

                case "<=":
                    print (self.df[self.df[colName]<=date])

                case "==":
                    print (self.df[self.df[colName]==date])

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

        