def sec_to_HMS(value, show_ms=False):
    # Convert numerical seconds to string HH:MM:SS / HH:MM:SS.ms

    value = max(0, value)
    h = value / 3600
    m = 60 * (h - int(h))
    s = 60 * (m - int(m))
    ms = s - int(s)

    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}" + (
        f"{ms:.3f}"[1:] if show_ms else ""
    )


def progress_bar(
    i, imin=0, imax=1, barsize=100, grid=10, label=False, to_string=False, oneline=False
):
    # Print a simple horizontal bar graph of length "barsize" characters
    # "i" is the current value of the graph
    # "grid" defines the spacing of dots
    # "label" is an optional progress label on the end of the bar graph

    ratio = (i - imin) / (imax - imin)
    i = max(0, min(barsize, int(barsize * ratio)))
    text = "▒" * i
    iter = " " * (grid - 1) + "."

    if i < barsize:
        # There will be some portion of a grid pattern to display
        text += iter[i % grid :]

    while len(text) < barsize:
        # Continue tiling the grid until the bar is full
        text += iter

    # Display the bar graph and an optional progress % label
    if to_string:
        return f"|{text}|" + (f"[{int(100*ratio):3d}%]" if label else "")
    else:
        if oneline:
            print(
                "|" + text + "|",
                f"[{int(100*ratio):3d}%]" if label else "",
                end="\r",
                flush=True,
            )
        else:
            print("|" + text + "|", f"[{int(100*ratio):3d}%]" if label else "")


def to_set_len_str(val, pref_len=3, suff_len=1):
    # Formats a float as a string with:
    # At least "pref_len" leading digits
    # Exactly "suff_len" decimal places (rounding)

    suff_len = max(suff_len, 0)
    pref_len = max(pref_len, 0)
    return f"{val:.{suff_len}f}".rjust(pref_len + (suff_len > 0) + suff_len)
