import numpy as np


ANALYTIC_COUNTS = {
    2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6,
    8: 5, 9: 4, 10: 3, 11: 2, 12: 1
}


def simulate_two_dice(n: int = 200_000, seed: int = 42):
    """
    Імітація кидків двох кубиків.
    Повертає counts[сума] та probs[сума] для сум 2..12.
    """
    rng = np.random.default_rng(seed)

    # Кидаємо два кубики n разів (значення 1..6)
    rolls = rng.integers(1, 7, size=(n, 2))
    sums = rolls[:, 0] + rolls[:, 1]

    counts = np.bincount(sums, minlength=13)
    probs = counts / n

    return counts, probs


def analytic_probs():
    """Аналітичні ймовірності для двох кубиків"""
    probs = np.zeros(13, dtype=float)
    for s, c in ANALYTIC_COUNTS.items():
        probs[s] = c / 36.0
    return probs


def print_table(counts, probs_mc, probs_an, n: int):
    print(f"Кількість симуляцій (n): {n}\n")

    print(f"{'Сума':>4} | {'К-ть':>8} | {'MC ймовірн.':>11} | {'Аналіт.':>8} | {'|Δ|':>10}")
    print("-" * 55)

    max_diff = 0.0
    for s in range(2, 13):
        diff = abs(probs_mc[s] - probs_an[s])
        max_diff = max(max_diff, diff)
        print(f"{s:>4} | {counts[s]:>8} | {probs_mc[s]:>11.6f} | {probs_an[s]:>8.6f} | {diff:>10.6f}")

    print("\nМаксимальна абсолютна різниця |Δ|:", f"{max_diff:.6f}")


def plot_probs(probs_mc, probs_an):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("\nmatplotlib не знайдено — графік не буде побудований.")
        return

    x = np.arange(2, 13)
    y_mc = probs_mc[2:13]
    y_an = probs_an[2:13]

    plt.figure(figsize=(9, 5))
    plt.plot(x, y_an, marker="o", label="Аналітичні")
    plt.bar(x, y_mc, alpha=0.6, label="Монте-Карло")

    plt.title("Ймовірності сум при киданні двох кубиків")
    plt.xlabel("Сума (2..12)")
    plt.ylabel("Ймовірність")
    plt.xticks(x)
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    n = 1_000_000
    seed = 42

    counts, probs_mc = simulate_two_dice(n=n, seed=seed)
    probs_an = analytic_probs()

    print_table(counts, probs_mc, probs_an, n=n)
    plot_probs(probs_mc, probs_an)
