from flask import Flask, render_template, request, redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date,time,timedelta
from multiprocessing import Value
import math

renter = Value('i', 0)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///renter.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SQLALCHEMY_BINDS"]={
    'Car_list':"sqlite:///car_list.db",
    'Car_data':"sqlite:///car_data.db",
    'Car_avaibility':"sqlite:///car_avaibility.db",
    'Customer':"sqlite:///customer.db",
    'Repair_charge':"sqlite:///repair_charge.db",
    'Yearly_stats':"sqlite:///yearly_stats.db",
    'Monthly_stats':"sqlite:///monthly_stats.db"
}

db=SQLAlchemy(app)
app.secret_key = 'mysecretkey'
app.app_context().push()

class Renter(db.Model):
    Id=db.Column(db.Text,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=True)
    password=db.Column(db.String(50),nullable=False)
    date_of_joining=db.Column(db.DateTime,default=datetime.utcnow)

class Car_list(db.Model):
    __bind_key__='Car_list'
    carNameID=db.Column(db.Integer,primary_key=True)
    carName=db.Column(db.String(200),nullable=False)
    nonAC_num=db.Column(db.Integer,default=0)
    AC_num=db.Column(db.Integer,default=0)
    per_hr=db.Column(db.Integer)
    per_km=db.Column(db.Integer)

class Car_data(db.Model):
    __bind_key__="Car_data"
    carID=db.Column(db.Integer,primary_key=True)
    carName=db.Column(db.String(200),nullable=False)
    carType=db.Column(db.String(200),nullable=False)
    MMR=db.Column(db.Integer)
    carPrice=db.Column(db.Integer)

class Car_avaibility(db.Model):
    __bind_key__="Car_avaibility"
    Id=db.Column(db.Integer,primary_key=True)
    carId=db.Column(db.Text,nullable=False)
    carName=db.Column(db.String(200),nullable=True)
    status=db.Column(db.Integer,nullable=False)#"REPAIR=2" OR "BOOKED=1"
    start_date=db.Column(db.DateTime,default=datetime.utcnow)
    end_date=db.Column(db.DateTime,default=datetime.utcnow)
    # bookingId=db.Column(db.Integer,nullable=True)

    def setrepairid(self):
        self.bookingId=self.Id
        

class Repair_charge(db.Model):
    __bind_key__="Repair_charge"
    Id=db.Column(db.Integer,primary_key=True)
    bookingId=db.Column(db.Integer,nullable=False)
    price=db.Column(db.Integer)

class Customer(db.Model):
    __bind_key__='Customer'
    customerID=db.Column(db.Integer,primary_key=True)
    bookingId=db.Column(db.Integer,nullable=False)
    custName=db.Column(db.String(200),nullable=False)
    custPhone=db.Column(db.String(200),nullable=False)
    custEmail=db.Column(db.String(200),nullable=False)
    total_pay=db.Column(db.Integer)
    advance=db.Column(db.Integer)
    bookTime=db.Column(db.DateTime,default=datetime.utcnow)
    start_date=db.Column(db.DateTime,default=datetime.utcnow)
    end_date=db.Column(db.DateTime,default=datetime.utcnow)
    mile_start=db.Column(db.Integer)
    mile_end=db.Column(db.Integer)
    fuel_price=db.Column(db.Float)
    fuel_consumed=db.Column(db.Integer)

class Yearly_stats(db.Model):
    __bind_key__="Yearly_stats"
    monthnum=db.Column(db.Integer,primary_key=True)
    month=db.Column(db.String(10),nullable=False)
    revenue=db.Column(db.Float,nullable=True)
    repairCharge=db.Column(db.Float,nullable=True)
    netProfit=db.Column(db.Float,nullable=True)
    fuelPerkm=db.Column(db.Float,nullable=True)
    orderNum=db.Column(db.Integer,nullable=True)
    
class Monthly_stats(db.Model):
    __bind_key__="Monthly_stats"
    carNameId=db.Column(db.Integer,primary_key=True)
    revenue=db.Column(db.Float,nullable=True)
    repairCharge=db.Column(db.Float,nullable=True)
    netProfit=db.Column(db.Float,nullable=True)
    fuelPerkm=db.Column(db.Float,nullable=True)
    orderNum=db.Column(db.Integer,nullable=True)


with app.app_context():
    db.create_all()

@app.route("/addToList")
def hello_world():
    hc=Car_list(carName="Honda City",nonAC_num=0,AC_num=0)
    db.session.add(hc)
    ts=Car_list(carName="Tata Sumo",nonAC_num=0,AC_num=0)
    db.session.add(ts)
    mo=Car_list(carName="Maruti Omni",nonAC_num=0,AC_num=0)
    db.session.add(mo)
    md=Car_list(carName="Maruti Dzire",nonAC_num=0,AC_num=0)
    db.session.add(md)
    mb=Car_list(carName="Mahindra Bolero",nonAC_num=0,AC_num=0)
    db.session.add(mb)
    db.session.commit()
    addDataToYearlyData()
    return render_template("index.html")


def addDataToYearlyData():
    mon=Yearly_stats(monthnum=1,month="january")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=2,month="february")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=3,month="march")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=4,month="april")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=5,month="may")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=6,month="june")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=7,month="july")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=8,month="august")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=9,month="september")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=10,month="october")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=11,month="november")
    db.session.add(mon)
    mon=Yearly_stats(monthnum=12,month="december")
    db.session.add(mon)





#*********************************************************************************************************#
# ***************************************** ADMIN DATABASE MANAGEMENT ************************************#
#*********************************************************************************************************#


@app.route("/",methods=['POST','GET'])
def submitform():
    if request.method =='POST':
        print("submitted")
        id=request.form['id']
        nam=str(request.form['name'])
        emailId=str(request.form['email'])
        # mnum=int(request.form['number'])
        password=str(request.form['pass'])
        obj=Renter(Id=id,name=nam,email=emailId,password=password)
        db.session.add(obj)
        db.session.commit()
    return render_template("index.html")

@app.route("/admin",methods=['GET','POST'])
def direct_to_admin_page():
    if request.method=='POST':
        print("login successfull")
        id=request.form['id']
        passw=request.form['lpassword']
        print(id)
        print(passw)
        admins=Renter.query.all()
        print(admins)
        admin=Renter.query.filter_by(Id=id).first()
        print(admin)
        print(type(admin))
        if(admin.password==passw):
            print("matched")
            return redirect(f"/admin/{id}")
    return render_template("loginform.html")

@app.route("/loginform")
def login_page():
    admins=Renter.query.all()
    return render_template("loginform.html")

@app.route('/admin/<string:Id>')
def admins_page(Id):
    admin=Renter.query.filter_by(Id=Id).first()
    cars=Car_list.query.all()
    print(cars)
    return render_template("admin.html",administrator=admin,carList=cars)

@app.route("/logout")
def logout():
    return redirect("/")


#*********************************************************************************************************#
# ********************************** CAR DATABASE AND MANAGEMENT *****************************************#
#*********************************************************************************************************#



@app.route('/admin/<string:adminId>/update/<int:carNameID>', methods=['GET','POST'])
def update(adminId,carNameID):
    admin=Renter.query.filter_by(Id=adminId).first()
    print(admin)
    if request.method=='POST':
        print("posted")
        carname=request.form['carname']
        cartype=request.form['cartype']
        perHourCharge=request.form['perHourCharge']
        perKmCharge=request.form['perKmCharge']
        mmr=request.form['MMR']
        todo=Car_list.query.filter_by(carNameID=carNameID).first()
        newcar=Car_data(carName=carname,carType=cartype,MMR=mmr)
        car1=Car_list.query.filter_by(carName=carname)
        todo.per_hr=perHourCharge
        todo.per_km=perKmCharge
        db.session.add(newcar)
        if(cartype=="NON AC"):
            changenum=todo.nonAC_num + 1
            todo.nonAC_num=changenum
            print(todo.nonAC_num)
        if(cartype=="AC"):
            todo.AC_num+=1
        db.session.commit()
        return redirect(f"/admin/{adminId}")
    todo=Car_list.query.filter_by(carNameID=carNameID).first()
    return render_template('update.html',todo=todo,administrator=admin)  

@app.route('/admin/<string:adminId>/delete/<int:carID>', methods=['GET','POST'])
def delete(adminId,carID):
    admin=Renter.query.filter_by(Id=adminId).first()
    if request.method=='POST':
        carname=request.form['carname']
        carId=request.form['carID']
        todo=Car_list.query.filter_by(carName=carname).first()
        todo2=Car_data.query.filter_by(carID=carId).first()
        db.session.delete(todo2)
        if(todo2.carType=="NON AC"):
            todo.nonAC_num=todo.nonAC_num - 1
            print(todo.nonAC_num)
        if(todo2.carType=="AC"):
            todo.AC_num-=1
        db.session.commit()
        return redirect(f"/admin/{adminId}")
    todo=Car_data.query.filter_by(carID=carID).first()
    return render_template('delete.html',todo=todo,administrator=admin)  

@app.route('/admin/<string:adminId>/repair/<int:carID>', methods=['GET','POST'])
def repair(adminId,carID):
    admin=Renter.query.filter_by(Id=adminId).first()
    car=Car_data.query.filter_by(carID=carID).first()
    print(admin)
    if request.method=='POST':
        car_id=carID
        car=Car_data.query.filter_by(carID=carID).first()
        carname=car.carName
        date_start_str=request.form['startTime']
        date_start=datetime.fromisoformat(date_start_str)
        date_end_str=request.form['endTime']
        date_end=datetime.fromisoformat(date_end_str)
        car=Car_data.query.filter_by(carID=carID).first()
        newrepair=Car_avaibility(carId=car_id,carName=carname,status=2,start_date=date_start,end_date=date_end)
        db.session.add(newrepair)
        db.session.commit()
        print( "gbdj",newrepair.Id)
        return redirect(f"/admin/{adminId}/repair/{carID}")
        
    allTime=Car_avaibility.query.all()
    return render_template('repair.html',allTime=allTime,administrator=admin,car=car)



@app.route('/admin/<string:adminId>/view_data')
def view_carData(adminId):
    admin=Renter.query.filter_by(Id=adminId).first()
    cars=Car_data.query.all()
    return render_template(f"car_data.html",carData=cars,administrator=admin)


#***************************************************************************************************************#
# *************************************** PLACE ORDER DATABASE AND MANAGEMENT **********************************#
#***************************************************************************************************************#


def clashes(time1,time2,carid):
    print(time1)
    print(time2)
    # print(Car_avaibility.start_date)
    # print(Car_avaibility.end_date)
    print(carid)
    query1=Car_avaibility.query.filter(Car_avaibility.carId == carid,Car_avaibility.end_date > time1,Car_avaibility.start_date < time2).all()
    print("opposite query", query1)
    if(len(query1) ==0 ):
        print("returning true")
        return True
    else:
        return False

@app.route("/check",methods=['POST','GET'])
def checking_page():
    queried_list=[]
    allcars=Car_data.query.all()
    if(request.method=='POST'):
        print("posted")
        type=request.form['type']
        start_time=request.form['start_time']+":00"
        end_time=request.form['end_time']+":00"
        
        print("check: end_time", end_time)
        session['start_time'] = start_time
        session['end_time'] = end_time
        # print(compare(start_time,end_time))
        cars=Car_data.query.filter_by(carType=type).all()
        
        for car in cars:
            presentInAvaibilityList=Car_avaibility.query.filter_by(carId=car.carID).all()
            print("presentInAvaibilityList", presentInAvaibilityList)
            if presentInAvaibilityList==None :
                queried_list.append(car)
            else:
                noclash=clashes(start_time,end_time,car.carID)
                if noclash:
                    print("type", car)
                    queried_list.append(car)
        print(queried_list)
        return render_template("check.html",cars_available=queried_list)
    return render_template("check.html",cars_available=allcars)

def costcalc(carNameID,start_time,estd_dis,end_time,is_ac):
    start_time = datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%S")
    end_time = datetime.strptime(end_time,"%Y-%m-%dT%H:%M:%S")
    time_diff=end_time-start_time
    hr=math.ceil(time_diff.total_seconds()/3600)
    
    print("time_diff=",time_diff.total_seconds(),"hr=",hr)
    if hr<4:
        hr=4
    night_start = datetime.strptime("23:00:00", "%H:%M:%S").time()
    night_end = datetime.strptime("06:00:00", "%H:%M:%S").time()

    # Initialize the counter for the number of night halts
    num_night_halts = 0

    # Loop through each day between the start and end times
    current_time = start_time
    while current_time < end_time:
    # Check if the current time is within the night halt period
        if night_start <= current_time.time() or current_time.time() <= night_end:
        # Increment the counter if the current time is within the night halt period
            num_night_halts += 1
    
    # Increment the current time by one hour
        current_time += timedelta(hours=1)

    night_halts=num_night_halts//7
    num_hrs=num_night_halts%7
    if(num_hrs!=0):
        night_halts+=1

    print(carNameID)
    obj=Car_list.query.filter_by(carNameID=carNameID).first()

    per_hr=obj.per_hr
    per_km=obj.per_km
    cost1=(int(hr))*per_hr
    cost2=((int)(estd_dis))*per_km
    if(cost1>cost2):
        max_cost=cost1
    else:
        max_cost=cost2
    
    if(is_ac=="AC"):
        max_cost*=1.5

    max_cost+=(night_halts*150)
    
    return max_cost

    




@app.route('/book/<int:carID>', methods=['GET','POST'])
def booking(carID):
    car=Car_data.query.filter_by(carID=carID).first()
    session['car_id'] = carID
    carname=car.carName
    session['car_name'] = carname
    car2=Car_list.query.filter_by(carName=carname).first()
    carNameID=car2.carNameID
    print(carNameID)
    cartype=car.carType
    session['car_type'] = cartype
    start_time = session.get('start_time')
    print("start_time")
    end_time = session.get('end_time')
    print("book: end_time_hr: ",end_time)
    if(request.method=='POST'):
        estd_dis=request.form['estd_dis']
        cost=costcalc(carNameID=carNameID,start_time=start_time,end_time=end_time,estd_dis=estd_dis,is_ac=cartype)
        session['cost'] = cost
        print("cost= ",cost)
        return render_template("booking.html",carID=carID,carname=carname,cartype=cartype,start_time=start_time,end_time=end_time,cost=cost)
    
    return render_template("book.html",carID=carID,carname=carname,cartype=cartype,start_time=start_time,end_time=end_time)
    
@app.route('/booking', methods=['GET','POST'])
def book_page():
    carID=session.get('car_id')
    carname=session.get('car_name')
    cartype=session.get('car_type')
    start_time=session.get('start_time')
    start_time_iso=datetime.fromisoformat(start_time)
    end_time=session.get('end_time')
    end_time_iso=datetime.fromisoformat(end_time)
    cost=session.get('cost')
    if(request.method=='POST'):
        cust_name=request.form['cust_name']
        cust_phone=request.form['cust_phone']
        cust_email=request.form['cust_email']
        
        book_time=datetime.now()
        pay_now=request.form['pay_now']
        newrent=Car_avaibility(carId=carID,status=1,start_date=start_time_iso,end_date=end_time_iso)
        db.session.add(newrent)
        db.session.commit()
        print(newrent.Id)
        new_cust=Customer(bookingId=newrent.Id,custName=cust_name,custPhone=cust_phone,custEmail=cust_email,total_pay=cost,advance=pay_now,bookTime=book_time,start_date=start_time_iso,end_date=end_time_iso)
        db.session.add(new_cust)
        db.session.commit()
        return render_template("booking.html",cust_name=cust_name,cust_phone=cust_phone,cust_email=cust_email,pay_now=pay_now,start_time=start_time,end_time=end_time,car_id=carID,carname=carname,cartype=cartype,cost=cost)
    
    return render_template("booking.html",carname=carname,cartype=cartype,cost=cost,start_time=start_time,end_time=end_time)


#***************************************************************************************************************#
#**************************************** STATISTCS DATA AND MANAGEMENT ****************************************#
#***************************************************************************************************************#

@app.route('/admin/<string:adminId>/adddata/<int:Id>', methods=['GET','POST'])
def addData(adminId,Id):
    admin=Renter.query.filter_by(Id=adminId).first()
    booking=Car_avaibility.query.filter_by(Id=Id).first()
    print(booking.status)
    if booking.status==2:
        if request.method=="POST":
            print("insideposted")
            price=request.form['repprice']
            price=int(price)
            obj=Repair_charge(bookingId=Id,price=price)
            db.session.add(obj)
            db.session.commit()
            print("added repair charge")
            return redirect(f"/admin/{adminId}/repair/{booking.Id}")
        return render_template("adddata.html",administrator=admin,status=booking.status,bookingId=Id)
    if(booking.status==1):
        if request.method=="POST":
            order=Customer.query.filter_by(bookingId=Id).first()
            order.mile_start=request.form['MMRstart']
            order.mile_end=request.form['MMRend']
            order.fuel_price=request.form['fuel_price']
            order.fuel_consumed=request.form['fuel_consumed']
            db.session.commit()
            print("successfully")
            return redirect(f"/admin/{adminId}/repair/{booking.Id}")
        return render_template("adddata.html",administrator=admin,status=booking.status,bookingId=Id)




@app.route('/admin/<string:adminId>/stats/<int:carNameID>', methods=['GET','POST'])
def stats(adminId,carNameID):
    admin=Renter.query.filter_by(Id=adminId).first()
    cartype=Car_list.query.filter_by(carNameID=carNameID).first()
    print(admin)
    if(request.method=='POST'):
        type=request.form['cartype']
        name=Car_list.query.filter_by(carNameID=carNameID).first().carName
        year=request.form['year']
        # st=f"{year}-01-01T00:00:00"
        # yearst=datetime.strptime(st,"%Y-%m-%dT%H:%M:%S")
        year=int(year)
        year1=year+1
        year1=str(year1)
        # end=f"{year1}-01-01T00:00:00"
        # yearend=datetime.strptime(end,"%Y-%m-%dT%H:%M:%S")
        # yearlydata=Car_avaibility.query.filter(Car_avaibility.start_date > yearst, Car_avaibility.start_date < yearend).all()
        # print(yearlydata)
        for i in range(1,13):
            if(i<10):
                st=f"{year}-0{i}-01T00:00:00"
            else:
                st=f"{year}-{i}-01T00:00:00"
                
            if((i+1)<10):
                end=f"{year}-0{i+1}-01T00:00:00"
            else:
                if(i+1==13):
                    end=f"{year1}-01-01T00:00:00"
                else:
                    end=f"{year}-{i+1}-01T00:00:00"
            monthst=datetime.strptime(st,"%Y-%m-%dT%H:%M:%S")
            monthend=datetime.strptime(end,"%Y-%m-%dT%H:%M:%S")
            monthlydata=Car_avaibility.query.filter(Car_avaibility.start_date > monthst, Car_avaibility.start_date < monthend,Car_avaibility.carName == name).all()
            print(i,"th month",monthlydata)
            ordersnum=0
            sumfk=0
            revsum=0
            repairnum=0
            repch=0
            for car in monthlydata:
                if car.status==1:
                    ordersum=ordersum+1
                    order=Customer.query.filter_by(car.Id).first()
                    fk=order.fuel_consumed/(order.mile_start-order.mile_end)
                    totalrevenue=order.total_pay-order.fuel_consumed*order.fuel_price
                    sumfk=sumfk+fk
                    revsum=revsum+totalrevenue
                else:
                    repair=Repair_charge.query.filter_by(bookingId=car.Id).first()
                    repch=repch+repair.charge
                    repairnum=repairnum+1
            avgfk=sumfk/ordersnum
            avgrevenue=revsum/ordersnum
            avgrepair=repch/repairnum
            netrev=avgrevenue-avgrepair
            month=Yearly_stats.query.filter_by(monthnum=i)
            month.revenue=netrev
            month.repairCharge=avgrepair
            month.netProfit=netrev
            month.fuelPerkm=avgfk
            month.orderNum=ordersnum
            db.session.commit()
        return render_template("stats.html",administrator=admin,cartype=cartype)
    return render_template("stats.html",administrator=admin,cartype=cartype)


if __name__== "__main__":
    app.run(debug=True, port=5000)



    # f70c04a5-c1f6-4dc8-8545-1d95d00f306e