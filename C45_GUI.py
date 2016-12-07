# GUI to act as a driver for the C45 algorithm
# CT475 Machine Learning & Data Mining Assignment 3
# Conor Creagh - 13454222
# David Daly - 13504817

# (Note) If using the GUI, we have oberved the following nbug and have been unable to find the fix
# -> After we first fun the GUI by inputting the train % and # of runs, cliking on results shows a blank file
# -> To fix this you have to click train again, followed by test again, and this time the reults should be present in the file

import tkinter as tk
import os
import C45
import pandas as pd
import sys

#Author: Conor Creagh

dataSet = pd.read_csv('owls15.csv')

def changePrint():
    sys.stdout = open('results.txt', 'w')


class GUI(tk.Frame):
    #initialise GUI object
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.create_gui()
        self.test_data = []
        self.tree = []


    def create_gui(self):
        use_test_df = tk.IntVar()
        result = tk.StringVar()
        data = tk.StringVar()


        #function used when train button is clicked
        #builds a tree from the training data
        def train():
            train, test = C45.partitionData(dataSet, percent.get() / 100)
            inprogress_box.config(text = "Creating decision tree...")
            self.tree = C45.train(train)
            C45.printTree(self.tree)
            self.test_data = test
            # C45.printTreeToFile(text_file, self.tree)

        #function for when the results button is clicked
        #opens results.txt to allow the user to see results
        def show_results():
            partition_label.config(text = "Partitioning at " + str(percent.get()) + '%')
            os.startfile('results.txt')
            inprogress_box.config(text = "opening results...")

        #function for when the test button is clicked
        #tests the accuracy of the tree using the number of runs the user enters and prints them to file
        def test():
            changePrint() #change the stdout to be the file, rather than the terminal
            inprogress_box.config(text="testing decision tree...")
            labels = self.test_data['type']
            del self.test_data['type']
            num = number_tests.get()
            results = []
            #taken from test_tree function in C45.py but modified to use values from UI here
            for i in range(num):
                train_data, test_data = C45.partitionData(dataSet, 0.3);
                tree = C45.train(train_data)
                types = test_data['type']
                del test_data['type']
                str1="Test " + str(i + 1) + "\n------------"
                print(str1)

                print("Tree Generated:" + "\n")
                C45.printTree(tree)
                print()
                incorrect, correct, accuracy = C45.test_tree(test_data, types, tree)
                print("Accuracy: " + str(accuracy))
                print()
                results.append(accuracy)

            sum = 0
            for r in range(len(results)):
                sum += results[r]
            print("Average Accuracy after " + str(num) + " runs")
            print(sum / num)

        #variables to hold the percent split and numbe of runs entered on the GUI
        percent = tk.IntVar()
        number_tests = tk.IntVar()

        size = tk.Label() #widger that sets size for GUI

        #set up text boxes and lables
        tests_box = tk.Label(text = 'Number of tests')      #label the number of tests box
        num_tests = tk.Entry(textvariable = number_tests)       #allow user entry for number of tests
        data_size = tk.Entry(text = 'sample', textvariable = percent)       #entry widget for partitioning data
        partition_label = tk.Label(text = 'Enter partition percent')    #button to partition data
        train_button = tk.Button(text = 'Train classifier', command = train)
        quit_button = tk.Button(text = 'Quit' , fg = 'red', command = root.destroy)
        result_box = tk.Label(text = '') #printtree?
        inprogress_box = tk.Label(text = 'test') #program status
        result_button = tk.Button(text = 'Results', command = show_results)
        test_classifier = tk.Button(text = 'Test Tree', command=test)

        #place text boxes and labels on the UI
        data_size.place(x = 10, y = 10, width = 20, height = 20)
        partition_label.place(x = 35, y = 10, width = 130, height = 25)
        train_button.place(x = 165, y =10, width = 100, height = 25)
        result_button.place(x = 10, y = 50, width = 75, height = 25)
        # result_button.place(y = 50, x = 115, height = 25)
        test_classifier.place(y = 50, x = 100, width = 75, height = 25)
        num_tests.place(x = 190, y = 55, width = 20)
        tests_box.place(x = 210, y = 55)
        inprogress_box.place(y = 150, x = 100)
        quit_button.place(y = 200, x = 270)
        size.pack(padx = 152, pady = 105)


#start the UI
root = tk.Tk()
app = GUI(master = root)
app.mainloop()
