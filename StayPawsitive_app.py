from flask import Flask, redirect, render_template, request, json, url_for
from flaskext.mysql import MySQL
import pymysql.cursors



app = Flask(__name__)
mysql = MySQL()



# MySQL configurations
#app.config['catherinesolgani'] = 'catie'
#app.config['Password1%'] = 'catie'
#app.config['catherinesolgani$stay_pawsitive'] = 'StayPawsitive'
#app.config['catherinesolganik.mysql.pythonanywhere-services.com'] = 'localhost'
#mysql.init_app(app)

#connection = pymysql.connect(host='catherinesolganik.mysql.pythonanywhere-services.com', user = 'catherinesolgani', password = 'Password1%', db = 'catherinesolgani$stay_pawsitive', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

@app.route('/homePage')
def homePage():
    return render_template('main_page.html')

@app.route('/animalProfileForm')
def animalProfileForm():
    return render_template('new_animal_profile.html')


@app.route('/newProfile', methods=['POST'])
def newProfile():
    print("so far so good")
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        print("name is: " + _name)
        #_age = request.form['inputAge']
        #_animalType = request.form['inputAnimalType']
        #_breed = request.form['inputBreed']
        #_breedmix = request.form['inputBreedmix']
        #_weight = request.form['inputWeight']
        #_description = request.form['inputDescription']
        #_sex = request.form['inputSex']
        #_spayed_neutered = request.form['inputSpayed_Neutered']
        #_shelterID = request.form['inputShelterID']

        #validate the received values
        if _name and _age and _animalType and _breed and _breedmix and _weight and _description and _sex and _spayed_neutered and _shelterID:

           with mysql.get_db().cursor() as cursor:
                cursor.execute("insert into AnimalProfiles (name, age, animalType, breed, breedmix, weight, description, sex, spayed_neutered, shelter_ID) values (%s, %s, %s, %s, %s, %d, %s, %s, %s, %d)", (_name, _age, _animalType, _breed, _breedmix, _weight, _description, _sex, _spayed_neutered, _shelterID))
           mysql.get_db().commit()

        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        #connection.close()


if __name__ == '__homePage__':
    app.run()


