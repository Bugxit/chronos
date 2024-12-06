from svgnsi import *
from colorama import Fore

class Event:
    """
        Évènement défini par un titre, un jour, un moi et une année.
    """
    def __init__(self, title, day, month, year):
        self.title = title
        self.day = day
        self.month = month
        self.year = year
        # Calcul grossier du nombre de jours depuis JC
        # Permet de trier chronologiquement les évènements
        self.timecode = year*366 + month*31 + day

    def display(self):
        """
            Renvoie la date et le titre d'un évènement dans une chaîne de caractère.

            Exemple : "24 Novembre 2019 : La Fille de Vercingétorix"
        """
        fmt = ""

        if 1 <= self.day <= 31:
            fmt += str(self.day) + " "
        
        if 1 <= self.month <= 12:
            fmt += ["Jan", "Fev", "Mar", "Avr", "Mai", "Jui", "Jui", "Aou", "Sep", "Oct", "Nov", "Dec"][self.month - 1] + " "

        if type(self.year) == int:
            fmt += str(self.year)

        fmt += " : " + self.title

        return fmt

class Period:
    """
        Période définie par un titre et deux évènements (un pour le début et un pour la fin)
        Le titre des évènement n'a pas d'importance.
    """

    def __init__(self, title: str, startEvent: Event, lastEvent: Event):
        self.title = title
        self.startEvent = startEvent
        self.lastEvent = lastEvent

        self.timecode = startEvent.timecode
        self.endTimecode = lastEvent.timecode

    def display(self):
        pass


class Timeline:
    """
        Frise chronologique pouvant contenir des évènements et des périodes.
        Seulement les énvènements sont traités actuellement.
    """

    def __init__(self, name):
        self.listEvent = []
        self.listPeriod = []
        self.name = name

    def addEvent(self, event):
        eTime = event.timecode

        for ev in self.listEvent:
            if eTime != ev.timecode:
                continue

            ev.title += " ; " + event.title
            return

        self.listEvent.append(event)
        self.listEvent.sort(key=lambda e : e.timecode)

    def addPeriod(self, period):
        self.listPeriod.append(period)

    def display(self):
        """
            Affiche la liste des évènements et des périodes dans le shell
        """

        for event in self.listEvent:
            periodStartingWithEvent = [p for p in self.listPeriod if p.timecode == event.timecode]
            periodEndingWithEvent = [p for p in self.listPeriod if p.endTimecode == event.timecode]

            for p in periodStartingWithEvent:
                print(f"# {Fore.CYAN}{p.title}{Fore.RESET} - {p.startEvent.display().split(':')[0]}")

            print(event.display())
            
            for p in periodEndingWithEvent:
                print(f"# {Fore.RED}{p.title}{Fore.RESET} - {p.lastEvent.display().split(':')[0]}")


    def minMaxEvent(self):
        """
            Renvoie les timecodes du premier et du dernier évènement.
        """
        return self.listEvent[0].timecode, self.listEvent[-1].timecode


    def toSVG(self):
        """
            Dessine la frise en utilisant la bibliothèque svgnsi.
        """

        getTimecode = lambda e : e.timecode

        eventsToDisplay = self.listEvent
        eventsTimeCodes = list(map( getTimecode, eventsToDisplay ))

        minGapBetweenTwoDates = min([eventsTimeCodes[i + 1] - eventsTimeCodes[i] for i in range(len(eventsTimeCodes) - 1)])
        maxGapBetweenTwoDates = max(eventsTimeCodes) - min(eventsTimeCodes)
        
        width = ( 25 * maxGapBetweenTwoDates ) // minGapBetweenTwoDates + 200
        height = 500 

        img = Draw(width, height)
        img.generate()
        img.line(0, 300, width, 300, "black", 2)

        timecodeToXOffset = lambda t : ( 25 * (t - min(eventsTimeCodes)) ) // minGapBetweenTwoDates + 10
        for timecode, event in zip(eventsTimeCodes, eventsToDisplay):
            xOffset = timecodeToXOffset(timecode)
            img.line(xOffset, 305, xOffset, 295, "black", "2")
            img.text(xOffset, 290, event.display(), "black", 1, "black", "10", rotate = 45)



        periodsToDisplay = self.listPeriod
        periodsStart = list(map( lambda p : p.startEvent, periodsToDisplay ))
        periodsEnd   = list(map( lambda p : p.lastEvent, periodsToDisplay ))
        periodsTimeStart = list(map( getTimecode, periodsStart ))
        periodsTimeEnd = list(map( getTimecode, periodsEnd ))

        periodDeepness = [0 for i in range(width)]

        p_num = 0
        for timecodeStart, timecodeEnd, p in zip(periodsTimeStart, periodsTimeEnd, periodsToDisplay):
            xStart = timecodeToXOffset(timecodeStart)
            xEnd = timecodeToXOffset(timecodeEnd)
             
            curDeepness = max(periodDeepness[xStart:xEnd]) + 1
            
            color = ["cyan", "lime", "yellow", "magenta", "pink"][p_num % 5]
            p_num += 1

            img.line(xStart, 315 + 30 * curDeepness, xEnd, 315 + 30 * curDeepness, color, "3")
            img.text((xStart + xEnd) // 2, 330 + 30 * curDeepness, p.title, "black", 1, "black", "15", textanchor="middle")

            for x in range(xStart, xEnd):
                periodDeepness[x] = curDeepness

        img.save("output.svg")

# Création de frise avec quelques BD d'Astérix
timeline = Timeline("asterix")

timeline.addEvent(Event("Astérix le Gaulois", 0, 0, 1961))
timeline.addEvent(Event("La serpe d'or", 0, 0, 1962))
timeline.addEvent(Event("Astérix chez les Pictes", 0, 0, 2013))
timeline.addEvent(Event("La Fille de Vercingétorix",24,10,2019))
timeline.addEvent(Event("Astérix en Corse",0,0,1973))
timeline.addEvent(Event("Le grand fossé",0,0,1980))
timeline.addEvent(Event("Astérix chez les Bretons",0,0,1966))
timeline.addEvent(Event("La galère d'Obélix",0,0,1996))
timeline.addEvent(Event("Le ciel lui tombe sur la tête",0,0,2005))
timeline.addEvent(Event("Astérix chez Rahàzade",0,0,1987))
timeline.addEvent(Event("Astérix gladiateur",0,0,1964))
timeline.addEvent(Event("Le combat des chefs",0,0,1966))

timeline.addPeriod(Period("Goscinny", Event("Astérix le Gaulois", 0, 0, 1961), Event("Astérix en Corse",0,0,1973)))
timeline.addPeriod(Period("Uderzo", Event("Le grand fossé",0,0,1980), Event("Le ciel lui tombe sur la tête",0,0,2005)))
timeline.addPeriod(Period("Ferri", Event("Astérix chez les Pictes", 0, 0, 2013), Event("La Fille de Vercingétorix",24,10,2019)))

timeline.addPeriod(Period("Période de test =}", Event("Astérix chez les Bretons",0,0,1966), Event("Astérix chez Rahàzade",0,0,1987)))
timeline.addPeriod(Period("Période de ...", Event("Astérix en Corse",0,0,1973), Event("Astérix chez les Pictes", 0, 0, 2013)))

timeline.display()
timeline.toSVG()
