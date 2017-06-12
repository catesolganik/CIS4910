from flask import Flask, redirect, render_template, request, json, url_for, session, abort
from flaskext.mysql import MySQL
import pymysql.cursors
#import os
#import xlrd
from sqlalchemy.orm import sessionmaker
from hashlib import md5


app = Flask(__name__)
mysql = MySQL()



# MySQL configurations
#app.config['catherinesolgani'] = 'catie'
#app.config['Password1%'] = 'catie'
#app.config['catherinesolgani$stay_pawsitive'] = 'StayPawsitive'
#app.config['catherinesolganik.mysql.pythonanywhere-services.com'] = 'localhost'
#mysql.init_app(app)

connection = pymysql.connect(host='catherinesolganik.mysql.pythonanywhere-services.com',
                            user = 'catherinesolgani',
                            password = 'Password1%',
                            db = 'catherinesolgani$stay_pawsitive',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def homePage():
    return render_template('main_page.html')

@app.route('/animalProfileForm')
def animalProfileForm():
    return render_template('new_animal_profile.html')

@app.route('/animalProfiles')
def animlaProfiles():
    return render_template('animalProfiles.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/feedbackInput', methods=['POST'])
def feedbackInput():
    print("feedback input")
    try:
        # read the posted values from the UI
        _feedback = request.form['inputFeedback']
        #validate the received values
        #if _name and _age and _animalType and _breed and _breedmix and _weight and _description and _sex and _spayed_neutered and _shelterID:
        print(_feedback)
        try:
            cursor= connection.cursor()
            print ("writing to db")
            insert_stmt = (
                "insert into Feedback (feedback)"
                "values (%s)"
            )
            data = (_feedback)
            print ("after insert statement")
            try: cursor.execute(insert_stmt, data)
            except Exception as e:
                return json.dumps({'error &':str(e)})
            print ("wrote to db")
            connection.commit()
            print("try statement")
        except Exception as ex:
            print("except statement")
            return json.dumps({'error':str(ex)})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        print ("end")
        cursor.close()
        connection.close()
        return render_template('feedback.html')

# @app.route('/fillTable', methods=['POST'])
# def fillTable():
#     print("fill table begun")
#     # Open the workbook and define the worksheet
#     book = xlrd.open_workbook("mysite/sample_data.xlsx")
#     print("open workbook")
#     sheet = book.sheet_by_index(0)
#     #sheet = book.sheet_by_name("source")
#     print("define worksheet")

#     # Get the cursor, which is used to traverse the database, line by line
#     cursor = connection.cursor()

#     # Create the INSERT INTO sql query
#     insert_stmt = (
#             "insert into AnimalProfiles (name, age, animalType, breed, breedmix, weight, description, sex, spayed_neutered, shelterID)"
#             "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#         )
#     # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
#     for r in range(1, sheet.nrows):
#         name= sheet.cell(r,0).value
#         age = sheet.cell(r,1).value
#         animalType= sheet.cell(r,2).value
#         breed= sheet.cell(r,3).value
#         breedmix= sheet.cell(r,4).value
#         weight = sheet.cell(r,5).value
#         description= sheet.cell(r,6).value
#         sex= sheet.cell(r,7).value
#         spayed_neutered= sheet.cell(r,8).value
#         shelterID= sheet.cell(r,9).value
#         print("pull from excel sheet")
#         # Assign values from each row
#         data = (name, age, animalType, breed, breedmix, weight, description, sex, spayed_neutered, shelterID)

#         # Execute sql Query
#         cursor.execute(insert_stmt, data)
#         print("insert into database")
#     cursor.close()
#     connection.commit()
#     print("changes commited")
#     connection.close()
#     return render_template('main_page.html')

@app.route('/newProfile', methods=['POST'])
def newProfile():
    print("so far so good")
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        _age = request.form['inputAge']
        _animalType = request.form['inputAnimalType']
        _breed = request.form['inputBreed']
        _breedmix = request.form['inputBreedmix']
        _weight = request.form['inputWeight']
        _description = request.form['inputDescription']
        _sex = request.form['inputSex']
        _spayed_neutered = request.form['inputSpayed_Neutered']
        #_shelterID = request.form['inputShelterID']
        print("name is: " + _name + _age + _animalType)
        #validate the received values
        #if _name and _age and _animalType and _breed and _breedmix and _weight and _description and _sex and _spayed_neutered and _shelterID:

        try:
            cursor= connection.cursor()
            print ("writing to db")
            insert_stmt = (
                "insert into AnimalProfiles (name, age, animalType, breed, breedmix, weight, description, sex, spayed_neutered)"
                "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            data = (_name, _age, _animalType, _breed, _breedmix, _weight, _description, _sex, _spayed_neutered)
            print ("after insert statement")
            try: cursor.execute(insert_stmt, data)
            except Exception as es:
                return json.dumps({'error &':str(es)})
            print ("wrote to db")
            connection.commit()
            print("try statement")
        except Exception as ex:
            print("except statement")
            return json.dumps({'error':str(ex)})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        print ("end")
        cursor.close()
        connection.close()
        return render_template('main_page.html')

@app.route('/login_page')
def login_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        print("else render newProfile")
        return render_template('newProfile.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    print("beginning of longin method")
    if 'username' in session:
        return redirect(url_for('login'))
    try:
        cursor= connection.cursor()
        if request.method == 'POST':
            print("after connection")
            post_username = str(request.form['username'])
            post_password = str(request.form['password'])
            try:
                query = ('SELECT username from Users WHERE username = %s')
                cursor.execute(query, (post_username))
                data = cursor.fetchall()
                if not data:
                    print("not found")
                    return redirect(url_for('login'))
                else:
                    print('found')
                    session['logged_in'] = True

                print("after cursor")
            except Exception as ex:
                print("except statement")
                return json.dumps({'error':str(ex)})
        else:
            print("something is wrong")

    finally:
        cursor.close()
        connection.close()
        return render_template('main_page.html')


@app.route("/logout")
def logout():
    print("opened logout")
    #session['logged_in'] = False
    return render_template('logout.html')



if __name__ == '__main__':
    app.run()


