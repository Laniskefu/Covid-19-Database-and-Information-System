import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def currentone(tree_view, columns, select):
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
    
    for top in top10:
        date = [date for date in countries[top]]
        date.sort()
        x = []
        for d in date:
            if d[7]=='5': x.append(d) # ensure every month has same number of samples
        y = [countries[top][d] for d in x]
        
        plt.plot([d[4:] for d in x], y, label=top)
    
    plt.xlabel('date')
    plt.ylabel('numbers')
    plt.title(columns[select])
    plt.legend()
    plt.show()

def currentall(tree_view, columns):
    total = {}
    for item in tree_view.get_children():
        tup = tree_view.item(item, "values")
        if tup[1] not in total: total[tup[1]] = [0 for i in range(10)]
        total[tup[1]] = [int(tup[i+2])+total[tup[1]][i] for i in range(10)]
    
    for i in range(10):
        date = [date for date in total]
        date.sort()
        x = []
        for d in date:
            if d[7]=='5': x.append(d) # ensure every month has same number of samples
        y = [total[d][i] for d in x]
        
        plt.plot([d[4:] for d in x], y, label=columns[i+2])

    plt.xlabel('date')
    plt.ylabel('numbers')
    plt.title('Numbers of all attributes')
    plt.legend()
    plt.show()
