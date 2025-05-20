# WeatherMap

Landing page com um mapa para o usuário checar dados e alertas para uma localização, time frame e cultura.

### Quickstart

Edite os campos nos arquivos "docker-compose.yaml", "load_csvs.py", "brazil_grid.py" e "mapa/weathermap/views.py" com as suas credenciais /USER/, /PASSWORD/, /CONTAINER NAME/ e /DB NAME/.

Faça download dos dados do bucket: ds-global-data/data/processed/ds-poseidon. Edite os 'path/to/' nos arquivos "load_csvs.py" e "grid_brazil.py"

```
$ ls
	docker-compose.yaml
	grid_brazil.py
	load_csvs.py
	mapa/
	README.md
$ docker compose up -d
```
O docker vai puxar a image do timescale e vai demorar um pouco. Minutos.

Agora transfira os .csv para o db (esse passo é demorado)
```
$ python load_csvs.py
	Loading...
	Finished...
$ grid_brazil.py
```

```
$ cd mapa
$ python manage.py runserver
```

E depois visite [essa página](http://127.0.0.1:8000/weathermap/).