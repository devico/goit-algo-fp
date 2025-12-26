items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: dict, budget: int):
    """
    Жадібний алгоритм:
    сортуємо страви за calories/cost (спадання) і беремо, поки вистачає бюджету.
    Повертає список назв страв.
    """
    order = sorted(
        items.keys(),
        key=lambda name: items[name]["calories"] / items[name]["cost"],
        reverse=True,
    )

    chosen = []
    total_cost = 0

    for name in order:
        cost = items[name]["cost"]
        if total_cost + cost <= budget:
            chosen.append(name)
            total_cost += cost

    return chosen


def dynamic_programming(items: dict, budget: int):
    """
    Динамічне програмування (0/1 knapsack):
    dp[b] = максимум калорій при бюджеті b
    keep[b] = список обраних страв для dp[b]
    Повертає список назв страв.
    """
    names = list(items.keys())
    dp = [0] * (budget + 1)
    keep = [[] for _ in range(budget + 1)]

    for name in names:
        cost = items[name]["cost"]
        calories = items[name]["calories"]

        for b in range(budget, cost - 1, -1):
            if dp[b - cost] + calories > dp[b]:
                dp[b] = dp[b - cost] + calories
                keep[b] = keep[b - cost] + [name]

    return keep[budget]


if __name__ == "__main__":
    budget = 100

    greedy_choice = greedy_algorithm(items, budget)
    dp_choice = dynamic_programming(items, budget)

    def total(choice):
        return (
            sum(items[n]["cost"] for n in choice),
            sum(items[n]["calories"] for n in choice),
        )

    g_cost, g_cal = total(greedy_choice)
    d_cost, d_cal = total(dp_choice)

    print("Бюджет:", budget)

    print("\nЖадібний алгоритм:")
    print("Страви:", greedy_choice)
    print("Сумарна вартість:", g_cost)
    print("Сумарні калорії:", g_cal)

    print("\nДинамічне програмування:")
    print("Страви:", dp_choice)
    print("Сумарна вартість:", d_cost)
    print("Сумарні калорії:", d_cal)
