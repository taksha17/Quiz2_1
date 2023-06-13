from flask import Flask, render_template, request
import pandas as pd
import csv
import tempfile
import shutil

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        f = request.form['csvfile']
        data = []
        with open(f) as file:
            csvfile = csv.reader(file)
            for r in csvfile:
                data.append(r)
        return render_template('data.html')

@app.route("/rown", methods=['GET', 'POST'])
def rown():
    if request.method == 'POST':
        rown = request.form['rown']
        csv_reader = csv.DictReader(open('static/q1c.csv'))
        matching_records = []
        for r in csv_reader:
            if rown == r['row']:
                matching_records.append({
                    'image_path': '../static/' + r['pic'],
                    'name': r['name'],
                    'seatno': r['seat']
                })

        if matching_records:
            return render_template('rown.html', records=matching_records, message="found")
        else:
            return render_template('rown.html', error="Picture and Name did not find for Room!")


@app.route("/rnrange", methods=['GET', 'POST'])
def rownorange():
    if request.method == 'POST':
        rn1 = request.form['rn1']
        rn2 = request.form['rn2']
        seatlet = request.form['seatl']
        csv_reader = csv.DictReader(open('static/q1c.csv'))
        matching_records = []
        for r in csv_reader:
            
            if rn1 !='' and rn2 !='':
                if seatlet!='':
                    if r['row'] >= rn1 and r['row'] <= rn2 or r['seat'] == seatlet:
                        matching_records.append({
                            'image_path': '../static/' + r['pic'],
                            'name': r['name'],
                            'seatno': r['seat'],
                            'notesdesc' : r['notes']
                        })
                elif r['row'] >= rn1 and r['row'] <= rn2:
                     matching_records.append({
                            'image_path': '../static/' + r['pic'],
                            'name': r['name'],
                            'seatno': r['seat'],
                            'notesdesc' : r['notes']
                        })   

            elif r['seat'] == seatlet :
                matching_records.append({
                    'image_path': '../static/' + r['pic'],
                    'name': r['name'],
                    'seatno': r['seat'],
                    'notesdesc' : r['notes']
                })   

        if matching_records:
            return render_template('rnrange.html', records=matching_records, message="found")
        else:
            return render_template('rnrange.html', error="Picture and Name did not find for the given Room no!")
        

@app.route("/edit", methods=['GET', 'POST'])
def edit_details_by_name():
    return render_template('edit_details_by_name.html')


@app.route("/editdetails", methods=['GET', 'POST'])
def editdetails_form():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/q1c.csv'))
        temp_name = ''
        for r in csv_reader:
            if name == r['name']:
                temp_name = name
        if temp_name != '':
            return render_template('display_details_after_edit_by_name.html', name=temp_name)
        else:
            return render_template('display_details_after_edit_by_name.html', error="No Record Found!")


@app.route("/updatedetails", methods=['GET', 'POST'])
def display_updated_details():
    if request.method == 'POST':
        name = request.form['name']
        row = request.form['row']
        seat = request.form['seat']
        pic = request.files['pic']  
        notes = request.form['notes']
        cnt = 0

        temp = [name, row, seat,pic.filename,notes]  
        line = []

        with open('static/q1c.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                if name == r[0]:
                    line.append(temp)
                else:
                    line.append(r)
                cnt += 1

        with open('static/q1c.csv', 'w') as csv_write:  
            csv_writer = csv.writer(csv_write)
            csv_writer.writerows(line)

        if cnt != 0:
            return render_template('display_details_after_edit_by_name.html', update="One Record Updated Successfully.")
        else:
            return render_template('display_details_after_edit_by_name.html', error="No Record Found!")
        
@app.route("/remove", methods=['GET', 'POST'])
def remove_details_by_name():
    return render_template('remove_by_name.html')


@app.route("/removedetails", methods=['GET', 'POST'])
def remove_details_message_display():
    if request.method == 'POST':
        name = request.form['name']
        cnt = 0
        line = list()
        with open('static/q1c.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for row in csv_reader:
                line.append(row)
                if name == row[0]:
                    line.remove(row)
                    cnt += 1

        csv_write = open('static/q1c.csv', 'w')
        for i in line:
            for j in i:
                csv_write.write(j + ',')
            csv_write.write('\n')

        if cnt:
            return render_template('removedetails_validation.html', message="Record removed successfully.")
        else:
            return render_template('removedetails_validation.html', error="Record not found.")
        
@app.route("/adduser", methods=['GET', 'POST'])
def add_details_by_name():
    return render_template('adduserbyname.html')

@app.route("/adduserbn", methods=['GET', 'POST'])
def adduserbn():
    if request.method == 'POST':
        name = request.form['name']
        row = request.form['row']
        seat = request.form['seat']
        pic = request.files['pic']
        notes = request.form['notes']

        
        with open('static/q1c.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([name, row, seat, pic.filename, notes])

        return render_template('adduser.html', message="User added successfully.")
    else:
        return render_template('adduser.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
