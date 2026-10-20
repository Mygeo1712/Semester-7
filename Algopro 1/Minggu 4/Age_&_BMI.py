#Nessted IF Statement
age = int(input("Enter Age: "))
bmi = float (input("Enter BMI: "))
if age < 45:
    if bmi < 22.0:
        print ("low")
    else:
        print ("medium")
else:
    if bmi < 22.0:
        print ("medium")
    else:
        print ("high")

#Baru
young = age< 45
slim = bmi < 22.0

if young:
    if slim:
        print ("low")
    else:
        print ("medium")

else:
    if slim:
        print ("medium")
    else:
        print ("high")


if young and slim:
    print ("low")
if not young and slim:
    print ("medium")
if not young and not slim:
    print ("high")

