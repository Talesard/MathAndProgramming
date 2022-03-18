def mu(x1, x0, z1, z0):
    return abs(z1-z0)/(x1-x0)

def R(m, x1, x0, z1, z0):
    # print(m*(x1-x0), "+", ((z1-z0)**2) / (m*(x1-x0)), "-", 2*(z1+z0))
    return m*(x1-x0) + ((z1-z0)**2) / (m*(x1-x0)) - 2*(z1+z0)

def m(r, M):
    if M > 0: return r * M
    elif M == 0:
        return 1
    else:
        print("M < 0 wtf!!!!!!!!!!!!!!!!!!!!!!!")

def next_x(x1, x0, z1, z0, m):
    return (x1+x0)/2 - (z1-z0)/(2*m)

if __name__ == "__main__":
    # -----input-------
    r = 2
    a = -4
    b = 2
    def f(x):
        return x**2
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
    print("mu_1=", mu(b, a, f(b), f(a)))
    print("z_0=", f(a))
    print("z_1=", f(b))
    print("M=", mu(b, a, f(b), f(a)))
    print("m=", m(r, mu(b, a, f(b), f(a))))
    print("R(1)=", R(m(r, mu(b, a, f(b), f(a))), b, a, f(b), f(a)))
    print("R(t)=R(1)=", R(m(r, mu(b, a, f(b), f(a))), b, a, f(b), f(a)))
    print("x^3=", next_x(b, a, f(b), f(a), m(r, mu(b, a, f(b), f(a)))))
    print("z^3=", f(next_x(b, a, f(b), f(a), m(r, mu(b, a, f(b), f(a))))))

    print("\nk=4")
    L = sorted([a, b, next_x(b, a, f(b), f(a), m(r, mu(b, a, f(b), f(a))))])
    print("/\\={x_0, x_1, x_2}={", L,"}")
    print("tau=", 2)
    print("z_0=", f(L[0]))
    print("z_1=", f(L[1]))
    print("z_2=", f(L[2]))
    mu_list = [mu(L[1], L[0], f(L[1]), f(L[0])), mu(L[2], L[1], f(L[2]), f(L[1]))]
    print("mu_1=", mu_list[0])
    print("mu_2=", mu_list[1])
    M = max(mu_list)
    print("M=", M)
    m_val = m(r, M)
    print("m=", m_val)
    R1 = R(m_val, L[1], L[0], f(L[1]), f(L[0]))
    print("R(1)=", R1)
    R2 = R(m_val, L[2], L[1], f(L[2]), f(L[1]))
    print("R(2)=", R2)
    R_t = max([R1, R2])
    t = [R1, R2].index(R_t)
    print("R(t)=R(", t+1,")=", R_t)
    print("x^(i+1) \in (", L[t], L[t+1], ")")
    x_next =next_x(L[t+1], L[t], f(L[t+1]), f(L[t]), m_val)
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
    mu_list = [mu(L[1], L[0], f(L[1]), f(L[0])), mu(L[2], L[1], f(L[2]), f(L[1])), mu(L[3], L[2], f(L[3]), f(L[2]))]
    print("mu_1=", mu_list[0])
    print("mu_2=", mu_list[1])
    print("mu_3=", mu_list[2])
    M = max(mu_list)
    print("M=", M)
    m_val = m(r, M)
    print("m=", m_val)
    R1 = R(m_val, L[1], L[0], f(L[1]), f(L[0]))
    print("R(1)=", R1)
    R2 = R(m_val, L[2], L[1], f(L[2]), f(L[1]))
    print("R(2)=", R2)
    R3 = R(m_val, L[3], L[2], f(L[3]), f(L[2]))
    print("R(3)=", R3)
    R_t = max([R1, R2, R3])
    t = [R1, R2, R3].index(R_t)
    print("R(t)=R(", t+1,")=", R_t)
    print("x^(i+1) \in (", L[t], L[t+1], ")")
    x_next =next_x(L[t+1], L[t], f(L[t+1]), f(L[t]), m_val)
    print("x^5=", x_next)
    print("z^5=", f(x_next))