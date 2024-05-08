from django.db import models

# Create your models here.
class login_table(models.Model):
    Username=models.CharField(max_length=100)
    password=models.CharField(max_length=15)
    type=models.CharField(max_length=100)

class caretaker(models.Model):
    LOGINID = models.ForeignKey(login_table, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=100)
    photo = models.FileField()
    place =models.FileField()
    post =models.FileField()
    pin =models.FileField()
    qualification  =models.FileField()
    join_date=models.DateField()

class patient(models.Model):
    CARETAKERID = models.ForeignKey(caretaker, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    photo = models.FileField()
    healthcondition =models.CharField(max_length=100)
    type= models.CharField(max_length=100)
    admit_date= models.DateField()
class complaint(models.Model):
    CARETAKERID= models.ForeignKey(caretaker,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)
    date=models.DateField()

class work_table(models.Model):
    CARETAKERID = models.ForeignKey(caretaker, on_delete=models.CASCADE)
    work = models.CharField(max_length=100)
    details = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=100)

class medicine_table(models.Model):
    PATIENTID = models.ForeignKey(patient, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=100)
    details = models.CharField(max_length=100)



class camera(models.Model):

    camname = models.CharField(max_length=100)
    location= models.CharField(max_length=100)

class notification(models.Model):
    CAMERAID = models.ForeignKey(camera, on_delete=models.CASCADE)
    photo = models.FileField()
    date = models.DateField()
    time =models.TimeField()
    date = models.DateField()
    status = models.CharField(max_length=100)

class pillreminder(models.Model):
    PATIENTID = models.ForeignKey(patient, on_delete=models.CASCADE)
    medicine = models.ForeignKey(medicine_table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=40)
    no_oftimes =models.BigIntegerField()
    days = models.BigIntegerField()

class patientrecords(models.Model):
    PATIENTID = models.ForeignKey(patient, on_delete=models.CASCADE)

    report = models.FileField()
    date = models.DateField()


class medicine_notification(models.Model):
    CARETAKERID = models.ForeignKey(caretaker, on_delete=models.CASCADE)
    PATIENTID = models.ForeignKey(patient, on_delete=models.CASCADE)
    medicine = models.ForeignKey(medicine_table, on_delete=models.CASCADE)
    details = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=100)

class patients_needs(models.Model):
    CARETAKERID = models.ForeignKey(caretaker, on_delete=models.CASCADE)
    PATIENTID = models.ForeignKey(patient, on_delete=models.CASCADE)
    needs = models.CharField(max_length=100)
    details = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=100)


class fall_detection(models.Model):
    PATIENTID = models.ForeignKey(patient, on_delete=models.CASCADE)
    CAMERAID = models.ForeignKey(camera, on_delete=models.CASCADE)
    time = models.CharField(max_length=40)
    date = models.DateField()
    status = models.CharField(max_length=100)
    photo = models.FileField()
    condition=models.CharField(max_length=40)


class chat_table(models.Model):
    FROMID = models.ForeignKey(login_table, on_delete=models.CASCADE,related_name="fromid")
    TOID = models.ForeignKey(login_table, on_delete=models.CASCADE,related_name="toid")
    message= models.CharField(max_length=500)
    date = models.CharField(max_length=30)
