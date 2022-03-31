import shmsdbmodel

class controller:
    def __init__(self):
        self.dict = dict()
        self.db = shmsdbmodel.dbmodel()

    def save_data_to_db(self):
        check = self.db.save_data(temp =str( self.dict["temp"].get()), adh = str(self.dict["adh"].get()),bp=str(self.dict["bp"].get()), bs=str(self.dict["bs"].get()),pr = str(self.dict["pr"].get()))
        return check

    def get_data_from_db(self,adh):
        return self.db.get_data(adh)
    
    def sign_up(self,**d):
        self.db.sign_up(d["adh"].get(), d["name"].get().rstrip().lstrip(), d["cont"].get(), d["addres"].get().rstrip().lstrip(), d["dob"].get())

    def close_db(self):
        self.db.close_db()

    def login_by_adh(self,adh):
        new_adh=None
        try:
            new_adh = self.db.login_by_adh(adh)
        except:
            return None
        finally:
            self.db.close_db()
            if new_adh is not None:
                if adh in new_adh:
                    return True
                else:
                    return False
            else:
                return False
            

