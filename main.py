from svgnsi import *

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
            fmt += ["J", "F", "M", "A", "Mai", "Juin", "Juillet", "Aout", "Sept", "Oct", "Nov", "Dec"][self.month - 1] + " "

        if type(self.year) == int:
            fmt += str(self.year)

        fmt += " : " + self.title

        return fmt

class Period:
    def __init__(self): pass

    """
        Période définie par un titre et deux évènements (un pour le début et un pour la fin)
        Le titre des évènement n'a pas d'importance.
    """
    pass

class Timeline:
    """
        Frise chronologique pouvant contenir des évènements et des périodes.
        Seulement les énvènements sont traités actuellement.
    """

    def __init__(self, name):
        self.listEvent = []
        self.name = name

    def addEvent(self, event):
        self.listEvent.append(event)
        ## On remet la lsite dans l'ordre chronologique
        self.listEvent.sort(key=lambda event: event.timecode)

    def display(self):
        """
            Affiche la liste des évènements et des périodes dans le shell
        """

        for event in listEvent:
            print( event.display() )


    def minMaxEvent(self):
        """
            Renvoie les timecodes du premier et du dernier évènement.
        """
        return self.listEvent[0].timecode, self.listEvent[-1].timecode


    def toSVG(self):
        """
            Dessine la frise en utilisant la bibliothèque svgnsi.
        """
        
        w = len(self.listEvent) * 40
        h = 150

        img = Draw(w, h)
        img.generate()
        img.line(0, 135, w, 135, "black", 2)

        x = 10

        for event in self.listEvent:
            img.text(x, 130, event.display(), "black", 1, "red", "10", rotate = 45)

            x += 20
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

timeline.toSVG()
