from django.shortcuts import render,redirect,HttpResponse
import pyodbc
import requests
import pandas as pd
import json
from django.http import JsonResponse 
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
import xlwt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
print('hheddd..')
print(make_password('22222222'))
print('---------')
def EmialValidator(request):
    API_KEY = "badnafrtwrne5bdomrajme8sqyn27j6z"
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
    resp =requests.get(
    "https://gamalogic.com/emailvrf/",
    params={"emailid": email, "apikey": API_KEY}
    )
    return JsonResponse(resp.json())



def send_mail_client(request):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    stock=cursor.execute('LowInStock').fetchall()
    if stock:
        stock_details = "\n".join([f"{item[0]} - {item[1]} left" for item in stock])
    else:
        stock_details = "All products are sufficiently stocked."
    subject = "Low Stock Alert From IBIMS"
    message = f"""
    Hello Team,
    The following products are low in stock:
   {stock_details}
 
   Regards,
   Your Inventory System
   """
    from_email=settings.EMAIL_HOST_USER
    recipient_list=['nikeshdevendran07@gmail.com']
    send_mail(subject,message,from_email,recipient_list)
    return JsonResponse({'status':'Mail Sent Sucessfully'})

def Home(request):
    return render(request,'index.html',)

def login(request):
    return render(request,'login.html')

def logout(request):
    return redirect('/')

def displayLowStock(request):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    stock=cursor.execute('LowInStock').fetchall()
    print(stock)
    cursor.close()
    Connection.close()
    return redirect(dashbord)





def Authenticate(request):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    if(request.method=='POST'):
        data=json.loads(request.body)
        email=data.get('email')
        password=data.get('password')
        result = cursor.execute("select password ,role,name from users where email=? and status=? ", [email,"active"]).fetchone()
        if result is None:
            # No user with that email
            return JsonResponse({"success": False, "redirect_url": "/", "error": "Invalid credentials"}, status=401)

        stored_hash = result[0]

        if check_password(password, stored_hash):
            request.session['role'] = result[1]
            request.session['name'] = result[2]
            return JsonResponse({"success": True, "redirect_url": "/dashboard/"})
        else:
            return JsonResponse({"success": False, "redirect_url": "/", "error": "Invalid credentials"}, status=401)

        
    

def AddProduct(request):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    if(request.method=='POST'):
      data=request.FILES.get('dataSheet')
      df=pd.read_excel(data)
      df.columns = df.columns.str.strip()
      for row in df.itertuples(index=False):
            result=cursor.execute("select * from Products where barcode=?",[str(row.Barcode)]).fetchall()
            if result:
               cursor.execute("update products set Quantity+=? where Barcode=?",[row.Quantity,str(row.Barcode)])
               print('updted')
            else:
               cursor.execute('Insert into products (ProductName,Quantity,Price,Barcode,active,vendorname) values (?,?,?,?,?,?)',[row.ProductName,row.Quantity,row.Price,str(row.Barcode),'Active','test'])
               print('inserted')
      cursor.commit()
      cursor.close()
      Connection.close()
      return JsonResponse({'status':'Inserted Sucessfully'})
    


def dashbord(request):
    role = request.session.get('role')
    name = request.session.get('name')
    print('-------------')
    print(role)
    print('-------------')
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    stock=cursor.execute('LowInStock').fetchall()
    TotalProduct=cursor.execute("FetchActiveProduct").fetchall()
    stockdata=cursor.execute('GetNameAndQuantity').fetchall()
    itemInstock=json.dumps([list(data) for data in stockdata])
    staff=cursor.execute("select * from users").fetchall()
    cursor.close()
    Connection.close()
    return render(request,'dashbord.html',{'stocks':stock,'TotalProduct':TotalProduct,'itemInstock':itemInstock,'staff':staff,'role':role,'name':name})



def edit_by_name(request,name):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    result=cursor.execute('GetProductByName ?',name).fetchone()
    cursor.close()
    Connection.close()
    return render(request,'updateProduct.html',{'data':result})
 

def updateStock(request,pname):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    if(request.method=='POST'):
        name=request.POST['pname']    
        qnt=request.POST['pqnt']    
        price=request.POST['price']   
        cursor.execute('UpdateProduct ?,?,?,?',[name,qnt,price,pname]) 
        cursor.commit()
        cursor.close()
        Connection.close()
        return redirect(dashbord)
    else:
        return redirect('/')        
    

def Deactive(request,pname):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    cursor.execute("UpdateStatus ?",pname)
    cursor.commit()
    cursor.close()
    Connection.close()
    return redirect(dashbord)


def TakeAway(request):
    return render(request,'takeAway.html')

def GenerateInvoice(request):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    if request.method == 'POST':
        data = json.loads(request.body)
        pname = data.get('pname')
        pcode = data.get('pcode')
        qnt =0 if data.get('qnt')==None else data.get('qnt')
        price = data.get('price')
        customerName=data.get('customerName')
        customerMob=data.get('customerMob')
        FullHalfPayemnt=data.get('FullHalfPayemnt')
        paymentMode=data.get('paymentMode')
        dueStart=data.get('dueStart')
        dueEnd=data.get('dueEnd')
        grandTotal=price
        PayingAmount=data.get('PayingAmount')
        balanceAmount=data.get('balanceAmount')
        item=cursor.execute('EXEC GetProductByName ?',pname).fetchall()
        print([customerName,customerMob,FullHalfPayemnt,paymentMode,dueStart,dueEnd,grandTotal,PayingAmount,balanceAmount])
        if(int(qnt)>0 and item[0][1]<int(qnt)):
            cursor.close()
            Connection.close()
            return JsonResponse({'status':'Quantity Out of Stock !!!'})
        else:
            try:
                return JsonResponse({'status':'Success'})
            except pyodbc.Error as e:
                  print("Database error:", e.args)
   
        
        
     

def getData(request,barcode):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    stockdata=cursor.execute('EXEC GetByBarcode ?',barcode).fetchall()
    print(stockdata)
    cursor.close()
    Connection.close()
    itemInstock=[list(data) for data in stockdata]
    print(itemInstock)
    return JsonResponse({"item":itemInstock})


def AddItem(request):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    if request.method == 'POST':
        data = json.loads(request.body)
        pname = data.get('pname')
        qnt =0 if data.get('pqnt')==None else data.get('pqnt')
        price = data.get('price')
        pcode = data.get('pcode')
        stockdata=cursor.execute('EXEC GetByBarcode ?',pcode).fetchall()
        if(len(stockdata)>0):
            cursor.execute('update Products set ProductName=?,Quantity+=? where barcode=?',[pname,qnt,pcode])
            cursor.commit()
            cursor.close()
            Connection.close()
            return JsonResponse({'status':'Item Already Present,So Qnt Updated!!!'})
        else:
            cursor.execute('Insert into products (ProductName,Quantity,Price,Active,Barcode) values (?,?,?,?,?)',[pname,qnt,price,'Active',pcode])
            cursor.commit()
            Connection.close()
            return JsonResponse({'status':'Item Add Sucessfully'})



def vendor(request):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    data = cursor.execute("""
    SELECT b.CustomerName, b.MobileNo, b.PaymentType, b.FullHalfPayment, 
           b.BillDate, b.TotalAmount, i.ItemID, i.ProductName, i.Quantity, 
           i.Price, i.Total AS ItemTotal 
    FROM Billing b 
    INNER JOIN BillItems i ON b.MobileNo = i.MobileNo
""").fetchall()

    bills = {}
    for row in data:
        key = (row[1], row[4])  
        if key not in bills:
            bills[key] = {
                'customer': {
                    'name': row[0],
                    'mobile': row[1],
                    'payment_type': row[2],
                    'payment_mode': row[3],
                    'bill_date': row[4].strftime("%Y-%m-%d %H:%M:%S"),
                    'total_amount': float(row[5])
                },
                'items': []
            }
        bills[key]['items'].append({
            'product': row[7],
            'qty': row[8],
            'total': float(row[9])
        }) 
    vendors=cursor.execute("SELECT  p.ProductName,p.Quantity,p.Price, p.Active,p.Barcode,p.VendorName,v.StoreName,v.Address FROM Products p JOIN Vendors v ON p.VendorName = v.VendorName;").fetchall()
    print(vendors)
    return render(request, 'vendor.html', {
    'vendors': vendors,
    'bills': bills.values(),
    })


def BillingInfo(request):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        cursor.execute("insert into Billing (CustomerName,MobileNo,PaymentType,FullHalfPayment,TotalAmount) values(?,?,?,?,?)",[data.get('cname'),data.get('mob'),data.get('PaymentType'),data.get('HalfFull'),data.get('Total')])
        cursor.commit()

        for product in data.get('items',[]):
            cursor.execute('update products set Quantity-=? where Barcode=?',[product['qnt'],product['bc']])


        for item in data.get('items'):
            cursor.execute("insert into BillItems(MobileNo,ProductName,Quantity,Price,Total)values(?,?,?,?,?)",[data.get('mob'),item['name'],item['qnt'],item['price'],item['total']])
            cursor.commit()
    return HttpResponse(status=204)  


def export_product_sales_to_excel(request):
    Connection = pyodbc.connect(
        'Driver={ODBC Driver 18 for SQL Server};'
        'Server=NIKESH;'
        'Database=Inventory;'
        'Encrypt=no;'
        'Trusted_Connection=yes;'
    )
    cursor = Connection.cursor()
    query = """
SELECT 
    b.MobileNo,
    b.ProductName,
    b.Quantity,
    p.BillDate,
	b.Price
FROM 
    BillItems b
JOIN 
    Billing p ON b.MobileNo = p.MobileNo
WHERE 
     MONTH(p.BillDate) =  MONTH(GETDATE()) AND
    YEAR(p.BillDate) = YEAR(GETDATE());
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Product Sales')

    header_style = xlwt.easyxf('font: bold 1; align: horiz center')

    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, header_style)

    for row_num, row in enumerate(rows, start=1):
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value))  

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=product_sales_current.xls'
    wb.save(response)
    cursor.close()
    Connection.close()

    return response



def export_product_sales_to_excel_prevoius(request):
    Connection = pyodbc.connect(
        'Driver={ODBC Driver 18 for SQL Server};'
        'Server=NIKESH;'
        'Database=Inventory;'
        'Encrypt=no;'
        'Trusted_Connection=yes;'
    )
    cursor = Connection.cursor()
    query = """
	SELECT 
    b.MobileNo,
    p.ProductName,
    p.Quantity,
    b.BillDate
FROM 
    Billing b
JOIN 
    BillItems p ON b.MobileNo = p.MobileNo
WHERE 
    MONTH(b.BillDate) = MONTH(DATEADD(MONTH ,-1, GETDATE())) AND
    YEAR(b.BillDate) = YEAR(DATEADD(MONTH, -1, GETDATE()));
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Product Sales')
    header_style = xlwt.easyxf('font: bold 1; align: horiz center')

    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, header_style)

    for row_num, row in enumerate(rows, start=1):
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value))  
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=product_sales_prevoiusMonth.xls'

    wb.save(response)
    cursor.close()
    Connection.close()
    return response


def gemini_chat(request):
    if request.method == "POST" or request.method=='GET':
        try:
            # Parse JSON body (from fetch POST)
            body = json.loads(request.body.decode("utf-8"))
            user_input = body.get("user_input", "")

            if not user_input.strip():
                return JsonResponse({"error": "No input provided"}, status=400)

            # Consultant prompt
            prompt_intro = """
You are my dedicated Inventory Management Consultant. 
Your role is to act like a domain expert and provide me with professional guidance 
whenever I ask about inventory, sales performance, demand forecasting, or stock control. 

Please ensure your responses include:
- Clear, practical explanations I can apply in real situations. 
- Actionable strategies and step-by-step recommendations. 
- Real-world examples, best practices, or industry insights when relevant. 
- Suggestions for improving efficiency, reducing costs, and preventing stockouts or overstocking. 

Always answer in a consultant tone: analytical, helpful, and focused on driving better 
inventory decisions for my business.
"""

            API_KEY = "AIzaSyBUTtsGCIMdvJVvPYkpDmsPwuXRTzycjSw"
            MODEL_NAME = "gemini-1.5-flash-latest"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": prompt_intro},
                            {"text": user_input}   # ✅ add actual user question
                        ]
                    }
                ]
            }

            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                result = response.json()
                text_output = result['candidates'][0]['content']['parts'][0]['text']
                return JsonResponse({"response": text_output})
            else:
                return JsonResponse(
                    {"error": "Gemini API error", "details": response.text},
                    status=500
                )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


def Staff(request):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')   
        role = data.get('role')
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", [email])
        exists = cursor.fetchone()[0]

        if exists:
            return JsonResponse({'message': 'User already exists!'}, status=400)

        cursor.execute(
            "INSERT INTO users (Name, email, password, role,status) VALUES (?,?,?, ?, ?)",
            [name, email, make_password(password), role,'active']
        )
        Connection.commit()

        return JsonResponse({'message': 'User Created Successfully!'})


def FreeseStaff(request,email):
    Connection=pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'server=NIKESH;'
                          'Database=Inventory;'
                          'Encrypt=no;'
                          'Trusted_Connection=yes;')
    cursor=Connection.cursor()
    cursor.execute("update users set status=? where email=?",'deactive',email)
    cursor.commit()
    cursor.close()
    Connection.close()
    return redirect(dashbord)