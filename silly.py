from pprint import pp

def next_term(p, q):
    """
    for a = sqrt(991), (p + a)/q = m + q2/(p2+a)
    """
    c = (p + 31)//q
    p2 = c * q - p
    return c, p2, (991 - p2*p2) // q

c, p, q = (0, 0, 1)
coeffs = []

while c != 62:
    c, p, q = next_term(p, q)
    coeffs.append(c)

m, n = (0, 1)
for c in coeffs[::-1]:
    m, n = (m*c + n, m)

pp(coeffs, compact=True)
print('m^2 - 991n^2 =', m**2 - 991 * n**2)
print(f'm = {m:,d}')
print(f'n = {n:,d}')