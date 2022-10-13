from django.db import models

class user_reg(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password1=models.CharField(max_length=255)
    password2=models.CharField(max_length=255)

class userreg(models.Model):
    user_id = models.IntegerField()
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    username = models.CharField(max_length=50)
    pass1=models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    
    def __str__(self): 
        return self.name
  


class farmer_reg(models.Model):

    name=models.CharField(max_length=255)
    address=models.TextField()
    phone=models.CharField(max_length=12)
    email=models.EmailField(max_length=255)
    place=models.CharField(max_length=255)
    pincode=models.TextField()
    password1=models.CharField(max_length=255)
    password2=models.CharField(max_length=255)



class farmerreg(models.Model):
    user_id = models.IntegerField(null=True)
    name=models.CharField(max_length=255)
    address=models.TextField()
    phone=models.CharField(max_length=12)
    email=models.EmailField(max_length=255)
    place=models.CharField(max_length=255)
    pincode=models.TextField()
    username=models.CharField(max_length=255)
    pass1=models.CharField(max_length=255)
     
     
    def __str__(self): 
        return self.name



class krishireg(models.Model):
    name=models.CharField(max_length=255)
    address=models.TextField()
    phone=models.CharField(max_length=12)
    email=models.EmailField(max_length=255)
    city=models.CharField(max_length=255)
    pincode=models.TextField()
    password1=models.CharField(max_length=255)
    password2=models.CharField(max_length=255)
    status=models.BooleanField(default=False)
   

class krishireg1(models.Model):
    user_id = models.IntegerField()
    name=models.CharField(max_length=255)
    address=models.TextField()
    phone=models.CharField(max_length=12)
    email=models.EmailField(max_length=255)
    city=models.CharField(max_length=255)
    pincode=models.TextField()
    username = models.CharField(max_length=50,null=True)
    pass1=models.CharField(max_length=255)
    status=models.BooleanField(default=False)

    def __str__(self): 
        return self.name


class feed(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    description=models.TextField()


class solreq(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    description=models.TextField()

class user_login(models.Model):
    username = models.CharField(max_length=50)
    pass1 = models.CharField(max_length=50)
    u_type = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id} - {self.username}'

class solreq1(models.Model):
    user_id = models.IntegerField(null=True)
    #name=models.CharField(max_length=255)
    #email=models.EmailField(max_length=255)
    description=models.TextField()
    dt=models.DateField(null=False)
    status=models.CharField(max_length=255)


class farmerrequest1(models.Model):
    user_id = models.IntegerField()
    kid=models.ForeignKey(krishireg1,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=255,null=True)
    email=models.EmailField(max_length=255)
    description=models.TextField()
    dt=models.DateField(null=False)
    status = models.CharField(max_length=25)
    reply_msg = models.CharField(max_length=200,null=True,blank=True)


    
class krishreply(models.Model):
    user_id = models.IntegerField()
    farmer_id=models.ForeignKey(farmerrequest1,on_delete=models.CASCADE,null=True)
    description=models.TextField()
    dt=models.DateField(null=False)
    status = models.CharField(max_length=25)

class krishreply1(models.Model):
    user_id = models.IntegerField()
    farmer_id=models.IntegerField()
    description=models.TextField()
    dt=models.DateField(null=False)
    status = models.CharField(max_length=25)

class pfeedback1(models.Model):
    user_id = models.IntegerField(null=True)
    description=models.TextField(null=True) 
    reply=models.TextField(null=True)
    dt=models.DateField(null=False)  
    status =models.BooleanField(default=False)



