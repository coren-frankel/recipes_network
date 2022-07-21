from flask import Flask, session
DATABASE = "recipes_schema"
app = Flask(__name__)
app.secret_key = "4wallsandaroofkeepthesecretsin"