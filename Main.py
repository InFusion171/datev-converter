from Gui import Gui


'''
Aufbau der input datei:

"Kontoumsätze 
* 
"Währung"

"BUCHUNGSTAG";"WERTSTELLUNGSTAG";"VERWENDUNGSZWECK";"UMSATZ";"WÄHRUNG"
"BUCHUNGSTAG";"WERTSTELLUNGSTAG";"VERWENDUNGSZWECK";"UMSATZ";"WÄHRUNG"
"BUCHUNGSTAG";"WERTSTELLUNGSTAG";"VERWENDUNGSZWECK";"UMSATZ";"WÄHRUNG"
...

"* noch nicht ausgeführte Umsätze"

'''

def main():
    gui = Gui('DATEV Format erstellen')
    gui.run()


if __name__ == '__main__':
    main()
