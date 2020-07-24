def Person():
    def __init__(self, age, vaccine_rate, affected_rate):
        self.age = age
        self.vaccine_rate = vaccine_rate
        self.affected_rate = affected_rate

def HealthPerson():
    def __init__(self, age, vaccine_rate, affected_rate):
        Person(age, vaccine_rate, affected_rate)

def IdxCasePerson():
    def __init__(self, age, vaccine_rate, affected_rate, hosp_status, sever_rate, mortality_rate, symptom):
        Person(age, vaccine_rate, affected_rate)
        self.hosp_status = hosp_status
        self.sever_rate = sever_rate
        self.mortality_rate = mortality_rate
        self.symptom = symptom
