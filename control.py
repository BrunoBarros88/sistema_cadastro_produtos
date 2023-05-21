import mysql.connector
from PyQt5 import QtWidgets, uic
from reportlab.pdfgen import canvas

id_number=0
db=mysql.connector.connect(port='3308',host='localhost',user='root',passwd='',database='product_registration')
cursor=db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS products (id INT NOT NULL AUTO_INCREMENT, quantity INT, name VARCHAR(50), price DOUBLE, category VARCHAR(20), PRIMARY KEY(id))')


def generate_pdf():
    cursor = db.cursor()
    SQL_command = "SELECT * FROM products"
    cursor.execute(SQL_command)
    data_read = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("products_list.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Registered Products:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "QUANTITY")
    pdf.drawString(210,750, "PRODUCT")
    pdf.drawString(310,750, "PRICE")
    pdf.drawString(410,750, "CATEGORY")

    for i in range(0, len(data_read)):
        y = y + 50
        pdf.drawString(10,750 - y, str(data_read[i][0]))
        pdf.drawString(110,750 - y, str(data_read[i][1]))
        pdf.drawString(210,750 - y, str(data_read[i][2]))
        pdf.drawString(310,750 - y, str(data_read[i][3]))
        pdf.drawString(410,750 - y, str(data_read[i][4]))

    pdf.save()
    print("PDF GENERATED WITH SUCESS!")

def main_func():
    line1 = form.lineEdit.text()
    line2 = form.lineEdit_2.text()
    line3 = form.lineEdit_3.text()
    
    category = ""
    if form.radioButton.isChecked() :
        print("category Meat selected")
        category ="Meat"
    elif form.radioButton_2.isChecked() :
        print("category Dairy selected")
        category ="Dairy"
    else :
        print("category Other selected")
        category ="Other"

    print("Quantity:",line1)
    print("Name:",line2)
    print("Price",line3)

    cursor = db.cursor() 
    SQL_command = "INSERT INTO products (quantity,name,price,category) VALUES (%s,%s,%s,%s)"
    data = (str(line1),str(line2),str(line3),category)
    cursor.execute(SQL_command,data)
    db.commit()
    form.lineEdit.setText("")
    form.lineEdit_2.setText("")
    form.lineEdit_3.setText("")

def call_second_screen():
    second_screen.show()

    cursor = db.cursor() 
    SQL_command = "SELECT * FROM products"
    cursor.execute(SQL_command)
    data_read=cursor.fetchall()

    second_screen.tableWidget.setRowCount(len(data_read)) 
    second_screen.tableWidget.setColumnCount(5)

    for i in range(0, len(data_read)):
        for j in range(0, 5):
           second_screen.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(data_read[i][j]))) 

def delete_data():
    line = second_screen.tableWidget.currentRow() 
    second_screen.tableWidget.removeRow(line)

    cursor = db.cursor()
    cursor.execute("SELECT id FROM products")
    data_read = cursor.fetchall()
    id_value = data_read[line][0]
    cursor.execute("DELETE FROM products WHERE id="+ str(id_value))

def editar_data():
    global id_number

    line = second_screen.tableWidget.currentRow()
    
    cursor = db.cursor()
    cursor.execute("SELECT id FROM products")
    data_read = cursor.fetchall()
    id_value = data_read[line][0]
    cursor.execute("SELECT * FROM products WHERE id="+ str(id_value))
    product = cursor.fetchall()
    edit_screen.show()

    edit_screen.lineEdit.setText(str(product[0][0]))
    edit_screen.lineEdit_5.setText(str(product[0][1]))
    edit_screen.lineEdit_4.setText(str(product[0][2]))
    edit_screen.lineEdit_3.setText(str(product[0][3]))
    id_number = id_value
def save_edited_value():
    global id_number

    # ler data do lineEdit
    quantity = edit_screen.lineEdit_5.text()
    name = edit_screen.lineEdit_4.text()
    price = edit_screen.lineEdit_3.text()
    category = ""
    if edit_screen.radioButton.isChecked() :
        print("category Dairy selected")
        category ="Dairy"
    elif edit_screen.radioButton_2.isChecked() :
        print("category Meat selected")
        category ="Meat"
    else :
        print("category Other selected")
        category ="Other"
   
    # atualizar os data no db
    cursor = db.cursor()
    cursor.execute("UPDATE products SET quantity = '{}', name = '{}', price = '{}', category ='{}' WHERE id = {}".format(quantity,name,price,category,id_number))
    db.commit()
    #atualizar as janelas
    edit_screen.close()
    second_screen.close()
    call_second_screen()
    

app=QtWidgets.QApplication([])
form=uic.loadUi("form.ui")
second_screen=uic.loadUi("list_data.ui")
edit_screen=uic.loadUi("edit_menu.ui")
form.pushButton.clicked.connect(main_func)
form.pushButton_2.clicked.connect(call_second_screen)
second_screen.pushButton.clicked.connect(generate_pdf)
second_screen.pushButton_2.clicked.connect(delete_data)
second_screen.pushButton_3.clicked.connect(editar_data)
edit_screen.pushButton.clicked.connect(save_edited_value)

form.show()
app.exec()
