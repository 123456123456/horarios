import BO as Models
class SubjectDao:
    def __init__(self,sia):
        self.sia = sia 

    def getSubjectsByName(self,name,level,maxResults):
        data = self.sia.querySubjectsByName(name,level,maxResults)
        result = []
        for i in data:
            result.append(self._createSubject(i))
        return result;

    def _createSubject(this,data):
        groups=[]
        return Models.Subject(data["nombre"],data["codigo"],data["creditos"],groups,data["tipologia"])

    def getSubjectByName(this,name,level):
        data = self.sia.querySubjectsByName(name,level,1)[0]
        return this.createSubject(data);

    def getSubjectByCode(this,code):
        raise Exception("Not implemented for SIA DAOs")


class GroupDao:
    def __init__(self,sia):
        self.sia = sia 
    
    def getGroupsBySubjectCode(self,code):
        groups = []
        groupsData = self.sia.queryGroupsBySubjectCode(code)
        for g in groupsData:
            schedule = {}
            if(g["horario_lunes"] != "--"):
                schedule[Models.DAYS[0]] = g["horario_lunes"]
            if(g["horario_martes"] != "--"):
                schedule[Models.DAYS[1]] = g["horario_martes"]
            if(g["horario_miercoles"] != "--"):
                schedule[Models.DAYS[2]] = g["horario_miercoles"]
            if(g["horario_jueves"] != "--"):
                schedule[Models.DAYS[3]] = g["horario_jueves"]
            if(g["horario_viernes"] != "--"):
                schedule[Models.DAYS[4]] = g["horario_viernes"]
            if(g["horario_sabado"] != "--"):
                schedule[Models.DAYS[5]] = g["horario_sabado"]
            if(g["horario_domingo"] != "--"):
                schedule[Models.DAYS[6]] = g["horario_domingo"]
            
            professions = []
            for i in self.sia.queryGroupsProfessions(code,g["codigo"]):
                professions.append(Models.Profession(i[0],i[1]))

            groups.append(Models.Group(g["codigo"],g["nombredocente"],self._parseSchedule(schedule),code,professions,g["cuposdisponibles"],g["cupostotal"]))
        return groups

    def _parseSchedule(self,scheduleDict):
        """
                schedule is a dictionary of {day : begin-end}*
                returns an array of ints which follows : The i-th (for i = [1,24]) less significant bit represents the time period between i-1 hours and i hours.
        """
        schedule=[]
        for i in Models.DAYS:
            try:
                scheduleString = scheduleDict[i]
                hours = ["0"]*24
                hourBlocks = scheduleString.split(" ")
                for hourBlock in hourBlocks:
                    split = hourBlock.split("-")
                    try:
                        for i in range(int(split[0]),int(split[1])):
                            #from i%24 to (i%24)+1
                            hours[23-(i%24)]="1"
                    except Exception:
                        print "Problem while parsing schedule described as :", scheduleString
                schedule.append(int("".join(hours),2))
            except KeyError:
                schedule.append(0)
        return schedule
