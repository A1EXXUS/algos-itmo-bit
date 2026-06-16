import math

# Константы точности и ограничений
EPS = 1e-9       # точность вычислений (эпсилон)
MAX_ITER = 1000  # максимальное число итераций
ZERO = 1e-15     # порог для определения нулевого значения


# Кубический корень с учётом знака числа
def cbrt(x):
    return math.copysign(abs(x) ** (1 / 3), x)


# ===================== ВВОД ДАННЫХ =====================

# Ввод и проверка коэффициентов a,b,c,d,k,n,m
def input_coefficients():
    while True:
        try:
            print("Введите коэффициенты уравнения")
            print("ax^6 + bx^5 + cx^4 + dx^3 + kx^2 + mx + n = 0\n")
            a = float(input("a = "))
            b = float(input("b = "))
            c = float(input("c = "))
            d = float(input("d = "))
            k = float(input("k = "))
            m = float(input("m = "))
            n = float(input("n = "))
            return a, b, c, d, k, n, m
        except ValueError:
            print("\nОшибка ввода! a,b,c,d,k,m,n - числа?\n")


# ===================== БАЗОВЫЕ ФУНКЦИИ =====================

# Вычисление значения полинома по схеме Горнера
# Mas -- массив коэффициентов от старшей степени к младшей
def p(Mas, x):
    value = 0.0
    for coef in Mas:
        value = value * x + coef
    return value


# Одновременное вычисление значения полинома p(x) и его производной p'(x)
# Использует схему Горнера для обоих значений за один проход
def p_and_dp(Mas, x):
    N = len(Mas) - 1
    if N < 0:
        return 0.0, 0.0
    p_val = float(Mas[0])
    dp_val = 0.0
    for i in range(1, N + 1):
        dp_val = dp_val * x + p_val
        p_val = p_val * x + Mas[i]
    return p_val, dp_val


# Вычисление коэффициентов производной полинома
# Возвращает новый массив коэффициентов для p'(x)
def deriv_Mas(Mas):
    N = len(Mas) - 1
    if N <= 0:
        return [0.0]
    return [Mas[i] * (N - i) for i in range(N)]


# Вычисление второй производной полинома в точке x
def p2(Mas, x):
    return p(deriv_Mas(deriv_Mas(Mas)), x)


# ===================== gorn(...) (по схеме Горнера) =====================

# Деление полинома Mas на (x - root) по схеме Горнера
# Возвращает коэффициенты частного (полином на степень ниже)
def gorn(Mas, x):
    if len(Mas) <= 1:
        return []
    N = len(Mas)
    new_Mas = [float(Mas[0])]
    for i in range(1, N):
        new_Mas.append(new_Mas[-1] * x + Mas[i])
    return new_Mas[:-1]


# ===================== findAB(Mas) (поиск отрезка с корнем) =====================

# Оценка радиуса, в пределах которого лежат все корни полинома
# Использует формулу: R = 1 + max(|a_i| / |a_0|)
def findR(Mas):
    if len(Mas) <= 1 or abs(Mas[0]) < ZERO:
        return 10.0
    lead = abs(Mas[0])
    max_ratio = max(abs(coef) / lead for coef in Mas[1:]) if len(Mas) > 1 else 0.0
    return min(1.0 + max_ratio, 1e4)


# Поиск отрезка [A, B], на котором функция меняет знак (есть корень)
# Сканирует от -R до R с уменьшающимся шагом
def findAB(Mas):
    A, B = 0.0, 0.0
    h = 0.1
    R = findR(Mas)
    total = 0

    while h > 1e-7:
        i = -R
        while i < (R - h):
            # Проверяем смену знака: f(i) * f(i+h) <= 0
            if p(Mas, i) * p(Mas, i + h) <= 0:
                A, B = i, i + h
                return A, B
            i += h
            total += 1
            if total > 200000:
                return None
        h /= 10.0  # уменьшаем шаг для более точного поиска
    return None


# ===================== cas(...) (метод касательных / Ньютона) =====================

# Метод касательных (Ньютона): x_{n+1} = x_n - f(x_n)/f'(x_n)
# Выбор начального приближения по условию сходимости: f(x)*f''(x) > 0
def cas_method(Mas, eps=EPS):
    X = []
    O = findAB(Mas)
    if O is None:
        print("    не удалось найти корень")
        return None

    A, B = O

    # Выбираем начальную точку по условию: f(x0)*f''(x0) > 0
    if p(Mas, A) * p2(Mas, A) > 0:
        X.append(A)
    elif p(Mas, B) * p2(Mas, B) > 0:
        X.append(B)
    else:
        X.append((A + B) / 2)

    i = 0
    while i < MAX_ITER:
        f_val, df_val = p_and_dp(Mas, X[i])
        if abs(df_val) < ZERO:
            print("    Производная равна 0")
            return None

        # Формула Ньютона: x_{n+1} = x_n - f(x_n) / f'(x_n)
        X.append(X[i] - f_val / df_val)

        # Проверка сходимости
        if abs(X[i + 1] - X[i]) < eps:
            return X[i + 1]

        i += 1

    print("    Превышено число итераций")
    return None


def cas(a, b, c, d, k, m, n, eps=EPS):
    Mas = [a, b, c, d, k, m, n]
    return cas_method(Mas, eps)


# ===================== hord(...) (метод хорд) =====================

# Метод хорд (секущих с фиксированной точкой)
# Один конец отрезка фиксирован, другой движется к корню
def hord_method(Mas, eps=EPS):
    X = []
    O = findAB(Mas)
    if O is None:
        print("    не удалось найти корень")
        return None

    A, B = O
    x_fix = B       # фиксированная точка
    x_move = A      # подвижная точка

    f_fix = p(Mas, x_fix)
    f_move = p(Mas, x_move)

    n = 0
    while n < MAX_ITER:
        if abs(f_move) < eps:
            X.append(x_move)
            return x_move
        if abs(f_fix) < eps:
            x_move = x_fix
            X.append(x_move)
            return x_move

        denom = f_fix - f_move
        if abs(denom) < ZERO:
            print("    Деление на 0!")
            return None

        # Формула хорд: пересечение хорды с осью OX
        x_new = x_move - f_move * (x_fix - x_move) / denom
        f_new = p(Mas, x_new)

        # Проверка сходимости
        if abs(x_new - x_move) < eps:
            X.append(x_new)
            return x_new

        x_move = x_new
        f_move = f_new
        n += 1

    print("    Превышено число итераций")
    return None


def hord(b, c, d, k, m, n, eps=EPS):
    Mas = [b, c, d, k, m, n]
    return hord_method(Mas, eps)


# ===================== khord(...) (комбинированный метод хорд и касательных) =====================

# Комбинированный метод: одновременно применяются метод Ньютона и метод хорд
# Ньютон сужает отрезок с одной стороны, хорды -- с другой
def khord_method(Mas, eps=EPS):
    X = []
    O = findAB(Mas)
    if O is None:
        print("    не удалось найти корень")
        return None

    A, B = O

    # Выбор: метод Ньютона применяется к точке, где f(x)*f''(x) > 0
    if p(Mas, A) * p2(Mas, A) > 0:
        x_start = A      # точка для метода Ньютона
        x_move = B       # точка для метода хорд
    elif p(Mas, B) * p2(Mas, B) > 0:
        x_start = B
        x_move = A
    else:
        x_start = (A + B) / 2
        x_move = A

    f_start = p(Mas, x_start)
    f_move = p(Mas, x_move)
    n = 0

    while n < MAX_ITER:
        # Шаг метода Ньютона (касательных)
        _, dp_start = p_and_dp(Mas, x_start)
        if abs(dp_start) < ZERO:
            print("    Деление на 0!")
            return None

        x_start_new = x_start - f_start / dp_start
        f_start_new = p(Mas, x_start_new)

        # Шаг метода хорд
        denom = f_start_new - f_move
        if abs(denom) < ZERO:
            # оба значения функции неразличимы -- уже у корня
            return x_start_new if abs(f_start_new) <= abs(f_move) else x_move

        x_move_new = x_move - f_move * (x_start_new - x_move) / denom
        f_move_new = p(Mas, x_move_new)

        # Корень -- среднее между приближениями с двух сторон
        X.append((x_start_new + x_move_new) / 2)

        # Проверка сходимости
        if abs(x_start_new - x_move_new) < eps:
            return X[n]

        x_start = x_start_new
        x_move = x_move_new
        f_start = f_start_new
        f_move = f_move_new

        n += 1

    print("    Превышено число итераций")
    return None


def khord(c, d, k, m, n, eps=EPS):
    Mas = [c, d, k, m, n]
    return khord_method(Mas, eps)


# ===================== Решение: метод -> gorn -> метод, соответствующий степени =====================

# Ищет корень чётной кратности: корень f'(x), являющийся и корнем f(x)
# Используется когда основной метод не смог найти корень (нет смены знака)
def _find_even_root(Mas, eps=EPS):
    dMas = deriv_Mas(Mas)
    if len(dMas) <= 1:
        return None
    # Ищем корни производной -- кратные корни полинома являются корнями производной
    d_degree = len(dMas) - 1
    if d_degree == 1:
        cands = [-dMas[1] / dMas[0]]
    elif d_degree == 2:
        cands = viet(dMas[0], dMas[1], dMas[2])
    elif d_degree == 3:
        cands = kardan(dMas[0], dMas[1], dMas[2], dMas[3])
    else:
        # Для высоких степеней -- метод Ньютона для производной
        r = findAB(dMas)
        if r is None:
            return None
        A, B = r
        x0 = (A + B) / 2
        for _ in range(MAX_ITER):
            fv, dfv = p_and_dp(dMas, x0)
            if abs(dfv) < ZERO:
                break
            x1 = x0 - fv / dfv
            if abs(x1 - x0) < eps:
                x0 = x1
                break
            x0 = x1
        cands = [x0]
    # Проверяем, является ли корень производной также корнем исходного полинома
    for c in cands:
        if abs(p(Mas, c)) < 1e-6:
            return c
    return None


# Выбор численного метода в зависимости от степени полинома:
# степень >= 6 -- комбинированный, 5 -- хорд, 4 -- касательных
def _method_for_degree(degree):
    if degree >= 6:
        return khord_method, "комбинированный"
    if degree == 5:
        return hord_method, "хорд"
    return cas_method, "касательных"   # degree == 4


# Последовательное нахождение всех корней полинома
# Находит один корень, делит полином на (x - корень) по Горнеру,
# и повторяет для полинома меньшей степени
def solve_numerical(Mas):
    roots = []
    Mas = [float(coef) for coef in Mas]
    step = 1

    while len(Mas) > 1:
        # Убираем ведущие нули (понижаем фактическую степень)
        while len(Mas) > 1 and abs(Mas[0]) < ZERO:
            Mas = Mas[1:]
        if len(Mas) <= 1:
            break

        # Извлекаем корни x=0 (если свободный член равен нулю)
        while len(Mas) > 1 and abs(Mas[-1]) < ZERO:
            roots.append(0.0)
            print(f"  Шаг {step}: x = 0 (свободный член = 0)")
            Mas = Mas[:-1]
            step += 1
        if len(Mas) <= 1:
            break

        degree = len(Mas) - 1

        # Степень 1: линейное уравнение ax + b = 0
        if degree == 1:
            x = -Mas[1] / Mas[0]
            roots.append(x)
            print(f"  Шаг {step}: линейное уравнение, x = {x:.10f}")
            break

        # Степень 2: квадратное уравнение (теорема Виета)
        if degree == 2:
            new_roots = viet(Mas[0], Mas[1], Mas[2])
            roots.extend(new_roots)
            if new_roots:
                print(f"  Шаг {step}: viet, x = {[round(r, 10) for r in new_roots]}")
            else:
                print(f"  Шаг {step}: viet, действительных корней нет")
            break

        # Степень 3: кубическое уравнение (формула Кардано)
        if degree == 3:
            new_roots = kardan(Mas[0], Mas[1], Mas[2], Mas[3])
            roots.extend(new_roots)
            print(f"  Шаг {step}: kardan, x = {[round(r, 10) for r in new_roots]}")
            break

        # Степень >= 4: численный метод + деление по Горнеру для понижения степени
        method_func, method_name = _method_for_degree(degree)
        x = method_func(Mas)
        if x is None:
            # Если метод не нашёл корень -- пробуем найти корень чётной кратности
            x = _find_even_root(Mas)
            if x is None:
                print(f"  Шаг {step}: не удалось найти корень методом {method_name}")
                break
            method_name += " (чётная кратность)"

        roots.append(x)
        print(f"  Шаг {step}: метод {method_name}, x = {x:.10f}")
        Mas = gorn(Mas, x)  # делим полином на (x - корень), понижая степень
        step += 1

    return roots


# ===================== kardan(d, k, m, n) -- формула Кардано =====================

# Решение кубического уравнения dx^3 + kx^2 + mx + n = 0
# по формуле Кардано. Возвращает список действительных корней
def kardan(d, k, m, n):
    a = d
    b = k
    c = m
    free = n

    # Приведение к виду t^3 + pt + q = 0 (подстановка x = t - b/(3a))
    p_val = (3 * a * c - b * b) / (3 * a * a)
    q = (2 * b ** 3 - 9 * a * b * c + 27 * a * a * free) / (27 * a ** 3)
    Delta = (q / 2) ** 2 + (p_val / 3) ** 3  # дискриминант

    if Delta > EPS:
        # Один действительный корень (Delta > 0)
        u = cbrt(-q / 2 + math.sqrt(Delta))
        v = cbrt(-q / 2 - math.sqrt(Delta))
        x = u + v - b / (3 * a)
        return [x]

    if abs(Delta) <= EPS:
        # Кратные корни (Delta = 0)
        if abs(q) <= EPS:
            x = -b / (3 * a)
            return [x]
        u = cbrt(-q / 2)
        x1 = 2 * u - b / (3 * a)
        x2 = -u - b / (3 * a)
        return [x1, x2]

    # Три различных действительных корня (Delta < 0) -- тригонометрическая формула
    phi = math.acos(-q / (2 * math.sqrt(-(p_val / 3) ** 3)))
    r = 2 * math.sqrt(-p_val / 3)
    x1 = r * math.cos(phi / 3) - b / (3 * a)
    x2 = r * math.cos((phi + 2 * math.pi) / 3) - b / (3 * a)
    x3 = r * math.cos((phi + 4 * math.pi) / 3) - b / (3 * a)
    return [x1, x2, x3]


# ===================== viet(k, m, n) -- квадратное уравнение =====================

# Решение квадратного уравнения kx^2 + mx + n = 0 через дискриминант
def viet(k, m, n):
    a = k
    b = m
    c = n
    D = b * b - 4 * a * c  # дискриминант

    if D < -EPS:
        return []            # нет действительных корней
    if abs(D) <= EPS:
        x = -b / (2 * a)
        return [x]           # один корень (кратный)
    sqrt_D = math.sqrt(D)
    x1 = (-b + sqrt_D) / (2 * a)
    x2 = (-b - sqrt_D) / (2 * a)
    return [x1, x2]          # два различных корня


# Удаление дублирующихся корней (с допуском tol)
def deduplicate_roots(roots, tol=1e-6):
    unique = []
    for r in roots:
        if not any(abs(r - u) < tol for u in unique):
            unique.append(r)
    return unique


# ===================== ГЛАВНАЯ ФУНКЦИЯ =====================

def main():
    a, b, c, d, k, n, m = input_coefficients()
    print(f"\nУравнение: {a}x^6 + {b}x^5 + {c}x^4 + {d}x^3 + {k}x^2 + {m}x + {n} = 0")
    print("=" * 60)

    roots = None

    # Определяем степень уравнения по первому ненулевому коэффициенту
    # и выбираем соответствующий метод решения
    if a != 0:
        print("\n>>> khord(a, b, c, d, k, m, n)")
        Mas = [a, b, c, d, k, m, n]
        roots = solve_numerical(Mas)

    elif b != 0:
        print("\n>>> hord(b, c, d, k, m, n)")
        Mas = [b, c, d, k, m, n]
        roots = solve_numerical(Mas)

    elif c != 0:
        print("\n>>> cas(c, d, k, m, n)")
        Mas = [c, d, k, m, n]
        roots = solve_numerical(Mas)

    elif d != 0:
        print("\n>>> kardan(d, k, m, n)")
        roots = kardan(d, k, m, n)

    elif k != 0:
        print("\n>>> viet(k, m, n)")
        roots = viet(k, m, n)

    elif m != 0:
        # Линейное уравнение mx + n = 0
        x = -(n / m)
        roots = [x]

    elif n != 0:
        # 0 = n, где n != 0 -- решений нет
        roots = []

    else:
        # Все коэффициенты нули -- любое x является решением
        roots = None

    if roots is not None:
        roots = deduplicate_roots(roots)

    print("\n" + "=" * 60)
    if roots is None:
        print("Результат: корнем является любое число")
        return

    if len(roots) == 0:
        print("Результат: Решений нет")
        return

    # Вывод найденных корней с проверкой подстановкой
    print("вывод корней:")
    for i, x in enumerate(roots, 1):
        f_x = a * x ** 6 + b * x ** 5 + c * x ** 4 + d * x ** 3 + k * x ** 2 + m * x + n
        print(f"  x{i} = {x:.10f}; проверка f(x{i}) = {f_x:.2e}")


if __name__ == "__main__":
    main()
