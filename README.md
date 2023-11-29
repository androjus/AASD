## Rozproszony system pomiarowy

Repozytorium stworzone w ramach realizacji przedmiotu AASD Aktorowe i Agentowe systemy decyzyjne.

### Uruchamianie

Cały system można uruchomić za pomocą jedengo pliku docker-compose

```bash
docker-compose up
```

Możliwe też jest uruchomienie wszystkiego lokalnie, wtedy jedynie serwer XMPP musibyć uruchomiony za pomocą dockera:

```bash
docker run -d \
   -p 5222:5222 \
   -p 5269:5269 \
   -p localhost:5347:5347 \
   -e PASSWORD=testowehaslo \
   prosody/prosody:latest
```

Poszczególne agenty znajdują się w folderze `app`

```
cd app
pip3 install -r ./requirements.txt
XMPP_PASSWORD="testowehaslo" ./app.py
```