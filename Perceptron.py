import numpy as np

# Page 25

class Perceptron(object):

    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    def fit(self, X, y):

        # X = [n_samples, n_features]
        # y = [n_samples]

        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size = 1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, -1)

# Page 29

import pandas as pd
df = pd.read_csv('iris.data',header=None)
#print(df.head())
#print(df.tail())

# Page 30

import matplotlib.pyplot as plt

X1 = df.iloc[0:100, [0,2]].values
y1_tmp = df.iloc[0:100, 4].values
y1 = np.where(y1_tmp=='Iris-setosa',-1,1)

#print(X1[0],y1_tmp[0])
#print(X1[1],y1_tmp[1])
#print(X1[2],y1_tmp[2])
#print(X1[49],y1_tmp[49])
#print(X1[50],y1_tmp[50])
#print(X1[51],y1_tmp[51])
#print(X1[52],y1_tmp[52])

plt.figure()
plt.scatter(X1[:50,0],X1[:50,1],color='black',marker='o',label='setosa')
plt.scatter(X1[50:100,0],X1[50:100,1],color='black',marker='x',label='verisicolor')
plt.xlabel('sepal length [cm]')
plt.ylabel('petal length [cm]')
plt.savefig("page30.pdf")

# Page 31

ppn = Perceptron(eta=0.1, n_iter=10)
ppn.fit(X1,y1)

plt.figure()
plt.plot(range(1, len(ppn.errors_) + 1), ppn.errors_, color='black', marker = 'o')
plt.xlabel('Epochs')
plt.ylabel('Number of updates')
plt.savefig("page31.pdf")

# Page 32

from matplotlib.colors import ListedColormap

def plot_decision_regions(X, y, classifier, resolution=0.02):
    markers = ('s','x','o','^','v')
    colors = ('red','blue','lightgreen','gray','cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    x1_min, x1_max = X[:, 0].min() -1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() -1, X[:, 1].max() + 1

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))

    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)

    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)

    plt.xlim(xx1.min(),xx1.max())
    plt.ylim(xx2.min(),xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y==cl, 0],
                    y=X[y==cl, 1],
                    alpha=0.8,
                    c=colors[idx],
                    marker=markers[idx],
                    label=cl,
                    edgecolor='black')

plt.figure()
plot_decision_regions(X1, y1, classifier=ppn)
plt.xlabel('sepal length [cm]')
plt.ylabel('petal length [cm]')
plt.legend(loc='upper left')
plt.savefig("page33.pdf")
