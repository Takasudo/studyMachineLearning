from sklearn import datasets
import numpy as np
iris = datasets.load_iris()
X = iris.data[:, [2,3]]
y = iris.target
print('Class labels : ', np.unique(y))

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)
print('Labels count in y : ',np.bincount(y))
print('Labels count in y_train : ',np.bincount(y_train))
print('Labels count in y_test : ',np.bincount(y_test))

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train) # calculate mean and deviation for X_train
X_train_std = sc.transform(X_train) 
X_test_std = sc.transform(X_test)

from sklearn.linear_model import Perceptron
ppn = Perceptron(max_iter=40, eta0=0.1, random_state=1)
ppn.fit(X_train_std, y_train)

y_pred = ppn.predict(X_test_std)
print('Misclassified samples : %d' % (y_test != y_pred).sum())

from sklearn.metrics import accuracy_score
print('Accuracy %.2f' % accuracy_score(y_test, y_pred))

print('Accuracy %.2f' % ppn.score(X_test_std, y_test))

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

def plot_decision_regions(X, y, classifier, test_idx = None, resolution=0.02):
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

    if test_idx:
        X_test, y_test = X[test_idx, :], y[test_idx]
        plt.scatter(X_test[:,0], X_test[:,1],
                    c='',
                    edgecolor = 'black',
                    alpha=1.0,
                    linewidth=1,
                    marker='o',
                    s=100,
                    label='test set')

X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined = np.hstack((y_train, y_test))
plot_decision_regions(X=X_combined_std, y=y_combined, classifier=ppn, test_idx=range(105,150))
plt.xlabel("petal length (standardized)")
plt.ylabel("petal width (standardized)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig("page58.pdf")

# Page 70

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(C=100.0, random_state=1, solver='lbfgs', multi_class='auto')
lr.fit(X_train_std, y_train)
plt.figure()
plot_decision_regions(X=X_combined_std, y=y_combined, classifier=lr, test_idx=range(105,150))
plt.xlabel("petal length (standardized)")
plt.ylabel("petal width (standardized)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig("page70.pdf")

# Page 71

N_tmp = 3 
prob = lr.predict_proba(X_test_std[:N_tmp,:])
predclass1 = prob.argmax(axis=1)
predclass2 = lr.predict(X_test_std[:N_tmp,:])
print(prob)
print(predclass1)
print(predclass2)

# Page 79

from sklearn.svm import SVC
svm = SVC(kernel = 'linear', C=1.0, random_state=1)
svm.fit(X_train_std, y_train)
plt.figure()
plot_decision_regions(X=X_combined_std, y=y_combined, classifier=svm, test_idx=range(105,150))
plt.xlabel("petal length (standardized)")
plt.ylabel("petal width (standardized)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig("page80.pdf")

# Page 94

from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(criterion='gini',max_depth=4,random_state=1)
tree.fit(X_train, y_train)
X_combined = np.vstack((X_train,X_test))
plt.figure()
plot_decision_regions(X=X_combined, y=y_combined, classifier=tree, test_idx=range(105,150))
plt.xlabel("petal length (cm)")
plt.ylabel("petal width (cm)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig("page95.pdf")

# Page 96

from pydotplus import graph_from_dot_data
from sklearn.tree import export_graphviz

dot_data = export_graphviz(tree,
                           filled=True,
                           rounded=True,
                           class_names=['Setosa','Versicolor','Virginica'],
                           feature_names=['patal length','patal width'],
                           out_file=None)

graph = graph_from_dot_data(dot_data)
graph.write_png('page96.png')

# Page 99

from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(criterion='gini',
                                n_estimators=25,
                                random_state=1)
forest.fit(X_train, y_train)
plt.figure()
plot_decision_regions(X=X_combined, y=y_combined, classifier=forest, test_idx=range(105,150))
plt.xlabel("petal length (cm)")
plt.ylabel("petal width (cm)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig("page99.pdf")

# page 101

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5,
                            p=2,
                            metric='minkowski')

knn.fit(X_train_std, y_train)
plt.figure()
plot_decision_regions(X=X_combined_std, y=y_combined, classifier=knn, test_idx=range(105,150))
plt.xlabel("petal length (std)")
plt.ylabel("petal width (std)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig("page102.pdf")