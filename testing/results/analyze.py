#!/usr/bin/env python3

import numpy
import json
from scipy import optimize
from scipy.stats.distributions import t
import matplotlib.pyplot as plt
import os

def func(x, a, b, z):
    """ The function that we are going to try to fit"""
#    return z + a * numpy.exp(b*x)
    return z + a * x ** b

def analyze_results(analysis_file, prediction):
    with open('{}.json'.format(analysis_file), 'r') as file:
        data1 = json.load(file)

    x = []
    y = []
    for key, value in data1.items():
        x.append(float(key))
        y.append(float(value))

    print("Len x: {} Len y: {}".format(len(x), len(y)))

    x = numpy.array(x)
    y = numpy.array(y)

    # Get the fit and covariance
    fit, covar = optimize.curve_fit(func, x, y, p0=(15, 0, 0))
    print(fit)
    a = fit.tolist()[0]
    b = fit.tolist()[1]
    z = fit.tolist()[2]

    # Do some confidence analysis
    # http://kitchingroup.cheme.cmu.edu/blog/2013/02/12/Nonlinear-curve-fitting-with-parameter-confidence-intervals/

    alpha = 0.05 # 95% confidence interval = 100*(1-alpha)

    n = len(y)    # number of data points
    p = len(fit) # number of parameters

    dof = max(0, n - p) # number of degrees of freedom

    # student-t value for the dof and confidence level
    tval = t.ppf(1.0-alpha/2., dof)

    lower = []
    upper = []
    with open('{}.md'.format(analysis_file), 'w') as file:
        file.write('# {}\n'.format(analysis_file))
        a = fit.tolist()[0]
        b = fit.tolist()[1]
        z = fit.tolist()[2]

        print("a = {}".format(a))
        file.write("\na = {}\n".format(a))
        print("b = {}".format(b))
        file.write("b = {}\n".format(b))
        print("z = {}".format(z))
        file.write("z = {}\n".format(z))

        seconds = func(prediction, a, b, z)
        hours = round(0.000277778 * seconds, 2)
        days = round(.000011574 * seconds, 2)
        prediction_text = "Prediction for {}: {} + {} exp({} * 10000) = {} seconds OR {} hours OR {} days".format(prediction, round(z, 2), round(a, 2), round(b, 2), seconds, hours, days)
        print(prediction_text)
        file.write(prediction_text)
        file.write("\n")

        # Print the confidence intervals
        for i, p, var in zip(range(n), fit, numpy.diag(covar)):
            sigma = var**0.5
            lower.append(p - sigma*tval)
            upper.append(p + sigma*tval)
            confidence = """p{0}: {1} [{2}  {3}]""".format(i, p, p - sigma*tval, p + sigma*tval)
            print(confidence)
            file.write(confidence + "\n")
        file.write("\n")

    #Plot the results
    plt.plot(x,y,'bo ')
    xfit = numpy.linspace(0, prediction, num=100)
    yfit = []
    yfit = func(xfit, fit[0], fit[1], fit[2])
    plt.plot(xfit,yfit,'b-', label='Measured')

    # Add confidence to plot
    yfit = func(xfit, *lower)
    plt.plot(xfit,yfit,'--', label='Lower 95%')
    yfit = func(xfit, *upper)
    plt.plot(xfit,yfit,'--',  label='Upper 95%')

    # Add a horizontal line
    yfit = []
    for point in xfit:
        yfit.append(60)
    plt.plot(xfit,yfit,'--', label='Acceptable')
    # Save the plot
    plt.legend(loc='best')
    plt.title('Ingress Reload Times')
    plt.xlabel('Ingress Count')
    plt.ylabel('Reload Time (s)')
    plt.ylim(ymin=0)
    plt.ylim(ymax=seconds)
    plt.xlim(xmin=0)
    plt.xlim(xmax=prediction)
    plt.savefig('{}.png'.format(analysis_file), dpi=600)
    plt.clf()

if __name__ == "__main__":
   #analyze_results('results', 3000)
   for results_file in ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'results']:
       analyze_results(results_file, 4000)
