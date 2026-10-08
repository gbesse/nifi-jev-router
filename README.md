# NiFi Jev Router

## Français

`NiFi Jev Router` ajoute un embranchement sémantique borné à un flux NiFi. Un FlowFile JSON contenant `id` et `text` reçoit une décision `incident`, `routine` ou `review`, une probabilité et une version de politique. Le texte original n'est pas enregistré par ce service ; SQLite ne conserve qu'une empreinte, l'identifiant et la décision. Les répétitions du même identifiant sont dédupliquées. Un texte différent sous le même identifiant est refusé.

Installez les dépendances avec `python3 -m pip install -r requirements.txt`. Définissez `TYPESAFE_API_KEY` et un `JEV_INGEST_TOKEN` aléatoire d'au moins 16 caractères dans un environnement privé, puis lancez `python3 app.py --serve`. Le service écoute sur `127.0.0.1:8096` par défaut. Dans NiFi, envoyez le JSON par `InvokeHTTP` en `POST` vers `/decide` avec `Authorization: Bearer <jeton>`. Reliez sa sortie `Response` à `EvaluateJsonPath` pour extraire `$.outcome`, puis à `RouteOnAttribute`. La réponse contient la décision, pas le contenu d'origine : utilisez `id` pour la corrélation si le flux doit conserver le FlowFile initial. Les réponses `503` doivent suivre la voie de nouvelle tentative NiFi.

Exemple sans clé : `python3 app.py --demo`. Tests : `python3 -m unittest discover -s tests -v`. Lisez les décisions via `GET /decisions` avec le même jeton. Le protocole HTTP est testé localement ; aucun serveur NiFi n'a été connecté dans cette version. [Documentation `InvokeHTTP`](https://nifi.apache.org/components/org.apache.nifi.processors.standard.InvokeHTTP/).

## English

`NiFi Jev Router` adds a bounded semantic branch to a NiFi flow. A JSON FlowFile with `id` and `text` receives `incident`, `routine`, or `review`, plus probability and policy version. The service does not persist the original text; SQLite stores only a digest, ID, and decision. Repeated IDs are deduplicated, while a changed text under the same ID is rejected.

Install dependencies with `python3 -m pip install -r requirements.txt`. Set `TYPESAFE_API_KEY` and a random `JEV_INGEST_TOKEN` of at least 16 characters privately, then run `python3 app.py --serve`. The service binds to `127.0.0.1:8096` by default. In NiFi, POST the JSON with `InvokeHTTP` to `/decide` using `Authorization: Bearer <token>`. Connect its `Response` relationship to `EvaluateJsonPath` for `$.outcome`, then `RouteOnAttribute`. The response contains the decision, not the original content: correlate by `id` if the flow must retain the original FlowFile. Send `503` responses to NiFi's retry path.

Offline example: `python3 app.py --demo`. Tests: `python3 -m unittest discover -s tests -v`. Read decisions through authenticated `GET /decisions`. HTTP behavior was tested locally; no NiFi server was connected for this release. [`InvokeHTTP` documentation](https://nifi.apache.org/components/org.apache.nifi.processors.standard.InvokeHTTP/).

## Español

`NiFi Jev Router` añade una bifurcación semántica acotada a un flujo NiFi. Un FlowFile JSON con `id` y `text` recibe `incident`, `routine` o `review`, además de probabilidad y versión de política. El servicio no conserva el texto original; SQLite solo guarda una huella, el ID y la decisión. Los ID repetidos se deduplican y un texto distinto con el mismo ID se rechaza.

Instale las dependencias con `python3 -m pip install -r requirements.txt`. Defina `TYPESAFE_API_KEY` y un `JEV_INGEST_TOKEN` aleatorio de al menos 16 caracteres de forma privada y ejecute `python3 app.py --serve`. Por defecto, escucha en `127.0.0.1:8096`. En NiFi, envíe el JSON mediante `InvokeHTTP` por `POST` a `/decide` con `Authorization: Bearer <token>`. Conecte la salida `Response` a `EvaluateJsonPath` para extraer `$.outcome` y luego a `RouteOnAttribute`. La respuesta contiene la decisión, no el contenido original: correlacione por `id` si necesita conservar el FlowFile inicial. Envíe las respuestas `503` a la ruta de reintento de NiFi.

Ejemplo sin clave: `python3 app.py --demo`. Pruebas: `python3 -m unittest discover -s tests -v`. Consulte las decisiones por `GET /decisions` autenticado. El comportamiento HTTP se probó localmente; esta versión no se conectó a un servidor NiFi. [Documentación de `InvokeHTTP`](https://nifi.apache.org/components/org.apache.nifi.processors.standard.InvokeHTTP/).

MIT. Tag: `v0.1.0`.
