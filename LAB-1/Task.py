import json

class Data:
    def __init__(self):
        self.data = {}

    def __hash__(self, name, greeting, org):
        
        return hash((name, greeting, org))

    def addData(self, greeting, name, org):
        next = hash((greeting, name, org)) + 1
        if(not self.data):
            self.data.update({hash((greeting, name, org)): [greeting, name, org, next]})
        else:
            no_of_keys = len(self.data.keys())

            for itr in range(no_of_keys):
                if itr == no_of_keys -1:
                    
                
                


    def getJson(self):
        return json.dumps(self.data)

Data1 = Data()

Data1.addData('Hello1', 'Bilal', 'NuFast')
Data1.addData('Hello2', 'Ahmed', 'NuFast')

print(Data1.getJson())
