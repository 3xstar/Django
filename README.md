# Insert Coin

Insert Coin is a Django site with ten original, browser-playable arcade mini-games. The games run locally in the browser; no ROM files or game downloads are required.

## Run locally

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\InsertCoin\manage.py migrate
python .\InsertCoin\manage.py runserver
```

Open `http://127.0.0.1:8000/`.

To run the tests:

```powershell
python .\InsertCoin\manage.py test main
```

For deployment, set the `DJANGO_SECRET_KEY` environment variable to a private, randomly generated value and configure `DEBUG` and `ALLOWED_HOSTS` for the deployment environment.
