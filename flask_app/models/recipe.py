from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
DATE_REGEX = re.compile(r"^[12]{1,1}[09]{1,1}[0-9]{2,2}-[01]{1,1}[0-9]{1,1}-[0123]{1,1}[0-9]{1,1}$")

class Recipe():
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.under_30 = data['under_30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod# Submit a recipe to the database
    def submit(cls, data):
        query = "INSERT INTO recipes (user_id, name, under_30, description, instructions, date_made) VALUES (%(user_id)s, %(name)s, %(under_30)s, %(description)s, %(instructions)s, %(date_made)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_recipe( recipe ):
        is_valid = True
        # requires a language selection
        if len(recipe['name']) < 5:
            flash(u'Name must contain at least 5 characters')
            is_valid = False
        # requires a language selection
        if len(recipe['description']) < 5:
            flash(u'Description must contain at least 5 characters')
            is_valid = False
        # requires a language selection
        if len(recipe['instructions']) < 5:
            flash(u'Instructions must contain at least 5 characters')
            is_valid = False
        # test whether date matches the pattern/may be unnecessary with date picker
        if not DATE_REGEX.match(recipe['date_made']):
            flash(u'Recipe Made Date cannot be left blank and must follow the format: XX-XX-XXXX')
            is_valid = False
        return is_valid

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update_recipe(cls, data): 
        query = "UPDATE recipes SET user_id = %(user_id)s, name = %(name)s, under_30 = %(under_30)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def fetch_recipes(cls):# retrieves all recipes
        query = "SELECT * FROM recipes JOIN users on users.id = recipes.user_id;"
        return connectToMySQL(DATABASE).query_db(query)

    @classmethod
    def grab_recipe(cls, data):# retrieves specific recipe
        query = "SELECT * FROM recipes JOIN users on users.id = recipes.user_id where recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results[0]