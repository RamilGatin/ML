import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs

# Создание случайной выборки
X, y = make_blobs(n_samples=50, centers=2, random_state=6)

# Инициализация SVM и обучение модели
clf = svm.SVC(kernel="linear", C=1000)
clf.fit(X, y)

# Визуализация данных
plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired)

# Построение разделяющей прямой
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# Создание сетки, чтобы построить разделяющую прямую
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

# Рисуем разделяющую прямую и границы
ax.contour(
    XX, YY, Z, colors="k", levels=[-1, 0, 1], alpha=0.5, linestyles=["--", "-", "--"]
)
ax.scatter(
    clf.support_vectors_[:, 0],
    clf.support_vectors_[:, 1],
    s=100,
    linewidth=1,
    facecolors="none",
    edgecolors="k",
)


# Добавление новой точки по нажатию на среднюю кнопку мыши
def onclick(event):
    if event.button == 2:
        if event.xdata is not None and event.ydata is not None:
            x, y = event.xdata, event.ydata
            point_class = clf.predict([[x, y]])
            color = "r" if point_class == 0 else "b"
            plt.scatter(x, y, c=color, s=100, linewidth=2, edgecolors="k")
            plt.draw()


plt.gcf().canvas.mpl_connect("button_press_event", onclick)

plt.show()