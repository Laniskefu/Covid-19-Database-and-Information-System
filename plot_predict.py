import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import easygui

n = 3 # predict one month

def x_extended(x):
    extended = x[:] # critical mistake, so used to change x because of pass by reference
    for i in range(n):
        last = extended[-1]
        if last[-2:]=='05':
            new = last[:-2]+'15'
        elif last[-2:]=='15':
            new = last[:-2]+'25'
        else:
            new = last[:5]+str(int(last[5])+1)+'05'
        extended.append(new)
    return extended

def y_extended(y, degree):
    x = [i for i in range(len(y))]
    x2 = [i for i in range(len(y)+n)]
    fit = np.polyfit(x, y, degree)
    polynomial = np.poly1d(fit)
    y2 = polynomial(x2)
    return y2

def predictone(tree_view, columns, select):
    degree = int(easygui.choicebox("Please input the max degree of the linear regression curve",
                               choices = [3,4,5,6,7]))

    countries = {}
    for item in tree_view.get_children():
        tup = tree_view.item(item, "values")
        if tup[0] not in countries: countries[tup[0]] = {}
        countries[tup[0]][tup[1]] = int(tup[select])

    means = {}
    for country in countries:
    	means[country] = sum([countries[country][date] for date in countries[country]])/len(countries[country])
    
    top10 = []
    for i in range(10):
    	if means:
    	    top = max(means, key=means.get)
    	    top10.append(top)
    	    del means[top]

    plt.figure(figsize=(10, 5))
    for top in top10:
        date = [date for date in countries[top]]
        date.sort()
        x = []
        for d in date:
            if d[7]=='5': x.append(d) # ensure every month has same number of samples
        y = [countries[top][d] for d in x]
        
        x2 = x_extended(x)
        y2 = y_extended(y, degree)

        plt.plot([d[4:] for d in x], y, 's')
        plt.plot([d[4:] for d in x2], y2, label=top)
    
    plt.xlabel('date')
    plt.ylabel('numbers')
    plt.title('Predicted '+columns[select])
    plt.legend()
    plt.show()

def predictall(tree_view, columns):
    degree = int(easygui.choicebox("Please input the max degree of the linear regression curve",
                               choices = [3,4,5,6,7]))
    
    total = {}
    for item in tree_view.get_children():
        tup = tree_view.item(item, "values")
        if tup[1] not in total: total[tup[1]] = [0 for i in range(10)]
        total[tup[1]] = [int(tup[i+2])+total[tup[1]][i] for i in range(10)]

    plt.figure(figsize=(10, 5))
    for i in range(10):
        date = [date for date in total]
        date.sort()
        x = []
        for d in date:
            if d[7]=='5': x.append(d) # ensure every month has same number of samples
        y = [total[d][i] for d in x]
        
        x2 = x_extended(x)
        y2 = y_extended(y, degree)

        plt.plot([d[4:] for d in x], y, 's')
        plt.plot([d[4:] for d in x2], y2, label=columns[i+2])

    plt.xlabel('date')
    plt.ylabel('numbers')
    plt.title('Predicted numbers of all attributes')
    plt.legend()
    plt.show()
