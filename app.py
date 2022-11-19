from flask import Flask, render_template, request, url_for,redirect
import sqlite3


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/booker/', methods = ["GET","POST"])
def booker():
    if request.method == "GET":
        return render_template("booker.html")
    else:
        bookername = request.form['bookername']
        ccaname = request.form['ccaname']
        datee = request.form['datee']
        venue = request.form['venue']
        nop = request.form['nop']
        conn = sqlite3.connect("rvpc.db")
        query = '''
        INSERT INTO Booker(BookerName,CCAName,Date,Venue,NOP) VALUES(?,?,?,?,?)
        '''
        conn.execute(query,(bookername,ccaname,datee,venue,nop))
        conn.commit()
        print("inserted")
        conn.close()
        return redirect(url_for('bsuccess'))

@app.route('/check/', methods = ["GET","POST"])
def check():
    if request.method == "GET":
        return render_template("booker_check.html")

    else:
        ccaname = request.form['ccaname']
        query = "SELECT * FROM Booker WHERE CCAName = ?"
        conn = sqlite3.connect("rvpc.db")
        cursor = conn.execute(query,(ccaname,))
        data = cursor.fetchall()
        conn.close()
        return render_template("booker_result.html",data =data)


@app.route('/validation/', methods = ["GET","POST"])
def validation():
    if request.method == "GET":
        return render_template("password.html")
    else:
        password = request.form['password']
        username = request.form['username']

        print("_________")
        print(password,username)

        if password == "lala" and username == "xiaoming":
            return redirect(url_for('administrator'))
            
        else:
            print("----wrong")
            return redirect(url_for('validation'))

            
@app.route('/administrator/')
def administrator():    
    conn = sqlite3.connect("rvpc.db")
    query = "SELECT * FROM Booker"
    cursor = conn.execute(query)
    data = cursor.fetchall()
    conn.close()
    return render_template("administrator.html",data = data)

@app.route('/administrator/accept/<int:BookingRecord>/')
def accept(BookingRecord):
    conn = sqlite3.connect("rvpc.db")
    query = '''
    Update Booker SET Status = "True" AND Reviewed = "True" WHERE BookingRecord = ?
    '''
    conn.execute(query,(BookingRecord,))
    print("________")
    print(BookingRecord)
    conn.commit()
    conn.close()
    return redirect(url_for('asuccess'))

@app.route('/administrator/decline/<int:BookingRecord>/')
def decline(BookingRecord):
    conn = sqlite3.connect("rvpc.db")
    query = '''
    Update Booker SET Reviewed = "True" WHERE BookingRecord = ?
    '''
    conn.execute(query,(BookingRecord,))
    print("________")
    print(BookingRecord)
    conn.commit()
    conn.close()
    return redirect(url_for('administrator'))

@app.route('/asuccess/')
def asuccess():
    return render_template("asuccess.html")

@app.route('/bsuccess/')
def bsuccess():
    return render_template("bsuccess.html")

if __name__ == "__main__":
    app.run(debug = True)