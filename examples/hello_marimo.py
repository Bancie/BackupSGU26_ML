"""Sample marimo notebook for this repo."""

import marimo

__generated_with = "0.23.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Marimo trong repo này

    Notebook mẫu **reactive**: kéo slider để đổi đồ thị `sin(n·x)`.
    """)
    return


@app.cell
def _(mo):
    n = mo.ui.slider(1, 10, value=3, label="n (bội số tần số)")
    return (n,)


@app.cell
def _(n):
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 200)
    y = np.sin(n.value * x)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(x, y)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    return


if __name__ == "__main__":
    app.run()
