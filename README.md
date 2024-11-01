# SAI-INM5151


## Scrapper Annonces Immobileres

## Description
Ce logiciel sert a trouver les informations de proprietes en vente sur Duproprio, Centris ou Realtor et de sortir les donnees de ceux-ci sous un format CSV, JSON, XML ou PDF.

## Installation

Pour installer le logiciel:
1. `git clone https://gitlab.info.uqam.ca/delisle.nicolas/sai-inm5151.git`
2. `.\venv\Scripts\activate`
2. `pip install -r requirements.txt`
3. `python scraper.py <[numero d'adresse] [nom de rue], [ville], [province], [pays]>`

## Developeurs
Utiliser le format suivant pour les branches:
`git checkout -b sprint-1-nom-du-feature`

## Usage
Le programme prend en entre une adresse au format suivant:

```[numero d'adresse] [nom de rue], [ville], [province], [pays]```

exemple:

```750 Rue des Sureaux, Boucherville, QC, Canada```

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
1. Sprint 1:

 [x] Module de scrapping

2. Sprint 2:

 - GUI (web ui)
 - Conversion vers XML, CSV, JSON et PDF

3. Sprint 3:

 - Persistance des donnees (BD)
 - Hosting et admin


## Authors and acknowledgment
Logiciel cree dans le cadre du cours INM5151 par:
Nicolas Delisle
Christian Barikhan
Ibrahima Mathias Davieau

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
