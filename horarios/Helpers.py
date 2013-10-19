import json
import urllib2
from Models import Subject,Group,Schedule
import Models

class SIA:

    def existsSubject(this,name,level):
        return this.queryNumSubjectsWithName(name,level)>0

    def queryNumSubjectsWithName(this,name,level):
        data = json.dumps({"method": "buscador.obtenerAsignaturas", "params": [name, level, "", level, "", "", 1, 1]})
        req = urllib2.Request("http://www.sia.unal.edu.co/buscador/JSON-RPC", data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        result = json.loads(f.read())["result"]["totalAsignaturas"]
        f.close()
        return result

    def querySubjectsByName(this,name,level,maxRetrieve):
        data = json.dumps({"method": "buscador.obtenerAsignaturas", "params": [name, level, "", level, "", "", 1, maxRetrieve]})
        req = urllib2.Request("http://www.sia.unal.edu.co/buscador/JSON-RPC", data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        result=json.loads(f.read())
        f.close()
        return result["result"]["asignaturas"]["list"]

    def queryGroupsBySubjectCode(this,code):
        data = json.dumps({"method": "buscador.obtenerGruposAsignaturas", "params": [code, "0"]})
        req = urllib2.Request("http://www.sia.unal.edu.co/buscador/JSON-RPC", data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        result=json.loads(f.read())
        f.close()
        return result["result"]["list"]

    def getSubject(this,name,level):
        data = this.querySubjectsByName(name,level,1)[0]
        groupsData = this.queryGroupsBySubjectCode(data["codigo"])
        groups=[]
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

            groups.append(Group(g["codigo"],g["nombredocente"],schedule))

        return Subject(data["nombre"],data["codigo"],data["creditos"],groups)


class Generator:

    def generateSchedule(self,listOfListOfCourses):
        result = []
        if(len(listOfListOfCourses) == 1):
            for c in listOfListOfCourses[0]:
                result.append(Schedule(None,c))
            return result

        courses = listOfListOfCourses.pop()
        subSchedules = self.generateSchedule(listOfListOfCourses)
        for course in courses:
            for schedule in subSchedules:
                if(schedule._isCompatible(course)):
                    result.append(schedule.clone().addGroup(course))

        if(len(result) == 0):
            print "No schedule can be generated so that it includes " , courses
        return result
                
sia = SIA()
print "Fetching info"
a = sia.getSubject("Algoritmos","PRE")
b = sia.getSubject("Seguridad en redes","PRE")
c = sia.getSubject("Lenguajes de programacion","PRE")
print "Generating schedules"
gen = Generator()
s = gen.generateSchedule([a.groups,b.groups])
for i in s:
    print i
