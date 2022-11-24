# engage-twitter-clone

twitter clone made with flask

## Getting started

Once you have created your new app, take a few minutes to look through the files to familiarise yourself with the project structure.

- `app.py` : entry point to the Flask app
- `templates/` : contains the frontend dynamic HTML files
- `static/` : contains the static frontend assets (images, stylesheets and scripts)
- `models.py` : contains all the database models/schemas

To start the application locally, you can just run `flask run` and this will launch the app on port 5000 (by default).
You will notice a message in the console saying:

`WARNING: Could not connect to the given database URL!`

To fix this, you should set the environment variable DATABASE_URL accordingly. If you have PostgreSQL running locally, you can use that. Alternatively, you could use SQLite which is much simpler and does not require installation, for example, by running `export DATABASE_URL="sqlite:///dev.db"`

If you do not want to use a database yet, you can ignore this warning and delete any routes that interact with the database.

If you navigate to `http://localhost:5000`, you will see the response created by the home route defined in `views.py`.

## Deploying to Heroku

To deploy your app to Heroku, you will need to create a new Heroku app and add a Postgres database to it. You can do this by running the following commands:

```bash
heroku create
heroku addons:create heroku-postgresql:hobby-dev
```

You will also need to set the environment variable `DATABASE_URL` to the value of the `DATABASE_URL` config variable that Heroku automatically sets for you. You can do this by running the following command:

```bash
heroku config:set DATABASE_URL=$(heroku config:get DATABASE_URL)
```

You can now deploy your app to Heroku by pushing to the Heroku remote:

```bash
git push heroku master
```

## Good luck with the above option because it's going away from 28NOV2022.
