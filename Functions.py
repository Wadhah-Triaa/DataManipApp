import pandas as pd
import requests as rq
from googletrans import Translator
import asyncio
from tkinter import messagebox

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

def saveCSV(filePath,df):
    df.to_csv(filePath, index=False)

def saveTxt(filePath,df):
    df.to_csv(filePath, index=False)

def saveExcel(filePath,df):
    df.to_excel(filePath, index=False)

class DataF:
    def __init__(self,path,func):
            self.df=func(path)
            self.df=self.df.convert_dtypes()
            self.originalData=self.df.copy()
     
    def get_df(self):
        return self.df
    
    def get_columns(self):
        return list(self.df.columns)
    
    def __getattr__(self, name):
        return getattr(self.df, name)

    def replaceChars(self,col,removedChar,newChar=""):
        
        self.df.iloc[:,col]=self.df.iloc[:,col].astype(str).str.replace(removedChar,newChar,case=False ,regex=False)
        return (self.df)

    def renameColumn(self,colNumber,newColName):
        colName=self.df.columns[colNumber]
        self.df = self.df.rename(columns={colName:newColName})
        return self.df

    def filterNumerical(self,colNumber,value ,filterType):
        colName=self.df.columns[colNumber]
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

    def filterString(self,colNumber,value ,exactMatch=False):
        colName=self.df.columns[colNumber]
        if (exactMatch):
            self.df=self.df[ self.df[colName]==value]
        else:
          self.df=self.df[self.df[colName].str.contains(value, case=False, na=False)]

    def filterByDate(self,colNumber,value,filterType):
        colName=self.df.columns[colNumber]
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
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.\n}")


    def dropColumn(self,colNumber):
        self.df=self.df.drop(self.df.columns[colNumber], axis=1)   
    
    async def translate(self, txt, semaphore,language,retries=3):
        async with semaphore:
            tr = Translator()
            for attempt in range(retries):
                try:
                    result = await tr.translate(txt, dest=language)
                    return result.text, result.src   # return only the translation
                except Exception as e:
                    print(f"Error on attempt {attempt+1} for '{txt}': {e}")
                    await asyncio.sleep(2)  # wait before retry
            return ""

    async def translateAll(self,colNumber,language):
        semaphore = asyncio.Semaphore(10)  # Limit concurrent translations
        tasks = [self.translate(txt, semaphore,language) for txt in self.df[self.df.columns[colNumber]]]
        results = await asyncio.gather(*tasks)  
        translations = [res[0] for res in results]
        sourceLanguages = [res[1] for res in results]

        newColName=self.df.columns[colNumber]+" translated"
        self.df[newColName] = translations
        newColLanguage=self.df.columns[colNumber]+" source"
        self.df[newColLanguage] = sourceLanguages

    def sortByOrder(self,colNumber,order):
        if (order=="Ascending"):
            self.df.sort_values(by=self.df.columns[colNumber], ascending=True, na_position='first', inplace=True)
        elif ( order=="Descending"):
            self.df.sort_values(by=self.df.columns[colNumber], ascending=False, na_position='first', inplace=True)
      

    def showRows(self,border,number):
        if (border=="Top Rows"):
            self.df=self.df.head(number)
        elif (border=="Bottom Rows"):
            self.df=self.df.tail(number)

    def removeDuplicateByColumn(self,colNumber):
        self.df.drop_duplicates(subset=self.df.columns[colNumber], keep='last',inplace=True)

    def removeAllDuplicates(self):
        self.df.drop_duplicates(inplace=True)

    def getOriginalData(self):
        
        self.df=self.originalData.copy()

    def mergeColumns(self,colNumber1,ColNumber2,newColName):
        self.df[newColName]=self.df.columns[colNumber1]+self.df.columns[ColNumber2]

    def splitColumn(self,colNumber,newColName1,newColName2,separator):
        dttype=self.df[self.df.columns[colNumber]].dtype
        newColumns=self.df[self.df.columns[colNumber]].astype(str).str.split(pat=separator,expand=True)
        newColumns = newColumns.iloc[:, :2] 
        newColumns.columns = [newColName1, newColName2]
        if dttype== "Float64":
            dttype="Int64"
        newColumns=newColumns.astype(dttype)
        newColumns=newColumns.convert_dtypes()
        self.df = pd.concat([self.df, newColumns], axis=1)


