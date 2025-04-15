import csv
from RBM import RBM, TrainRBM
from numpy.random import shuffle

data = []
with open('data.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        data_row = [float(item) for item in row[:-1]]
        data_row.append(row[-1])
        data.append(data_row)

def train():
    rbm = TrainRBM(1)
    for _ in range(180):
        shuffle(data)
        for row in data:
            rbm.train(row[:-1], row[-1])

    rbm.save_trained_data() 

def run_on_samples(randomize: bool): 
    print("Running...")
    accuracy = 0    
    for row in data:
        rbm = RBM(row[:-1], 100, randomize)
        result = rbm.classify()
        if result == row[-1]:
            accuracy += 1

    print("Accuracy rate:", accuracy / len(data))    


def run_on_user_input(randomize: bool):
    sample_input = input("Enter your data in format <sepal length>, <sepal width>, <petal length>, <petal width>")
    sample_input = sample_input.split(",")
    if len(sample_input)!=4:
        print("Data not in the right format")
        exit() 
    try:    
        sample_input = [float(item) for item in sample_input]
    except Exception as e:
        print("Data not in the right format")
        exit()    
    rbm = RBM(sample_input, 100, randomize)
    print(rbm.classify())



action = "-"
while action != "5":
    action = input("Welcome to RBM Iris edition!\n \
What would you like to do?\n \
0 - train the model\n \
1 - run all samples, trained model\n \
2 - run all samples, untrained model\n \
3 - enter your input, trained model\n \
4 - enter your input, untrained model\n \
5 - quit\n").strip()
    match action:
        case "0":
            train()
        case "1":
            run_on_samples(randomize=False)
        case "2":
            run_on_samples(randomize=True)            
        case "3":
            run_on_user_input(randomize=False)
        case "4":
            run_on_user_input(randomize=True)
        case "5":
            print("Gule gule")
        case _:
            print("Invalid option")
                