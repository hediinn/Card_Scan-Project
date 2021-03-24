import mysql.connector

class SQL:
  def __init__(self):
    self.mydb = mysql.connector.connect(host="localhost",user="root",password="",database="mtg")
   
  def searchFun(self,Key):
    mycursor =self.mydb.cursor()
    mycursor.execute("SELECT `name` FROM `cards` WHERE `name` LIKE \""+Key+"%\"")
    d=[]
    for x in mycursor:
      d.append(x[0])
    return d
  def refSerch(self,IDK):
    if self.searchFun(IDK)==[]:
      Keid= IDK.replace("s","'s", IDK.find("s"))
      test=self.searchFun(Keid)
      test.append(self.searchFun(IDK))
      return test
    else:
      return self.searchFun(IDK)
class CSV:
  def __init__(self):
    pass
class Scryfall():
  def __init__(self):
    pass
