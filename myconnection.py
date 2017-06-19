import pymysql.cursors

#module which returns database connection
def getConnection():
    connection = pymysql.connect(host='catherinesolganik.mysql.pythonanywhere-services.com',
                            user = 'catherinesolgani',
                            password = 'Password1%',
                            db = 'catherinesolgani$stay_pawsitive',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection