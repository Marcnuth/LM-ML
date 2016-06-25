import matplotlib.pyplot as plt


def show(imgs, row, col):

    fig, axes = plt.subplots(nrows=row, ncols=col, figsize=(70, 10), sharex=True, sharey=True)
    ax = axes.ravel()

    for i in range(row * col):
        ax[i].imshow(imgs[i], cmap=plt.cm.gray)
        ax[i].axis('off')
        
    fig.tight_layout()
    plt.show()





