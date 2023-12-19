## Rozproszony system pomiarowy

Repozytorium stworzone w ramach realizacji przedmiotu AASD Aktorowe i Agentowe systemy decyzyjne.

### Proces developerski

W celu zachowania zasad clean code, przed wrzuceniem commita na brancha, zaleca się wykonaie pre-commita. Wszystkie potrzebne w tym celu biblioteki są zawarte w `dev_requirements.txt`.

```bash
pip install -r app/dev_requirements.txt
```

Aby uruchomić pre-commit, należy użyć komendy:

```bash
pre-commit run --all-files
```

W skład pre-commita wchodzą: black, isort, ruff i mypy.


### Uruchamianie

Cały system można uruchomić za pomocą jedengo pliku docker-compose

```bash
docker-compose up
```

Możliwe też jest uruchomienie poszczególnych elementów niezależnie od siebie np na potrzeby developmentu, czy testów.

Uruchomienie serwera XMPP:

```bash
docker run --rm \
   -p 5222:5222 \
   -p 5280:5280 \
   -v /"$(pwd)"/ejabberd.yml:/home/ejabberd/conf/ejabberd.yml \
   ejabberd/ecs
```

Poszczególne agenty znajdują się w folderze `app`  
Uruchomienie przykładowej apki

```bash
cd app
pip3 install -r ./requirements.txt
XMPP_SERVER=localhost XMPP_PASSWORD="PASSWORD" ./app.py
```
