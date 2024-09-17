import matplotlib
import matplotlib.pyplot as plt

# Runtime Configuration Parameters
matplotlib.rcParams["mathtext.fontset"] = "cm"  # Font changed to Computer Modern
matplotlib.rcParams["text.usetex"] = True
matplotlib.rcParams["text.latex.preamble"] = r"\usepackage{{amsmath}}\usepackage{{amssymb}}"


def latex2image(
    latex_expression,
    image_path,
    image_size_in=(3, 0.5),
    fontsize=16,
    dpi=200,
    padding=0,
    transparent=False,
):
    if image_size_in is not None:
        fig = plt.figure(figsize=image_size_in, dpi=dpi)
    else:
        fig = plt.figure(dpi=dpi)
    text = fig.text(
        x=0.5,
        y=0.5,
        s=latex_expression,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=fontsize,
    )

    plt.savefig(
        image_path,
        transparent=transparent,
        bbox_inches="tight",
        pad_inches=padding,
    )

    return fig


if __name__ == "__main__":
    latex_expression = r"""$(u, v) = \Big(\frac{f_x \cdot x}{z}, \frac{f_y \cdot y}{z}\Big)$"""
    image_name = "projection.png"
    fig = latex2image(latex_expression, image_name, image_size_in=(1, 0.5), dpi=100)
