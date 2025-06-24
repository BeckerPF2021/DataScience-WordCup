import os

def save_figure(fig, filename):
    path = os.path.join('plots', filename)
    try:
        fig.write_image(path)
    except Exception:
        pass