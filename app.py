from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, re, time

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def home():
    return render_template("Index.html")

@app.route('/login')
def login():
    return render_template("Login.html")

@app.route('/apanel',methods = ['POST'])
def ahome():
    uname=request.form['uname']  
    passwrd=request.form['psw']  
    if uname=="admin" and passwrd=="1234":
        return render_template("APanel.html")
    else:
        flash('Wrong Username or Password')
        return render_template("Login.html")

@app.route('/apanel/t')
def ahome2():
    return render_template("APanel.html")

@app.route('/vpanel')
def vhome():
    return render_template("VPanel.html")

# ---------------------------------------------------------------------------------------------------
# 
#                                       Dictionaries
# 
# ----------------------------------------------------------------------------------------------------

bio = {
    "cnic": 0,
    "age": 0,
    "contact_no": 0,
    "disabled": 0,
    "guardian": 'A',
    "family_members": 0,
    "name": 0,
    "gender": 0,
    "district": 0,
    "martial_status": 0,
    "hhi": 0
}

job = {
    "cnic": 0,
    "job_category": 0,
    "employment_status": 0,
    "profession": 0,
    "experience": 0,
    "salary": 0,
    "prev_salary": 0,
    "comment": 'None'
}

org = {
    "reg_no": 0,
    "type": 0,
    "org_name": 'None'
}

relief_reg = {
    "rr_no": 0,
    "reg_no": 0,
    "relief_awarded": 0,
    "total_people": 0,
    "date": 0
}

district_stats = {
    "district": 0,
    "employment_no": 0,
    "unemployment_no": 0,
    "hhi_average": 0,
    "teen_age_no": 0,
    "middle_age_no": 0,
    "old_age_no": 0,
    "disable_percentage": 0,
    "family_members_average": 0,
    "women_no": 0,
    "men_no": 0,
    "white_job_percentage": 0,
    "blue_job_percentage": 0,
    "pink_job_percentage": 0,
}

profession_stats = {
    "profession": 0,
    "employed_no": 0,
    "unemployed_no": 0,
    "salary_wage_average": 0,
    "experience_average": 0,
    "profession_percentage": 0,
    "district": 0
}

relief_bene = {
    "r_id": 0,
    "nic": 0,
    "rr_id": 0
}

nic_list = {
    "nic": 0
}

count = 0

# ---------------------------------------------------------------------------------------------------
# 
#                                       Functions
# 
# ----------------------------------------------------------------------------------------------------


# This function is used to fetch 11 latest records from Organization table
# Write appopriate query for that inside the function

def prep_org_list():
    
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT * FROM Organization ORDER BY rowid DESC LIMIT '11'")
    data = rows.fetchall()
    conn.commit()
    conn.close()
    return data

# This function is used to fetch 11 latest records from Relief Registration table
# Write appopriate query for that inside the function

def prep_relief_reg_list():
    
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT RR_id, Registration_No, Relief_Awarded, Total_People, Date FROM Relief_Record ORDER BY rowid DESC LIMIT '11'")
    data = rows.fetchall()
    conn.commit()
    conn.close()
    return data

# This function is used to fetch 11 latest records from Bio table
# Write appopriate query for that inside the function

def prep_bio_list():

    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT NIC, Name, Age, Gender, District FROM Bio ORDER BY rowid DESC LIMIT '11'")
    data = rows.fetchall()
    conn.commit()
    conn.close()
    return data

def number_check(a):
    num = ['0','1','2','3','4','5','6','7','8','9', '-']
    for item in range(0,len(a)-1):
        if a[item] not in num:
            return False
    return True

def chacracter_check(a):
    cha = ['0','1','2','3','4','5','6','7','8','9', '-']
    for item in range(0,len(a)-1):
        if a[item] in cha:
            return False
    return True

def is_digit(check_input):
    if check_input.isdigit():
        return True
    return False

def check_cnic(cnic_input):
    regex1 = "^[0-9]{4}-[0-9]{4}-[0-9]{4}$"
    if re.search(regex1,cnic_input):
        return True
    return False

def check_mobno(mobno_input):
    regex2 = "^[0]{1}[3]{1}[0-9]{2}-[0-9]{7}$"
    if re.search(regex2, mobno_input):
        return True
    return False

def check_cnic_db(cnic_input_db):
    con = sqlite3.connect('BDCS219.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT COUNT(NIC) FROM Bio WHERE NIC = ?" ,[cnic_input_db])
    rows = cur.fetchone()
    con.commit()
    con.close()
    if(rows[0] == 0):
        return True
    return False

def check_Contact_No_db(Contact_No_input_db):
    con = sqlite3.connect('BDCS219.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT COUNT(Contact_No) FROM Bio WHERE Contact_No = ?" ,[Contact_No_input_db])
    rows = cur.fetchone()
    con.commit()
    con.close()
    if(rows[0] == 0):
        return True
    return False

def check_org_regno(reg_no_input_db):
    con = sqlite3.connect('BDCS219.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT COUNT(Registration_No) FROM Organization WHERE Registration_No = ?" ,[reg_no_input_db])
    rows = cur.fetchone()
    con.commit()
    con.close()
    if(rows[0] == 0):
        return True
    return False

def unique_num():
    localtime = time.asctime(time.localtime(time.time()))
    return '{}{}{}{}-{}{}{}{}{}{}'.format(localtime[0],localtime[4],localtime[8],localtime[9],localtime[11],localtime[12],localtime[14],localtime[15],localtime[17],localtime[18])

def district_stats_input(a):
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    x1 = db.execute("UPDATE District_Stats SET Employment_No = (SELECT count(*) FROM Bio INNER JOIN Job_Details ON Job_Details.NIC = Bio.NIC WHERE Job_Details.Employment_Status = 'employed' AND Bio.District = ?) WHERE District = ?", (a,a))
    x2 = db.execute("UPDATE District_Stats SET Unemployment_No = (SELECT count(*) FROM Bio INNER JOIN Job_Details ON Job_Details.NIC = Bio.NIC WHERE Job_Details.Employment_Status = 'unemployed' AND Bio.District = ?) WHERE District = ?", (a,a))
    x3 = db.execute("UPDATE District_Stats SET HHI_Average = (SELECT round(avg(House_Hold_Income),1) AS AVGHHI FROM Bio WHERE District = ?) WHERE District = ?", (a,a))
    x4 = db.execute("UPDATE District_Stats SET Teen_Age_No = (SELECT Count(*) FROM Bio WHERE Age <= 30 AND District = ?) WHERE District = ?", (a,a))
    x5 = db.execute("UPDATE District_Stats SET Middle_Age_No = (SELECT Count(*) FROM Bio WHERE Age > 30 AND Age <= 60 AND District = ?) WHERE District = ?", (a,a))
    x6 = db.execute("UPDATE District_Stats SET Old_Age_No = (SELECT Count(*) FROM Bio WHERE Age > 60 AND District = ?) WHERE District = ?", (a,a))
    x7 = db.execute("UPDATE District_Stats SET Disable_Percentage = (SELECT count(Disabled) AS dnumber FROM Bio WHERE Disabled != 'None' AND District = ?) WHERE District = ?", (a,a))
    x8 = db.execute("UPDATE District_Stats SET Family_Members_Average = (SELECT round(avg(Family_Members),1) AS dfm FROM Bio WHERE Disabled != 'None' AND District = ?) WHERE District = ?", (a,a))
    x9 = db.execute("UPDATE District_Stats SET Women_No = ( SELECT count(*) FROM Bio WHERE Gender = 'F' AND District = ?) WHERE District = ?", (a,a))
    x10 = db.execute("UPDATE District_Stats SET Men_No = ( SELECT count(*) FROM Bio WHERE Gender = 'M' AND District = ?) WHERE District = ?", (a,a))
    conn.commit()
    conn.close()

    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT NIC FROM Job_Details WHERE Job_Category = 'Blue'")
    data_nic = rows.fetchall()
    conn.commit()
    conn.close()

    data = []
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    for item in range(0,len(data_nic)):
        rows = db.execute("SELECT * FROM Bio WHERE NIC = ? AND District = ?", (data_nic[item][0],a))
        data_bio = rows.fetchone()
        if data_bio != None:
            data.append(data_bio)
    conn.commit()
    conn.close()
        
    c1 = len(data)

    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT NIC FROM Job_Details WHERE Job_Category = 'Pink'")
    data_nic = rows.fetchall()
    conn.commit()
    conn.close()

    data = []
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    for item in range(0,len(data_nic)):
        rows = db.execute("SELECT * FROM Bio WHERE NIC = ? AND District = ?", (data_nic[item][0],a))
        data_bio = rows.fetchone()
        if data_bio != None:
            data.append(data_bio)
    conn.commit()
    conn.close()
        
    c2 = len(data)

    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT NIC FROM Job_Details WHERE Job_Category = 'White'")
    data_nic = rows.fetchall()
    conn.commit()
    conn.close()

    data = []
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    for item in range(0,len(data_nic)):
        rows = db.execute("SELECT * FROM Bio WHERE NIC = ? AND District = ?", (data_nic[item][0],a))
        data_bio = rows.fetchone()
        if data_bio != None:
            data.append(data_bio)
    conn.commit()
    conn.close()

    c3 = len(data)

    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    db.execute("UPDATE District_Stats SET White_Job_Percentage = ?, Blue_Job_Percentage = ?, Pink_Job_Percentage = ? WHERE District = ?", (c3,c1,c2,a))
    conn.commit()
    conn.close()

def profession_stats_input(b,c):
    conn = sqlite3.connect('BDCS219.db')
    y1 = db = conn.cursor()
    y2 = db.execute("UPDATE Profession_Stats SET Employed_No = ( SELECT count(*) FROM Bio INNER JOIN Job_Details ON Job_Details.NIC = Bio.NIC WHERE Job_Details.Employment_Status = 'employed' AND Bio.District = ? AND Job_Details.Profession = ?) WHERE District = ? AND Profession = ?",(b, c, b, c))
    y3 = db.execute("UPDATE Profession_Stats SET Unemployed_No = ( SELECT count(*) FROM Bio INNER JOIN Job_Details ON Job_Details.NIC = Bio.NIC WHERE Job_Details.Employment_Status = 'unemployed' AND Bio.District = ? AND Job_Details.Profession = ?) WHERE District = ? AND Profession = ?",(b, c, b, c))
    y4 = db.execute("UPDATE Profession_Stats SET Salary_Wage_Average = ( SELECT avg(Job_Details.Salary_Wage) AS AVS FROM Bio INNER JOIN Job_Details ON Job_Details.NIC = Bio.NIC WHERE Bio.District = ? AND Job_Details.Profession = ?) WHERE District = ? AND Profession = ?", (b, c, b, c))
    y5 = db.execute("UPDATE Profession_Stats SET Experience_Average = ( SELECT avg(Job_Details.Experience) AS AVE FROM Bio INNER JOIN Job_Details ON Job_Details.NIC = Bio.NIC WHERE Bio.District = ? AND Job_Details.Profession = ?) WHERE District = ? AND Profession = ?", (b, c, b, c))
    conn.commit()
    conn.close()

    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT NIC FROM Job_Details WHERE Profession = ?",[c])
    data_nic = rows.fetchall()
    conn.commit()
    conn.close()

    data = []
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    for item in range(0,len(data_nic)):
        rows = db.execute("SELECT * FROM Bio WHERE NIC = ? AND District = ?", (data_nic[item][0],b))
        data_bio = rows.fetchone()
        if data_bio != None:
            data.append(data_bio)
    conn.commit()
    conn.close()

    y6 = len(data)

    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    db.execute("UPDATE Profession_Stats SET Profession_Percentage = ? WHERE Profession = ? AND District = ?", (y6,c,b))
    conn.commit()
    conn.close()


# ----------------------------------------------------------------------------------------------------
# 
#                                     Admin Features
# 
# ----------------------------------------------------------------------------------------------------

@app.route('/bio_insertion')  
def bio_insertion():
    return render_template("bio_insertion.html")

@app.route('/bio_deletion')  
def bio_deletion():
    return render_template("bio_deletion.html",bio=bio)

@app.route('/bio_updation')  
def bio_updation():
    return render_template("bio_updation.html",bio=bio)

@app.route('/job_insertion')
def job_insertion():
    return render_template("job_insertion.html")

@app.route('/job_deletion') 
def job_deletion():
    return render_template("job_deletion.html",job=job)

@app.route('/job_updation')  
def job_updation():
    return render_template("job_updation.html",job=job)

@app.route('/org_registration')  
def org_registration():
    org["reg_no"] = unique_num()
    return render_template("org_registration.html",org=org)

@app.route('/org_deletion')  
def org_deletion():
    return render_template("org_deletion.html",org=org)

@app.route('/org_updation')  
def org_updation():
    return render_template("org_updation.html",org=org)

@app.route('/relief_registration')  
def relief_registration():
    relief_reg["rr_no"] = unique_num()
    return render_template("relief_registration.html",relief_reg=relief_reg)

@app.route('/apanel/<name>')  
def apanel(name):  
    if name == 'bio_insertion':  
        return redirect(url_for('bio_insertion'))  
    if name == 'bio_deletion':  
        return redirect(url_for('bio_deletion'))  
    if name == 'bio_updation':  
        return redirect(url_for('bio_updation'))
    if name == 'job_insertion':
        return redirect(url_for('job_insertion'))
    if name == 'job_deletion':
        return redirect(url_for('job_deletion'))
    if name == 'job_updation':
        return redirect(url_for('job_updation'))
    if name == 'org_registration':
        return redirect(url_for('org_registration'))
    if name == 'org_deletion':
        return redirect(url_for('org_deletion'))
    if name == 'org_updation':
        return redirect(url_for('org_updation'))
    if name == 'relief_registration':
        return redirect(url_for('relief_registration'))

# ------------------------------------------------------------------------------------------------------------------------- 
# 
#                                                   Viewer Features
# 
# -------------------------------------------------------------------------------------------------------------------------

@app.route('/district_statistics')  
def district_statistics():
    return render_template("district_statistics.html",district_stats = district_stats)

@app.route('/profession_statistics')  
def profession_statistics():
    return render_template("profession_statistics.html",profession_stats = profession_stats)

@app.route('/bio_information')  
def bio_information():
    data = prep_bio_list()
    if len(data) != 11:
        for item in range(len(data)-11,len(data)-1):
            data.append([0,0,0,0,0])
    return render_template("bio_information.html",data = data, count = count)

@app.route('/job_information')  
def job_information():
    data = prep_bio_list()
    if len(data) != 11:
        for item in range(len(data)-11,len(data)-1):
            data.append([0,0,0,0,0])
    return render_template("job_information.html",data = data, count = count)

@app.route('/ngos_gov')
def ngos_gov():
    data = prep_org_list()
    if len(data) != 11:
        for item in range(len(data)-11,len(data)-1):
            data.append([0,0,0,0,0])
    return render_template("ngos_gov.html",data = data)

@app.route('/ref_pp')  
def ref_pp():
    data = prep_relief_reg_list()
    if len(data) != 11:
        for item in range(len(data)-11,len(data)-1):
            data.append([0,0,0,0,0])
    return render_template("ref_pp.html",data = data)

@app.route('/relief_bene')  
def relief_bene():
    data = prep_bio_list()
    if len(data) != 11:
        for item in range(len(data)-11,len(data)-1):
            data.append([0,0,0,0,0])
    return render_template("relief_bene.html",data = data, count = count)


@app.route('/vpanel/<name>')  
def vpanel(name):  
    if name == 'district_statistics':  
        return redirect(url_for('district_statistics'))  
    if name == 'profession_statistics':  
        return redirect(url_for('profession_statistics'))  
    if name == 'bio_information':  
        return redirect(url_for('bio_information'))
    if name == 'job_information':  
        return redirect(url_for('job_information'))
    if name == 'ngos_gov':  
        return redirect(url_for('ngos_gov'))
    if name == 'ref_pp':  
        return redirect(url_for('ref_pp'))
    if name == 'relief_bene':  
        return redirect(url_for('relief_bene'))  


# -----------------------------------------------------------------------------------------------------
#           
#                               ADMIN PANEL FEATURES IMPLEMENTATION
# 
# -----------------------------------------------------------------------------------------------------

# ==================================================

#   Bio INSERTION

@app.route('/F01', methods = ['POST' , 'GET'])
def f01():
    bio["cnic"] = request.form.get('f_cnic')
    bio["name"] = request.form.get('f_name')
    bio["age"] = request.form.get('f_age')
    bio["gender"] = request.form.get('f_gender')
    bio["contact_no"] = request.form.get('f_contact_no')
    bio["district"] = request.form.get('f_district')
    bio["guardian"] = request.form.get('f_guardian')
    bio["martial_status"] = request.form.get('f_martial_status')
    bio["family_members"] = request.form.get('f_family_members')
    bio["disabled"] = request.form.get('f_disabled')
    bio["hhi"] = request.form.get('f_hhi')
    if (check_cnic(bio["cnic"]) and check_mobno(bio["contact_no"]) and chacracter_check(bio["name"]) and is_digit(bio["age"]) and is_digit(bio["family_members"]) and is_digit(bio["hhi"])):
        if(check_cnic_db(bio["cnic"])):
            if check_Contact_No_db(bio["contact_no"]):
                con = sqlite3.connect('BDCS219.db')
                cur = con.cursor()
                cur.execute("INSERT INTO Bio (NIC, Name, Age, Gender, Contact_No, District, Guardian, Martial_Status, Family_Members, Disabled, House_Hold_Income) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" , (bio["cnic"], bio["name"], bio["age"], bio["gender"], bio["contact_no"], bio["district"], bio["guardian"], bio["martial_status"], bio["family_members"], bio["disabled"], bio["hhi"]))
                con.commit()
                con.close()
                flash("Person Successfully Registered.")
                district_stats_input(bio["district"])
            else:
                flash("Contact number is not unique.")
        else:
            flash("Person already registered in database.")
    else:
        flash('Please Input Correct Fields')
    bio["cnic"] = 0
    bio["name"] = 0
    bio["age"] = 0
    bio["gender"] = 0
    bio["contact_no"] = 0
    bio["district"] = 0
    bio["guardian"] = 0
    bio["martial_status"] = 0
    bio["family_members"] = 0
    bio["disabled"] = 0
    bio["hhi"] = 0
    return render_template('bio_insertion.html', bio=bio)


# Bio Updation

@app.route('/F02A', methods = ['POST'])
def f02a():
    bio["cnic"] = 0
    bio["name"] = 0
    bio["age"] = 0
    bio["gender"] = 0
    bio["contact_no"] = 0
    bio["district"] = 0
    bio["guardian"] = 0
    bio["martial_status"] = 0
    bio["family_members"] = 0
    bio["disabled"] = 0
    bio["hhi"] = 0
    if request.method == 'POST':
        try:
            bio["cnic"] = request.form['s_cnic']
            if(check_cnic(bio["cnic"])):
                con = sqlite3.connect('BDCS219.db')
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM Bio WHERE NIC = ?" ,(bio["cnic"],))
                rows = cur.fetchone()
                con.commit()
                if rows != None:
                    bio["name"] = rows[1]
                    bio["age"] = rows[2]
                    bio["gender"] = rows[3]
                    bio["contact_no"] = rows[4]
                    bio["district"] = rows[5]
                    bio["guardian"] = rows[6]
                    bio["martial_status"] = rows[7]
                    bio["family_members"] = rows[8]
                    bio["disabled"] = rows[9]
                    bio["hhi"] = rows[10]
                else:
                    bio["cnic"] = 0
                    bio["name"] = 0
                    bio["age"] = 0
                    bio["gender"] = 0
                    bio["contact_no"] = 0
                    bio["district"] = 0
                    bio["guardian"] = 0
                    bio["martial_status"] = 0
                    bio["family_members"] = 0
                    bio["disabled"] = 0
                    bio["hhi"] = 0
                    flash('Record not found. Please enter a valid cnic')
            else:
                bio["cnic"] = 0
                bio["name"] = 0
                bio["age"] = 0
                bio["gender"] = 0
                bio["contact_no"] = 0
                bio["district"] = 0
                bio["guardian"] = 0
                bio["martial_status"] = 0
                bio["family_members"] = 0
                bio["disabled"] = 0
                bio["hhi"] = 0
                flash('Please enter a valid cnic')
        except:
            con.rollback()
        finally:
            return render_template('bio_updation.html' , bio=bio)
            con.close()
# admin provided the cnic. Now we search in the database than store values in bio dictionary

@app.route('/F02B', methods = ['POST'])
def f02b():
    if request.method == 'POST':
        try:
            # bio["cnic"] = request.form['fu_cnic']
            bio["age"] = request.form['fu_age']
            bio["contact_no"] = request.form['fu_contact_no']
            bio["disabled"] = request.form['fu_disabled']
            bio["guardian"] = request.form['fu_guardian']
            bio["family_members"] = request.form['fu_family_members']
            bio["name"] = request.form['fu_name']
            bio["gender"] = request.form['fu_gender']
            bio["district"] = request.form['fu_district']
            bio["martial_status"] = request.form['fu_martial_status']
            bio["hhi"] = request.form['fu_hhi']
            # We already have a cnic from f02a function and store it in bio dictionary cnic value
            if(check_mobno(bio["contact_no"]) and is_digit(bio["age"]) and is_digit(bio["family_members"]) and is_digit(bio["hhi"])):
                conn = sqlite3.connect('BDCS219.db')
                db = conn.cursor()
                db.execute("UPDATE Bio SET Name = ?, Age = ?, Gender = ?, Contact_No = ?, District = ?, Guardian = ?, Martial_Status = ?, Family_Members = ?, Disabled = ?, House_Hold_Income = ? WHERE NIC = ?" , (bio["name"], bio["age"], bio["gender"], bio["contact_no"], bio["district"], bio["guardian"], bio["martial_status"], bio["family_members"], bio["disabled"], bio["hhi"], bio["cnic"]))
                conn.commit()
                flash("Record Successfully Updated")
                district_stats_input(bio["district"])
            else:
                flash('Please input valid fields')
        except:
            conn.rollback()
        finally:
            return render_template('bio_updation.html' , bio=bio)
            conn.close()

# Bio Deletion

@app.route('/F03A', methods = ['POST'])
def f03a():
    bio["cnic"] = 0
    bio["name"] = 0
    bio["age"] = 0
    bio["gender"] = 0
    bio["contact_no"] = 0
    bio["district"] = 0
    bio["guardian"] = 0
    bio["martial_status"] = 0
    bio["family_members"] = 0
    bio["disabled"] = 0
    bio["hhi"] = 0
    bio["cnic"] = request.form.get('s_cnic')
    # admin provided the cnic. Now we search in the database than store values in bio dictionary
    if(check_cnic(bio["cnic"])):
        con = sqlite3.connect('BDCS219.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Bio WHERE NIC = ?" ,(bio["cnic"],))
        rows = cur.fetchone()
        con.commit()
        con.close()
        if rows != None:
            bio["name"] = rows[1]
            bio["age"] = rows[2]
            bio["gender"] = rows[3]
            bio["contact_no"] = rows[4]
            bio["district"] = rows[5]
            bio["guardian"] = rows[6]
            bio["martial_status"] = rows[7]
            bio["family_members"] = rows[8]
            bio["disabled"] = rows[9]
            bio["hhi"] = rows[10]
        else:
            bio["cnic"] = 0
            bio["name"] = 0
            bio["name"] = 0
            bio["age"] = 0
            bio["gender"] = 0
            bio["contact_no"] = 0
            bio["district"] = 0
            bio["guardian"] = 0
            bio["martial_status"] = 0
            bio["family_members"] = 0
            bio["disabled"] = 0
            bio["hhi"] = 0
            flash('Record not found. Please enter a valid cnic')
    else:
        bio["cnic"] = 0
        bio["name"] = 0
        bio["age"] = 0
        bio["gender"] = 0
        bio["contact_no"] = 0
        bio["district"] = 0
        bio["guardian"] = 0
        bio["martial_status"] = 0
        bio["family_members"] = 0
        bio["disabled"] = 0
        bio["hhi"] = 0
        flash('Please enter a valid cnic')

    return render_template('bio_deletion.html' , bio=bio)


@app.route('/F03B', methods = ['POST'])
def f03b():
    # cnic already stored in the bio dictionary. Delete the record from database
    if request.method == 'POST':
        con = sqlite3.connect('BDCS219.db')
        cur = con.cursor()
        cur.execute("DELETE FROM Bio WHERE NIC = ?" , (bio["cnic"],))
        con.commit()
        con.close()

        flash("Record has been deleted")
        district_stats_input(bio["district"])

        bio["cnic"] = 0
        bio["name"] = 0
        bio["age"] = 0
        bio["gender"] = 0
        bio["contact_no"] = 0
        bio["district"] = 0
        bio["guardian"] = 0
        bio["martial_status"] = 0
        bio["family_members"] = 0
        bio["disabled"] = 0
        bio["hhi"] = 0
    return render_template('bio_deletion.html', bio=bio)

# =========================================================

# Job Insertion

@app.route('/F04', methods = ['POST'])
def f04():
    job["cnic"] = request.form['f_cnic']
    job["job_category"] = request.form['f_job_category']
    job["employment_status"] = request.form['f_employment_status']
    job["profession"] = request.form['f_profession']
    job["experience"] = request.form['f_experience']
    job["salary"] = request.form['f_salary']
    job["comment"] = request.form['f_comments']

    if(check_cnic(job["cnic"]) and is_digit(job["salary"]) and (is_digit(job["experience"]) or job["experience"] == 'null')):
        if not (check_cnic_db(job["cnic"])):
            con = sqlite3.connect('BDCS219.db')
            cur = con.cursor()
            cur.execute("INSERT INTO Job_Details (NIC, Job_Category, Employment_Status, Profession, Experience, Salary_Wage, Comment) VALUES (?, ?, ?, ?, ?, ?, ?)" , (job["cnic"], job["job_category"], job["employment_status"], job["profession"], job["experience"], job["salary"], job["comment"]))
            con.commit()
            con.close()
            flash("Job registered succesfully.")
            con = sqlite3.connect('BDCS219.db')
            cur = con.cursor()
            data = cur.execute("SELECT District FROM Bio WHERE NIC = ?" , [job["cnic"]])
            s_dist = data.fetchone()
            con.commit()
            con.close()
            profession_stats_input(s_dist[0],job["profession"])
        else:
            flash("Please register the cnic first.")
    else:
        flash('Please input valid fields')    
            
    return render_template('job_insertion.html' , job=job)

# Job Updation

@app.route('/F05A', methods = ['POST'])
def f05a():

    job["cnic"] = 0
    job["job_category"] = 0
    job["employment_status"] = 0
    job["profession"] = 0
    job["experience"] = 0
    job["salary"] = 0
    job["comment"] = 0

    job["cnic"] = request.form['s_cnic']
    job["profession"] = request.form['s1_profession']
    
    # admin provided the cnic and profession. Now we search in the database than store values in job dictionary

    if len(job["cnic"]) == 14 and check_cnic(job["cnic"]):
        conn = sqlite3.connect('BDCS219.db')
        db = conn.cursor()
        rows = db.execute("SELECT Job_Category, Employment_Status, Experience, Salary_Wage, Comment FROM Job_Details WHERE NIC = ? AND Profession = ?",(job["cnic"],job["profession"]))
        data = rows.fetchone()
        conn.commit()
        conn.close()
        if data != None:
            job["job_category"] = data[0]
            job["employment_status"] = data[1]
            job["experience"] = data[2]
            job["salary"] = data[3]
            job["prev_salary"] = data[3]
            job["comment"] = data[4]
        else:
            job["cnic"] = 0
            job["profession"] = 0
            job["job_category"] = 0
            job["employment_status"] = 0
            job["experience"] = 0
            job["salary"] = 0
            job["comment"] = 'None'
            flash('Record not found. Person is not registered or invalid cnic/profession.')

    else:
        job["cnic"] = 0
        job["profession"] = 0
        job["job_category"] = 0
        job["employment_status"] = 0
        job["experience"] = 0
        job["salary"] = 0
        job["comment"] = 'None'
        flash('Please enter a valid cnic')

    return redirect(url_for('job_updation'))


@app.route('/F05B', methods = ['POST'])
def f05b():
    job["job_category"] = request.form['f_job_category']
    job["employment_status"] = request.form['f_employment_status']
    job["experience"] = request.form['f_experience']
    job["salary"] = request.form['f_salary']
    job["comment"] = request.form['f_comments']

    if number_check(job["experience"]) or job["experience"] == 'null' and number_check(job["salary"]):
        conn = sqlite3.connect('BDCS219.db')
        db = conn.cursor()
        db.execute("UPDATE Job_Details SET Job_Category = ?, Employment_Status = ?, Experience = ?, Salary_Wage = ?, Comment = ? WHERE NIC = ? AND Profession = ?",(job["job_category"], job["employment_status"], job["experience"], job["salary"], job["comment"], job["cnic"],job["profession"]))
        conn.commit()
        conn.close()

        conn = sqlite3.connect('BDCS219.db')
        db = conn.cursor()
        rows = db.execute("SELECT House_Hold_Income FROM Bio WHERE NIC = ?", [job["cnic"]])
        data = rows.fetchone()
        conn.commit()
        conn.close()

        job["prev_salary"] = int(job["prev_salary"])
        job["salary"] = int(job["salary"])
        modified_data = data[0] - job["prev_salary"]
        modified_data = modified_data + job["salary"]

        conn = sqlite3.connect('BDCS219.db')
        db = conn.cursor()
        db.execute("UPDATE Bio SET House_Hold_Income = ? WHERE NIC = ?", (modified_data, job["cnic"]))
        conn.commit()
        conn.close()

        flash('Record Updated Successfully')

        con = sqlite3.connect('BDCS219.db')
        cur = con.cursor()
        data = cur.execute("SELECT District FROM Bio WHERE NIC = ?" , [job["cnic"]])
        s_dist = data.fetchone()
        con.commit()
        con.close()
        profession_stats_input(s_dist[0],job["profession"])

        job["cnic"] = 0
        job["profession"] = 0
        job["job_category"] = 0
        job["employment_status"] = 0
        job["experience"] = 0
        job["salary"] = 0
        job["comment"] = 'None'

    else:
        flash('Please enter valid salary or experience')

    return redirect(url_for('job_updation'))

# Job Deletion

@app.route('/F06A', methods = ['POST'])
def f06a():
    job["cnic"] = 0
    job["profession"] = 0
    job["job_category"] = 0
    job["employment_status"] = 0
    job["experience"] = 0
    job["salary"] = 0
    job["comment"] = 'None'

    job["cnic"] = request.form['s_cnic']
    job["profession"] = request.form['s1_profession']
    # search for cnic and profession in job table and store values in job dictionary if found.
    if(check_cnic(job["cnic"])):
        con = sqlite3.connect('BDCS219.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT Job_Category, Employment_Status, Experience, Salary_Wage, Comment FROM Job_Details WHERE NIC = ? AND Profession = ?",(job["cnic"],job["profession"]))
        data = cur.fetchone()
        con.commit()
        con.close()
        if data != None:
            job["job_category"] = data[0]
            job["employment_status"] = data[1]
            job["experience"] = data[2]
            job["salary"] = data[3]
            job["prev_salary"] = data[3]
            job["comment"] = data[4]
        else:           
            job["cnic"] = 0
            job["profession"] = 0
            job["job_category"] = 0
            job["employment_status"] = 0
            job["experience"] = 0
            job["salary"] = 0
            job["comment"] = 'None'
            flash('Record not found. Please input valid cnic.')
    else:
        job["cnic"] = 0
        job["profession"] = 0
        job["job_category"] = 0
        job["employment_status"] = 0
        job["experience"] = 0
        job["salary"] = 0
        job["comment"] = 'None'
        flash('Please input valid cnic.')

    return render_template('job_deletion.html', job=job)


@app.route('/F06B', methods = ['POST'])
def f06b():
    # job["cnic"] = request.form['f_cnic']
    # cnic and profession already stored in the job dictionary. Delete the record from database
    if request.method == 'POST':
        con = sqlite3.connect('BDCS219.db')
        cur = con.cursor()
        cur.execute("DELETE FROM Job_Details WHERE NIC = ? AND Profession = ?" , (job["cnic"],job["profession"]))
        con.commit()
        con.close()
    
        flash("Recoed Successfully Deleted")
        
        con = sqlite3.connect('BDCS219.db')
        cur = con.cursor()
        data = cur.execute("SELECT District FROM Bio WHERE NIC = ?" , [job["cnic"]])
        s_dist = data.fetchone()
        con.commit()
        con.close()
        profession_stats_input(s_dist[0],job["profession"])

        job["cnic"] = 0
        job["profession"] = 0
        job["job_category"] = 0
        job["employment_status"] = 0
        job["experience"] = 0
        job["salary"] = 0
        job["comment"] = 'None'
    return render_template('job_deletion.html', job=job)

# ========================================================

# Organization Registration

@app.route('/F07', methods = ['POST'])
def f07():
    # org["reg_no"] = unique_num()
    # org["reg_no"] = request.form.get('f_reg_no')
    org["type"] = 0
    org["org_name"] = 0
    org["type"] = request.form.get('f_type')
    org["org_name"] = request.form.get('f_org_name')
    con = sqlite3.connect('BDCS219.db') 
    cur = con.cursor()
    cur.execute("INSERT INTO Organization (Registration_No, Name, Type) VALUES (?, ?, ?)" , (org["reg_no"], org["org_name"], org["type"]))
    con.commit()
    con.close()
    flash("Organization Successfully Registered")
    org["reg_no"] = unique_num()
    return render_template('org_registration.html' , org=org)

# Organization Updation

@app.route('/F08A', methods = ['POST'])
def f08a():
    org["reg_no"] = 0
    org["type"] = 0
    org["org_name"] = 0
    org["reg_no"] = request.form['s_reg_no']
    conn = sqlite3.connect('BDCS219.db')
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM Organization WHERE Registration_No = ?",(org["reg_no"],))
    data = rows.fetchone()
    conn.commit()
    conn.close()
    if data != None:
        org["org_name"] = data[1]
        org["type"] = data[2]
    else:
        org["reg_no"] = 0
        org["type"] = 0
        org["org_name"] = 'None'
        flash('Record not found. Please enter valid registration number.')
    return render_template('org_updation.html' ,org=org)

@app.route('/F08B', methods = ['POST'])
def f08b():
    # org["reg_no"] = request.form['f_reg_no']
    org["type"] = request.form['f_type']
    org["org_name"] = request.form['f_org_name']
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    db.execute("UPDATE Organization SET Name = ? , Type = ?  WHERE Registration_No = ?",(org["org_name"], org["type"], org["reg_no"]))
    conn.commit()
    conn.close()
    flash("Record Succesfully Updated")
    return render_template('org_updation.html' ,org=org)

# Organization Deletion

@app.route('/F09A', methods = ['POST'])
def f09a():
    org["reg_no"] = 0
    org["type"] = 0
    org["org_name"] = 0
    org["reg_no"] = request.form['s_reg_no']
    con = sqlite3.connect('BDCS219.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Organization WHERE Registration_No = ?",(org["reg_no"],))
    data = cur.fetchone()
    con.commit()
    con.close()
    if data != None:
        org["org_name"] = data[1]
        org["type"] = data[2]
    else:
        org["reg_no"] = 0
        org["type"] = 0
        org["org_name"] = 0
        flash('Record not found. Please enter valid registration number.')
            
    return render_template('org_deletion.html', org=org)

@app.route('/F09B', methods = ['POST'])
def f09b():
    # org["reg_no"] = request.form['f_reg_no']
    con = sqlite3.connect('BDCS219.db')
    cur = con.cursor()
    cur.execute("DELETE FROM Organization WHERE Registration_No = ?" , (org["reg_no"],))
    con.commit()
    con.close()
    org["reg_no"] = 0
    org["type"] = 0
    org["org_name"] = 0
    flash("Record has been deleted.")
    return render_template('org_deletion.html', org=org)

# ======================================================

# Relief Rejistration
@app.route('/F10', methods = ['POST'])
def f10():
    # relief_reg["rr_no"] = request.form['f_rr_no']
    org["reg_no"] = request.form['f_reg_no']
    relief_reg["relief_awarded"] = request.form['f_relief_awarded']
    # relief_reg["total_people"] = request.form['f_total_people']
    relief_reg["date"] = request.form['f_date']
    if not (check_org_regno(org["reg_no"])):
        con = sqlite3.connect('BDCS219.db')
        cur = con.cursor()
        cur.execute("INSERT INTO Relief_Record (RR_id, Registration_No, Relief_Awarded, Total_People, Date) VALUES (?, ?, ?, ?, ?)" , (relief_reg["rr_no"], org["reg_no"], relief_reg["relief_awarded"], int(relief_reg["total_people"]), relief_reg["date"]))
        con.commit()
        con.close()
        flash("Relief Registered Successfully")
    else:
        flash("Organization is not Registered")
    
    relief_reg["rr_no"] = unique_num()
    return render_template('relief_registration.html' , org=org , relief_reg=relief_reg)


# -----------------------------------------------------------------------------------------------------
#           
#                               Viewer PANEL FEATURES IMPLEMENTATION
# 
# ------------------------------------------------------------------------------------------------------

# ================================================================

# District Statistics

@app.route('/F11', methods = ['POST'])
def f11():

    district_stats["district"] = request.form['f_district']

    con = sqlite3.connect('BDCS219.db')
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM District_Stats WHERE District = ?",[district_stats["district"]])
    data = rows.fetchone()
    con.commit()
    con.close()

    district_stats["employment_no"] = data[1]
    district_stats["unemployment_no"] = data[2]
    district_stats["hhi_average"] = data[3]
    district_stats["teen_age_no"] = data[4]
    district_stats["middle_age_no"] = data[5]
    district_stats["old_age_no"] = data[6]
    district_stats["disable_percentage"] = data[7]
    district_stats["family_members_average"] = data[8]
    district_stats["women_no"] = data[9]
    district_stats["men_no"] = data[10]
    district_stats["white_job_percentage"] = data[11]
    district_stats["blue_job_percentage"] = data[12]
    district_stats["pink_job_percentage"] = data[13]

    return render_template("district_statistics.html",district_stats = district_stats)

# Profession Statistics

@app.route('/F12', methods = ['POST'])
def f12():

    profession_stats["profession"] = request.form['f_profession']
    profession_stats["district"] = request.form['f_district']
    
    con = sqlite3.connect('BDCS219.db')
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM Profession_Stats WHERE District = ? AND Profession = ?",(profession_stats["district"],profession_stats["profession"]))
    data = rows.fetchone()
    con.commit()
    con.close()

    profession_stats["employed_no"] = data[1]
    profession_stats["unemployed_no"] = data[2]
    profession_stats["salary_wage_average"] = data[3]
    profession_stats["experience_average"] = data[4]
    profession_stats["profession_percentage"] = data[5]

    return render_template("profession_statistics.html",profession_stats = profession_stats)

# Bio Information View

@app.route('/F13A', methods = ['POST'])
def f13a():
    bio["cnic"] = request.form['s_cnic']

    if check_cnic(bio["cnic"]):
        conn = sqlite3.connect('BDCS219.db')
        db = conn.cursor()
        rows = db.execute("SELECT NIC, Name, Age, Gender, District FROM Bio WHERE NIC = ?", [bio["cnic"]])
        data = rows.fetchone()
        conn.commit()
        conn.close()
        if data != None:
            bio["cnic"] = data[0]
            bio["name"] = data[1]
            bio["age"] = data[2]
            bio["gender"] = data[3]
            bio["district"] = data[4]
        else:
            bio["cnic"] = 0
            bio["name"] = 0
            bio["age"] = 0
            bio["gender"] = 0
            bio["district"] = 0
            flash('Record not found. Person is not registered or invalid cnic.')

    else:
        bio["cnic"] = 0
        bio["name"] = 0
        bio["age"] = 0
        bio["gender"] = 0
        bio["district"] = 0
        flash('Please enter a valid cnic')

    # first search the person in Bio table with the help of cnic which is a primary key of Bio table
    # If not found send appopriate message to browser
    # If found then fetch Name, Age, Gender and District from Bio table with the help of cnic
    # Then store cnic, name, age, gender and district in bio dictionary
    
    return render_template("bio_information.html",bio_list = bio_list, count = count)

@app.route('/F13B', methods = ['POST'])
def f13b():
    min_age = request.form['s_min_age']
    gender = request.form['s_gender']
    hhi = request.form['s_hhi']
    max_age = request.form['s_max_age']
    gurdian = request.form['s_gurdian']
    family_no = request.form['s_family_no']
    district = request.form['s_district']
    martial_status = request.form['s_martial_status']
    disability = request.form['s_disability']

    # with the help of above variables, fetch the records from Bio table
    # Store the first 11 records in Dictionaries bio, bio1, bio2, bio3, bio4, bio5, bio6, bio7, bio8, bio9, and bio10
    # In dictionaries store the values cnic, name, age, gender and district
    # Also count the records fetch from database and store it in variable count

    if number_check(min_age) and number_check(max_age) and number_check(family_no) and number_check(hhi):
        values = []

        sql = {
            "query": "SELECT NIC, Name, Age, Gender, District FROM Bio WHERE"
        }

        if min_age != '0':
            sql["query"] = sql["query"][:len(sql["query"])] + " Age >= ? AND"
            values.append(int(min_age))
        if max_age != '0':
            sql["query"] = sql["query"][:len(sql["query"])] + " Age <= ? AND"
            values.append(int(max_age))
        if hhi != '0':
            sql["query"] = sql["query"][:len(sql["query"])] + " House_Hold_Income >= ? AND"
            values.append(int(hhi))
        if family_no != '0':
            sql["query"] = sql["query"][:len(sql["query"])] + " Family_Members <= ? AND"
            values.append(int(family_no))
        if gender != 'All':
            sql["query"] = sql["query"][:len(sql["query"])] + " Gender = ? AND"
            if gender == 'Male':
                values.append('M')
            elif gender == 'Female':
                values.append('F')
            else:
                values.append('T')
        if gurdian != 'All':
            sql["query"] = sql["query"][:len(sql["query"])] + " Guardian = ? AND"
            values.append(gurdian)
        if martial_status != 'All':
            sql["query"] = sql["query"][:len(sql["query"])] + " Martial_Status = ? AND"
            values.append(martial_status)
        if disability != 'All':
            sql["query"] = sql["query"][:len(sql["query"])] + " Disabled = ? AND"
            values.append(disability)
        if district != 'All':
            sql["query"] = sql["query"][:len(sql["query"])] + " District = ? AND"
            values.append(district)
        sql["query"] = sql["query"][:len(sql["query"])] + "no"
        sql["query"] = sql["query"].replace(" ANDno", "")
        
        if len(values) == 1:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"], [values[0]])
            data = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 2:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"], (values[0], values[1]))
            data = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 3:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"], (values[0], values[1], values[2]))
            data = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 4:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"], (values[0], values[1], values[2], values[3]))
            data = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 5:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"], (values[0], values[1], values[2], values[3], values[4]))
            data = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 6:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"], (values[0], values[1], values[2], values[3], values[4], values[5]))
            data = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 7:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"], (values[0], values[1], values[2], values[3], values[4], values[5], values[6]))
            data = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 8:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"], (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7]))
            data = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 9:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"], (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8]))
            data = rows.fetchall()
            conn.commit()
            conn.close()
        else:
            flash('Something went wrong. Please try again later.')

        # Total count i.e number of records fetch from database
        count = len(data)

        if len(data) != 11:
            for item in range(len(data)-11,len(data)-1):
                data.append([0,0,0,0,0])

        nic_list["nic"] = data

    else:
        count = 'None'
        flash('Please enter valid values in filter')

    return render_template("bio_information.html",data = data, count = count)

@app.route('/F13C', methods = ['POST'])
def f13c():
    people_count = request.form['s_people_count']
    rr_no = request.form['s_rr_no']
    ref_given_count = 0
    ref_Not_given_count = 0
    count = len(nic_list["nic"])
    # if people_count is equal to null means viewer didn't filter the record. Show a message "Please filter the records first"
    # check rr_no in database. If not found show a message "Please register your relief first"

    # if both conditions satisfied, than insert the nics, which we fetch from database when viewer click filter button in f13b function,
    # into the Relief table with orgaization registration number and relief registration number
    
    if nic_list["nic"] != 0:
        if number_check(people_count) and int(people_count) <= len(nic_list["nic"]):
            if True:
                conn = sqlite3.connect('BDCS219.db')
                db = conn.cursor()
                rows = db.execute("SELECT * FROM Relief_Record WHERE RR_id = ?", [rr_no])
                data = rows.fetchone()
                conn.commit()
                conn.close()
                if data != None:
                    conn = sqlite3.connect('BDCS219.db')
                    db = conn.cursor()
                    for item in range(0,int(people_count)):
                        rows = db.execute("SELECT * FROM Relief WHERE NIC = ? AND RR_id = ?", (nic_list["nic"][item][0] , rr_no))
                        data = rows.fetchone()
                        if data == None:
                            db.execute("INSERT INTO Relief (NIC,RR_id) VALUES (?,?)", (nic_list["nic"][item][0] , rr_no))
                            ref_given_count = ref_given_count + 1
                        else:
                            ref_Not_given_count = ref_Not_given_count + 1
                    conn.commit()
                    conn.close()
                    count = len(nic_list["nic"])
                    nic_list["nic"] = 0
                    flash(f'Relief have been allocated to {ref_given_count} people.')
                    if ref_Not_given_count != 0:
                        flash(f'{ref_Not_given_count} people have not been given relief, because were given relief in the past.')
                else:
                    flash('Relief not found. Please register relief or enter a valid relief registration number')
            else:
                flash('Please enter a valid relief registration number')
        else:
            flash('Please enter or select valid number of people.')
    else:
        count = 0
        flash('Please filter the records first.')

    return render_template("bio_information.html",bio_list = bio_list, count = count)

# Job Information View

@app.route('/F14A', methods = ['POST'])
def f14a():
    cnic = request.form['s_cnic']
    profession = request.form['s1_profession']

    # first search the person in Job table with the help of cnic and profession which is a primary key of Job table
    if check_cnic(cnic):
        conn = sqlite3.connect('BDCS219.db')
        db = conn.cursor()
        rows = db.execute("SELECT NIC FROM Job_Details WHERE NIC = ? AND Profession = ?",(cnic, profession))
        data = rows.fetchone()
        conn.commit()
        conn.close()

        if data[0] == cnic:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute("SELECT Name, Age, Gender, District, NIC FROM Bio WHERE NIC = ?",[cnic])
            data = rows.fetchone()
            conn.commit()
            conn.close()
            if data != None:
                bio["cnic"] = data[4]
                bio["name"] = data[0]
                bio["age"] = data[1]
                bio["gender"] = data[2]
                bio["district"] = data[3]
            else:
                bio["cnic"] = 0
                bio["name"] = 0
                bio["age"] = 0
                bio["gender"] = 0
                bio["district"] = 0
                flash('Please enter correct cnic')
    else:
        flash('Please enter a valid cnic.')

    return render_template("job_information.html",bio_list = bio_list, count = count)

@app.route('/F14B', methods = ['POST'])
def f14b():
    job_category = request.form['s_job_category']
    employment_status = request.form['s_employment_status']
    profession = request.form['s_profession']
    experience = request.form['s_experience']
    district = request.form['s_district']
    salary = request.form['s_salary']

    count = 0

    # with the help of above variables, fetch the records from Bio table
    # Store the first 11 records in Dictionaries bio, bio1, bio2, bio3, bio4, bio5, bio6, bio7, bio8, bio9, and bio10
    # In dictionaries store the values cnic, name, age, gender and district
    # Also count the records fetch from database and store it in variable count

    if number_check(experience) and number_check(salary):
        values = []

        sql = {
            "query": "SELECT NIC FROM Job_Details WHERE"
        }

        if experience != '0':
            sql["query"] = sql["query"][:len(sql["query"])] + " Experience >= ? AND"
            values.append(int(experience))
        if salary != '0':
            sql["query"] = sql["query"][:len(sql["query"])] + " Salary_Wage <= ? AND"
            values.append(int(salary))
        if job_category != 'All':
            sql["query"] = sql["query"][:len(sql["query"])] + " Job_Category = ? AND"
            values.append(job_category)
        if employment_status != 'All':
            sql["query"] = sql["query"][:len(sql["query"])] + " Employment_Status = ? AND"
            values.append(employment_status)
        if profession != 'All':
            sql["query"] = sql["query"][:len(sql["query"])] + " Profession = ? AND"
            values.append(profession)
        sql["query"] = sql["query"][:len(sql["query"])] + "no"
        sql["query"] = sql["query"].replace(" ANDno", "")

        if len(values) == 1:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"],[values[0]])
            data_nic = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 2:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"],(values[0],values[1]))
            data_nic = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 3:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"],(values[0],values[1],values[2]))
            data_nic = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 4:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"],(values[0],values[1],values[2],values[3]))
            data_nic = rows.fetchall()
            conn.commit()
            conn.close()
        elif len(values) == 5:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"],(values[0],values[1],values[2],values[3],values[4]))
            data_nic = rows.fetchall()
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect('BDCS219.db')
            db = conn.cursor()
            rows = db.execute(sql["query"],(values[0],values[1],values[2],values[3],values[4],values[5]))
            data_nic = rows.fetchall()
            conn.commit()
            conn.close()
        data = []
        conn = sqlite3.connect('BDCS219.db')
        db = conn.cursor()
        if district == 'All':
            for item in range(0,len(data_nic)):
                rows = db.execute("SELECT NIC, Name, Age, Gender, District FROM Bio WHERE NIC = ?",[data_nic[item][0]])
                data_bio = rows.fetchone()
                if data_bio != None:
                    data.append(data_bio)
        else:
            for item in range(0,len(data_nic)):
                rows = db.execute("SELECT NIC, Name, Age, Gender, District FROM Bio WHERE NIC = ? AND District = ?", (data_nic[item][0],district))
                data_bio = rows.fetchone()
                if data_bio != None:
                    data.append(data_bio)
        conn.commit()
        conn.close()
       
       # Total count i.e number of records fetch from database
        count = len(data)

        if len(data) != 11:
            for item in range(len(data)-11,len(data)-1):
                data.append([0,0,0,0,0])

        nic_list["nic"] = data
    else:
        count = 'None'
        flash('Please enter valid experience or salary')

    return render_template("job_information.html",data = data, count = count)

@app.route('/F14C', methods = ['POST'])
def f14c():
    people_count = request.form['s_people_count']
    rr_no = request.form['s_rr_no']
    ref_given_count = 0
    ref_not_given_count = 0
    count = len(nic_list["nic"])

    if nic_list["nic"] != 0:
        if number_check(people_count) and int(people_count) <= len(nic_list["nic"]):
            if True:
                conn = sqlite3.connect('BDCS219.db')
                db = conn.cursor()
                rows = db.execute("SELECT * FROM Relief_Record WHERE RR_id = ?", [rr_no])
                data = rows.fetchone()
                conn.commit()
                conn.close()
                if data != None:
                    conn = sqlite3.connect('BDCS219.db')
                    db = conn.cursor()
                    for item in range(0,int(people_count)):
                        rows = db.execute("SELECT * FROM Relief WHERE NIC = ? AND RR_id = ?", (nic_list["nic"][item][0] , rr_no))
                        data = rows.fetchone()
                        if data == None:
                            db.execute("INSERT INTO Relief (NIC,RR_id) VALUES (?,?)", (nic_list["nic"][item][0], rr_no))
                            ref_given_count = ref_given_count + 1
                        else:
                            ref_not_given_count = ref_not_given_count + 1
                    conn.commit()
                    conn.close()
                    count = len(nic_list["nic"])
                    nic_list["nic"] = 0
                    flash(f'Relief have been allocated to {ref_given_count} people.')
                    if ref_not_given_count != 0:
                        flash(f'{ref_not_given_count} people not given relief as they got it in past.')
                else:
                    flash('releif not found. ')
            else:
                flash('Enter valid releif number')
        else:
            flash('Select valid number of people')
    else:
        count = 0
        flash('please filter record first.')

    return render_template("job_information.html",bio_list = bio_list, count = count)

# ngos and goverment relief registration

@app.route('/F15', methods = ['POST', 'GET'])
def f15():
    
    org["reg_no"] = 0
    org["type"] = 0
    org["org_name"] = 0

    org["reg_no"] = request.form['s_reg_no']
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT * FROM Organization WHERE Registration_No = ?",[org["reg_no"]])
    data = rows.fetchall()
    conn.commit()
    # return render_template('ngos_gov.html', org=org)
    conn.close()
    if data != None:
        for item in range(1,11):
            data.append([0,0,0])
    else:
        if len(data) != 11:
            for item in range(0,11):
                data.append([0,0,0])
        flash("Please enter valid registration number")
    
    return render_template("ngos_gov.html",data = data)


# Relief Record View by public and private firms

@app.route('/F16A', methods = ['POST'])
def f16a():

    relief_reg["rr_no"] = 0
    relief_reg["reg_no"] = 0
    relief_reg["relief_awarded"] = 0
    relief_reg["total_people"] = 0
    relief_reg["date"] = 0

    relief_reg["rr_no"] = request.form['s_rr_no']
    
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT * FROM Relief_Record WHERE RR_id = ?", [relief_reg["rr_no"]])
    data = rows.fetchall()
    conn.commit()
    conn.close()
    if data != None:
        if len(data) != 11:
            for item in range(len(data)-11,len(data)-1):
                data.append([0,0,0,0,0])
    else:
        for item in range(len(data)-11,len(data)-1):
            data.append([0,0,0,0,0])
        flash('Record not found')

    return render_template("ref_pp.html",data = data)

@app.route('/F16B', methods = ['POST'])
def f16b():
    
    reg_no = request.form['s_reg_no']
    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT * FROM Relief_Record WHERE Registration_No = ?", [reg_no])
    data = rows.fetchall()
    conn.commit()
    conn.close()

    if len(data) != 0:
        if len(data) != 11:
            for item in range(len(data)-11,len(data)-1):
                data.append([0,0,0,0,0])

    else:
        for item in range(len(data)-11,len(data)-1):
            data.append([0,0,0,0,0])
        flash('Record not found')

    return render_template("ref_pp.html",data = data)


# Relief Beneficieries

@app.route('/F17A', methods = ['POST'])
def f17a():

    bio["cnic"] = request.form['s_cnic']
    if(check_cnic(bio["cnic"])):
        con = sqlite3.connect('BDCS219.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Bio WHERE NIC = ?" ,(bio["cnic"],))
        data = cur.fetchall()
        con.commit()
        con.close()
        if data != None:
            if len(data) != 11:
                for item in range(len(data)-11,len(data)-1):
                    data.append([0,0,0,0,0])
        else:
            flash('Record not found. Please enter valid cnic.')
    else:
        flash('Please enter a valid cnic')

    return render_template('relief_bene.html' , data = data, count = 0)

@app.route('/F17B', methods = ['POST'])
def f17b():
    reg_no = request.form['s_reg_no']
    rr_no = request.form['s_rr_no']
    district = request.form['s_district']

    count = 0

    conn = sqlite3.connect('BDCS219.db')
    db = conn.cursor()
    rows = db.execute("SELECT * FROM Relief WHERE RR_id = ?",[rr_no])
    data = rows.fetchall()
    conn.commit()
    conn.close()

    bio_data_list = []

    if len(data) != 0:
        conn = sqlite3.connect('BDCS219.db')
        db = conn.cursor()
        for item in range(0,len(data)):
            if district == "All":
                rows1 = db.execute("SELECT * FROM Bio WHERE NIC = ?",[data[item][0]])
                bio_data = rows1.fetchone()
                bio_data_list.append(bio_data)
            else:
                rows1 = db.execute("SELECT * FROM Bio WHERE NIC = ? AND District = ?",(data[item][0], district))
                bio_data = rows1.fetchone()
                if bio_data != None:
                    bio_data_list.append(bio_data)
        conn.commit()
        conn.close()
        data = bio_data_list
        if len(data) != 11:
            for item in range(len(data)-11,len(data)-1):
                data.append([0,0,0,0,0])
    else:
        flash('No record(s). Relief has not been given or enter valid relief/organization registration number')
    # Total count i.e number of records fetch from database
    count = len(bio_data_list)
    
    return render_template("relief_bene.html",data = data, count = count)