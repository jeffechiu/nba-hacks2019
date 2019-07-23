import numpy as np 
import csv
import datetime 
import calendar 
#reads csv file and feature engineering 


def read_data(path):
    with open(path, 'r') as f:
        data = csv.reader(f, delimiter=',') 
        #[(y, [feature vector]),...]
        X = []
        Y = []
        for i, line in enumerate(data):
            if i == 0: #first line is title
                continue 
            else:
                example = []
                Y.append(int(line[0]))
                example.append(feature_engineer(line[1:]))
                X.append(example)
    return np.array(Y), np.array(X)



def feature_engineer(x):
    feature_vector = []

    engagment = np.array([x[0]]) #engagment

    date, time, _ = x[1].split(" ")
    year, month, day = date.split("-")
    day_of_week_vector = np.zeros(7) #starts on monday
    day_of_week = datetime.date(int(year),int(month),int(day)).weekday() #0 for monday, 1 for tues...
    day_of_week_vector[day_of_week] = 1

    hours = np.zeros(24)
    hours[int(time[:2])] = 1

    medium = ["Photo", "Album", "Video"]
    medium_vector = np.zeros(3)
    medium_index = 2
    medium_vector[medium.index(x[medium_index])] = 1

    description_index = 3
    #description_vector = generate_description_vector(x[description_index])
    return np.concatenate((engagment, day_of_week_vector, hours, medium_vector))



#Y, X = read_data("training_set.csv")

