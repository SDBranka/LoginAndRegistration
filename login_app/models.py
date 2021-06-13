from django.db import models
import re
import datetime
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

        if len(postData['first_name']) < 2 or not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "Please enter a valid first name"
        if len(postData['last_name']) < 2 or not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Please enter a valid last name"
        
        if len(postData['email']) < 2 or not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter a valid email"
        email_in_db = self.filter(email = postData['email'])        #ensure no duplicate email exists
        if email_in_db:
            errors["email"] = "This email already exists in the database"
        
        if len(postData['birthdate']) < 1:
            errors['birthdate'] = "Please enter a valid birthdate"
        if postData['birthdate'] >= str(datetime.date.today()):
            errors['birthdate'] = "Please enter a date prior to today's date"
        # over_thirteen = datetime.date.today() - datetime.timedelta(days=4745)
        # if postData['birthdate'] < (over_thirteen):
        #     errors['birthdate'] = "You must be at least 13 to register"




        #Release Date must be 13 years in the past or older
        # print(postData['release_date'])
        #splits the data from request.POST on the - into a list
        nums = postData['birthdate'].split("-")

        # print(nums[0])
        #adding 13 to the year so we can compare to present date
        add_thirteen = int(nums[0])+13
        #typecasting year back to str and saving to split list
        nums[0] = str(add_thirteen)
        #joining the split list into a whole list to turn back to date
        new_date = "-".join(nums)
            
        # print(new_date)
        #changing date str into datetime object
        date_plus_thirteen = datetime.datetime.strptime(new_date, '%Y-%m-%d')
        
        # print(datetime_object)
        # print(datetime.now())
        #if datetime has 13 years more and it's older 13 years haven't passed since bday -- birthday year should be younger than datetime.now()
        if date_plus_thirteen > datetime.datetime.now():
            errors["birthday"] = "You must be at least 13 years or older."












        if len(postData['password']) < 8:
            errors["password"] = "Please enter a valid password"
        if not postData['password'] == postData['confirm_pw']:
            errors['confirm_pw'] = "Your passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['lemail']) < 2 or not EMAIL_REGEX.match(postData['lemail']):
            errors["email"] = "Please enter a valid email"
        if len(postData['lpassword']) < 8:
            errors["password"] = "Please enter a valid password"

        email_in_db = self.filter(email = postData['lemail'])
        if not email_in_db:
            errors['email'] = "This email is not registered"
        else:
            user = User.objects.get(email=postData["lemail"])
            pw_to_hash = postData["lpassword"]
            if not bcrypt.checkpw(pw_to_hash.encode(), user.password.encode()):
                errors['email'] = "Incorrect password entered"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()