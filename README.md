## Rozproszony system pomiarowy

Repozytorium stworzone w ramach realizacji przedmiotu AASD Aktorowe i Agentowe systemy decyzyjne.

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
   -v ./ejabberd.yml:/home/ejabberd/conf/ejabberd.yml \
   ejabberd/ecs
```

Poszczególne agenty znajdują się w folderze `app`  
Uruchomienie przykładowej apki

```bash
cd app
pip3 install -r ./requirements.txt
XMPP_SERVER=localhost XMPP_PASSWORD="PASSWORD" ./app.py
```
