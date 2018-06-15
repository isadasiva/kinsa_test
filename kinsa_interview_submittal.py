import json_lines
import sys

import csv


#object that represents users file content
class User(object):
    def __init__(self, zip, userid, fullname):
        self.zip = zip
        self.userid = userid
        self.fullname = fullname

    def __str__(self):
        return " Date : %s,  user %d, temperature %d" % (self.zip, self.userid, self.fullname)

#object that represents the readings file content
class Reading(object):

    def __init__(self, date, user, temperature):
        self.date = date
        self.user = user
        self.temperature = temperature

    def __str__(self):
        return " Date : %s,  user %d, temperature %d" % (self.date, self.user, self.temperature)



def get_sick_users_from_json_file(fjson):
    with open(fjson, 'rb') as f:  # opening file in binary(rb) mode
        sick_users = []

        for item in json_lines.reader(f):
            #ignoring healthy users as we search for only sick users
            if (item["temperature"] > 99.5):
                sick_users.append(Reading(item["date"], item["user"]["id"], item["temperature"]))

        return sick_users


def get_zip_users_from_csv_file(fcsv):
    with open(fcsv) as csvfile:
        reader = csv.DictReader(csvfile)
        users_zip_dict = {}

        for row in reader:
            #group users by zip so that we can get all of them at once
            u = User(row["zip"], row["user_id"], row["full_name"])
            if u.zip in users_zip_dict:
                users_zip_dict[u.zip].append(u)
            else:
                users = []
                users.append(u)
                users_zip_dict[u.zip] = users

        return users_zip_dict


def get_sick_users_in_zip(sick_users, zipusers):
    sickuserzip = []

    #we can't help a O[n]square here in theory. But, it is already optimized. So, should be ok.
    for user in zipusers:
        for sickuser in sick_users:
            if sickuser.user == user.userid:
                sickuserzip.append(user)

    return sickuserzip



if __name__ == "__main__":


    users_file = sys.argv[1]      #users file with path
    readings_file = sys.argv[2]   #readings file with path
    zip = sys.argv[3]  # pass existing zip


    users_dict = get_zip_users_from_csv_file(users_file)  #Note: if file is not accessible, FileNotFoundError

    sick_user_list = get_sick_users_from_json_file(readings_file)

    #Note: #not checking for key error that will be raised if zip is not present in the users_dict
    sick_user_zip_list = get_sick_users_in_zip(sick_user_list, users_dict[zip])

    for patient in sick_user_zip_list:
        print("Patient = ", patient.fullname, " userid = ", patient.userid)

