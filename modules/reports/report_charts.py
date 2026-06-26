import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def bar_chart(frame, title, labels, values):
    fig, ax = plt.subplots()

    ax.bar(labels, values)
    ax.set_title(title)
    ax.tick_params(axis='x', rotation=45)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def line_chart(frame, title, labels, values):
    fig, ax = plt.subplots()

    ax.plot(labels, values, marker="o")
    ax.set_title(title)
    ax.tick_params(axis='x', rotation=45)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand="True")