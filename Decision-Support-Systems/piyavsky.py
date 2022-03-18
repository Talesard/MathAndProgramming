def f(x):
    return x

def R(x1, x0, z1, z0, m):
    return 0.5*m*(x1-x0)-(z1+z0)/2

def next_x(x1, x0, z1, z0, m):
    return (x1+x0)/2 - (z1-z0)/(2*m)

if __name__ == "__main__":
    # -----input-------
    m = 2
    a = 0
    b = 4
    def f(x):
        return x
    # -----------------


    print("\nk=1")
    print("x^1=", a)
    print("z^1=", f(a))

    print("\nk=2")
    print("x^2=", b)
    print("z^2=", f(b))

    print("\nk=3")
    print("/\\={x_0, x_1}={", a, b, "}")
    print("tau=", 1)
    print("z_0=", f(a))
    print("z_1=", f(b))
    print("R(1)=", R(b, a, f(b), f(a), m))
    print("R(t)=R(1)=", R(b, a, f(b), f(a), m))
    print("x^3=", next_x(b, a, f(b), f(a), m))
    print("z^3=", f(next_x(b, a, f(b), f(a), m)))

    print("\nk=4")
    L = sorted([a, b, next_x(b, a, f(b), f(a), m)])
    print("/\\={x_0, x_1, x_2}={", L,"}")
    print("tau=", 2)
    print("z_0=", f(L[0]))
    print("z_1=", f(L[1]))
    print("z_2=", f(L[2]))
    R1 = R(L[1], L[0], f(L[1]), f(L[0]), m)
    print("R(1)=", R1)
    R2 = R(L[2], L[1], f(L[2]), f(L[1]), m)
    print("R(2)=", R2)
    R_t = max([R1, R2])
    t = [R1, R2].index(R_t)
    print("R(t)=R(", t+1,")=", R_t)
    print("x^(i+1) \in (", L[t], L[t+1], ")")
    x_next =next_x(L[t+1], L[t], f(L[t+1]), f(L[t]), m)
    print("x^4=", x_next)
    print("z^4=", f(x_next))

    print("\nk=5")
    L.append(x_next)
    L.sort()
    print("/\\={x_0, x_1, x_2, x_3}={", L,"}")
    print("tau=", 3)
    print("z_0=", f(L[0]))
    print("z_1=", f(L[1]))
    print("z_2=", f(L[2]))
    print("z_3=", f(L[3]))
    R1 = R(L[1], L[0], f(L[1]), f(L[0]), m)
    print("R(1)=", R1)
    R2 = R(L[2], L[1], f(L[2]), f(L[1]), m)
    print("R(2)=", R2)
    R3 = R(L[3], L[2], f(L[3]), f(L[2]), m)
    print("R(3)=", R3)
    R_t = max([R1, R2, R3])
    t = [R1, R2, R3].index(R_t)
    print("R(t)=R(", t+1,")=", R_t)
    print("x^(i+1) \in (", L[t], L[t+1], ")")
    x_next =next_x(L[t+1], L[t], f(L[t+1]), f(L[t]), m)
    print("x^5=", x_next)
    print("z^5=", f(x_next))