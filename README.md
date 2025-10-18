# Snake Reinforcement Learning
## Opis projektu
Ten projekt to implementacja gry Snake z wykorzystaniem uczenia ze wzmocnieniem (Reinforcement Learning). Celem projektu jest nauczenie Snaka poruszania się po planszy i zbirania owoców. 
## Instalacja i uruchomienie
1. Sklonuj repozytorium: `git clone`
```bash
git@github.com:Nicram123/snake_Reinforcement_Learning.git
```                                                                      
3. Zainstaluj wymagane biblioteki:
```bash
pip install pygame
```
```bash
pip install tensorflow, numpy
```
5. Uruchom trening:
```bash
python -m Snake.train
```
lub skorzystaj z gotowych modeli w folderze `models`

7. Uruchom program z poziomu `main.py`: 
```bash
python main.py
```
## Trening
Trening Snaka odbywa się:
* w train.py po przez naukę w epizodach
* jeden epizod trwa aż do momentu zderzenia ze ścianą lub z własnym ogonem (koniec gry), stopniowo ucząc się ruchów nie powodujących kolizji i zmierzających w stronę punktu (zielona kropka) 
## Wyniki po treningu 
![snake](https://github.com/user-attachments/assets/b89d4f36-77e7-46dd-a208-453af1289548)
## Uwagi
* Na razie najlepszy z modeli `snake_ai_ep100.keras` z folderu `models` działa najlpiej ale jest on w stanie maxymalnie zebrać do 50 punktów za pierwszym razem  

