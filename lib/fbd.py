import random
import math

# mass
alpha = 1.0
beta = 0.01
k = 0.008
# damping
eta = .99
delta_t = .001


# force directed graph drawing
def coulomb_force(xi, xj):
    dx = xj[0] - xi[0]
    dy = xj[1] - xi[1]
    ds2 = dx * dx + dy * dy
    ds = math.sqrt(ds2)
    ds3 = ds2 * ds
    if ds3 == 0.0:
        const = 0
    else:
        const = beta / (ds2 * ds)
    return [-const * dx, -const * dy]


def hooke_force(xi, xj, dij):
    dx = xj[0] - xi[0]
    dy = xj[1] - xi[1]
    ds = math.sqrt(dx * dx + dy * dy)
    dl = ds - dij
    const = k * dl / ds
    return [const * dx, const * dy]


def forcedrawing(x, v, d):
    m = len(x)
    ekint = [0.0, 0.0]

    segment = [[x[i], x[j]] for i in xrange(m) for j in xrange(m) if (d[i][j] != 0)]

    for i in xrange(m):
        Fx = 0.0 + random.random() * 0.1
        Fy = 0.0 + random.random() * 0.1
        for j in xrange(m):
            if j == 1:
                continue
            dij = d[i][j]
            FijH = [0.0, 0.0]

            FijC = coulomb_force(x[i], x[j])

            if dij != 0.0:
                FijH = hooke_force(x[i], x[j], dij)

            Fx += FijC[0] + FijH[0]
            Fy += FijC[1] + FijH[1]

        for s in segment:
            if s[0] != x[i] and s[1] != x[i]:
                FijS = coulomb_force(x[i], [(s[0][0] + s[1][0]) / 2, (s[0][1] + s[1][1]) / 2])
                Fx += FijS[0]
                Fy += FijS[1]

        v[i][0] = (v[i][0] + alpha * Fx * delta_t) * eta
        v[i][1] = (v[i][1] + alpha * Fy * delta_t) * eta
        ekint[0] = ekint[0] + alpha * (v[i][0] * v[i][0])
        ekint[1] = ekint[1] + alpha * (v[i][1] * v[i][1])

    for i in xrange(m):
        x[i][0] += v[i][0] * delta_t
        x[i][1] += v[i][1] * delta_t
    return x, v
