import pandas as pd


#================================================================
class DataQuery:
    """Generic data extractor for csv file. any header name 
    can be added to query, will return empty if name doesnt match."""


    #headers legend for MS specific table
    #DOB	Gender	OnsetDate	DiagnosisDate	MSAtDiagnosis	MSTypeNow	QuestionnaireKey	
    #QuestionnaireId	CompletedDate	Value	GroupId	QueryDate
    def __init__(self, path, filterVals):
        self.path = path;
        self.filterValues = filterVals
    
    def execute(self):
        '''
        Return:
            -pandas DataFrame
        '''
        dat_raw = pd.read_csv(self.path)
        dat = dat_raw.filter(self.filterValues)
        return dat
    
#================================================================
class DataQueryBuilder:

    """
    syntax: query(path).withAttr1().withAttr2().build().execute()
    will return a pd.DataFrame. Without execute() will return 
    a DataQuery object.
    """
    
    def __init__(self):
        self.filterValues = list()
        self.path = None
        
    @staticmethod
    def query(path):
        qb = DataQueryBuilder()
        qb.path = path
        return qb
        
    def build(self):
        return DataQuery(self.path, self.filterValues)
        
    
    def withUserId(self):
        self.filterValues.append("UserId")
        return self
    
    def withBirthDate(self):
        self.filterValues.append("DOB")
        return self    
    
    def withOnsetDate(self):
        self.filterValues.append("OnsetDate")
        return self
    
    def withValue(self):
        self.filterValues.append("Value")
        return self
    
    def withDiagnosisDate(self):
        self.filterValues.append("DiagnosisDate")
        return self
    
    def withQuestionnaireId(self):
        self.filterValues.append("QuestionnaireId")
        return self
    
    def withCompletedDate(self):
        self.filterValues.append("CompletedDate")
        return self
    
    def withGroupdD(self):
        self.filterValues.append("GroupId")
        return self
    
    def withGender(self):
        self.filterValues.append("Gender")
        return self
    
    def withMSAtDiagnosis(self):
        self.filterValues.append("MSAtDiagnosis")
        return self
    
    def withMSTypeNow(self):
        self.filterValues.append("MSTypeNow")
        return self
    
    def withQuestionnaireKey(self):
        self.filterValues.append("QuestionnaireKey")
        return self
    
    def withWebEDSS(self):
        self.filterValues.append("webEDSS")
        return self
    
    def withCompletedDate_webEDSS(self):
        self.filterValues.append("CompletedDate_webEDSS")
        return self