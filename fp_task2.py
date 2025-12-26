import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def rotate(vx: float, vy: float, angle_rad: float) -> tuple[float, float]:
    ca = math.cos(angle_rad)
    sa = math.sin(angle_rad)
    return vx * ca - vy * sa, vx * sa + vy * ca


def draw_square(ax, p0, u):
    x0, y0 = p0
    ux, uy = u
    vx, vy = -uy, ux

    p1 = (x0 + ux, y0 + uy)
    p2 = (p1[0] + vx, p1[1] + vy)
    p3 = (x0 + vx, y0 + vy)

    poly = Polygon([p0, p1, p2, p3], closed=True, fill=False, edgecolor="brown", linewidth=1)
    ax.add_patch(poly)

    return p0, p1, p2, p3


def pythagoras_tree(ax, p0, size, angle_rad, depth, phi_deg=45):
    """
    Рекурсивно будує дерево Піфагора.

    p0: нижня ліва точка базового квадрата
    size: довжина сторони квадрата
    angle_rad: кут напрямку нижнього ребра (в радіанах)
    depth: рівень рекурсії
    phi_deg: кут розгалуження (звичайно 45°)
    """
    if depth < 0 or size <= 0:
        return

    ux = size * math.cos(angle_rad)
    uy = size * math.sin(angle_rad)

    _, _, p2, p3 = draw_square(ax, p0, (ux, uy))

    if depth == 0:
        return

    tx, ty = ux, uy
    tlen = size
    t_unit = (tx / tlen, ty / tlen)

    phi = math.radians(phi_deg)

    rx, ry = rotate(t_unit[0], t_unit[1], phi)
    left_len = size * math.cos(phi)
    p4 = (p3[0] + rx * left_len, p3[1] + ry * left_len)

    u_left = (p4[0] - p3[0], p4[1] - p3[1])
    u_right = (p2[0] - p4[0], p2[1] - p4[1])

    pythagoras_tree(ax, p3, math.hypot(*u_left), math.atan2(u_left[1], u_left[0]), depth - 1, phi_deg)
    pythagoras_tree(ax, p4, math.hypot(*u_right), math.atan2(u_right[1], u_right[0]), depth - 1, phi_deg)


def main():
    try:
        depth = int(input("Введіть рівень рекурсії (наприклад, 8): ").strip())
    except Exception:
        print("Некоректне значення. Встановлено depth = 8.")
        depth = 8

    ax = plt.subplots(figsize=(8, 8))[1]
    ax.set_aspect("equal")
    ax.axis("off")

    # Стартовий квадрат
    start_size = 1.0
    start_p0 = (-0.5, 0.0)  # щоб дерево було ближче до центру
    start_angle = 0.0      # горизонтально

    pythagoras_tree(ax, start_p0, start_size, start_angle, depth, phi_deg=45)

    ax.relim()
    ax.autoscale_view()
    plt.show()


if __name__ == "__main__":
    main()
