import csv

users = {}
def read_from_csv(dict, file):
    with open(file, mode='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            dict[lines[0]] = lines[1]

def write_to_csv(dict, file):
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for key in dict:
            csvwriter.writerow([key, users[key]])

read_from_csv(users, 'users.csv')
print(users)
users['blair'] = 'pumpkin'
print(users)
write_to_csv(users, 'users.csv')
