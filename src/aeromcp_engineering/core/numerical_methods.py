"""Reusable numerical methods for AeroMCP engineering calculations.

Provides root-finding (bisection, safeguarded Newton-Raphson, secant),
explicit 4th-order Runge-Kutta (RK4) ODE integration, and small-matrix
linear algebra utilities without external dependencies.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence

from aeromcp_engineering.core.errors import ConvergenceError


@dataclass(frozen=True)
class RootResult:
    """Result of an iterative root-finding solver."""

    root: float
    converged: bool
    iterations: int
    residual: float
    tolerance: float
    reason: str = "converged"


def bisection(
    func: Callable[[float], float],
    a: float,
    b: float,
    *,
    tol: float = 1e-12,
    max_iter: int = 200,
) -> RootResult:
    """Find a root of *func* on [a, b] using bisection."""
    if a >= b:
        raise ValueError(f"Bracket [a, b] must satisfy a < b. Got [{a}, {b}].")
    fa = func(a)
    fb = func(b)
    if math.isnan(fa) or math.isnan(fb):
        raise ValueError("Function evaluated to NaN at bracket endpoints.")
    if abs(fa) <= tol:
        return RootResult(a, True, 0, fa, tol)
    if abs(fb) <= tol:
        return RootResult(b, True, 0, fb, tol)
    if fa * fb > 0.0:
        raise ValueError(f"Root is not bracketed on [{a}, {b}]: f(a)={fa}, f(b)={fb}.")

    lo, hi = a, b
    flo = fa
    for iteration in range(1, max_iter + 1):
        mid = 0.5 * (lo + hi)
        fmid = func(mid)
        if math.isnan(fmid) or math.isinf(fmid):
            raise ConvergenceError(f"Function returned non-finite value at x={mid}.")
        if abs(fmid) <= tol or 0.5 * (hi - lo) <= tol:
            return RootResult(mid, True, iteration, fmid, tol)
        if flo * fmid < 0.0:
            hi = mid
        else:
            lo = mid
            flo = fmid

    mid = 0.5 * (lo + hi)
    raise ConvergenceError(
        f"Bisection did not converge within {max_iter} iterations (residual={func(mid)})."
    )


def safeguarded_newton(
    func: Callable[[float], float],
    dfunc: Callable[[float], float],
    a: float,
    b: float,
    x0: float | None = None,
    *,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> RootResult:
    """Find a root of *func* on [a, b] using Newton-Raphson safeguarded by bisection."""
    if a >= b:
        raise ValueError(f"Bracket [a, b] must satisfy a < b. Got [{a}, {b}].")
    fa = func(a)
    fb = func(b)
    if abs(fa) <= tol:
        return RootResult(a, True, 0, fa, tol)
    if abs(fb) <= tol:
        return RootResult(b, True, 0, fb, tol)
    if fa * fb > 0.0:
        raise ValueError(f"Root is not bracketed on [{a}, {b}]: f(a)={fa}, f(b)={fb}.")

    lo, hi = a, b
    flo = fa
    x = 0.5 * (lo + hi) if x0 is None else x0
    if not (lo <= x <= hi):
        x = 0.5 * (lo + hi)

    for iteration in range(1, max_iter + 1):
        fx = func(x)
        if math.isnan(fx) or math.isinf(fx):
            raise ConvergenceError(f"Function returned non-finite value at x={x}.")
        if abs(fx) <= tol or 0.5 * (hi - lo) <= tol:
            return RootResult(x, True, iteration, fx, tol)

        if flo * fx < 0.0:
            hi = x
        else:
            lo = x
            flo = fx

        dfx = dfunc(x)
        if dfx != 0.0 and math.isfinite(dfx):
            x_new = x - fx / dfx
            if lo < x_new < hi:
                x = x_new
                continue
        x = 0.5 * (lo + hi)

    raise ConvergenceError(
        f"Safeguarded Newton did not converge within {max_iter} iterations."
    )


def rk4_step(
    derivs: Callable[[float, list[float]], list[float]],
    t: float,
    y: Sequence[float],
    dt: float,
) -> list[float]:
    """Perform a single 4th-order Runge-Kutta step."""
    n = len(y)
    k1 = derivs(t, list(y))
    y2 = [y[i] + 0.5 * dt * k1[i] for i in range(n)]
    k2 = derivs(t + 0.5 * dt, y2)
    y3 = [y[i] + 0.5 * dt * k2[i] for i in range(n)]
    k3 = derivs(t + 0.5 * dt, y3)
    y4 = [y[i] + dt * k3[i] for i in range(n)]
    k4 = derivs(t + dt, y4)
    return [
        y[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i])
        for i in range(n)
    ]


def rk4_integrate(
    derivs: Callable[[float, list[float]], list[float]],
    t0: float,
    y0: Sequence[float],
    t_end: float,
    dt: float,
) -> tuple[list[float], list[list[float]]]:
    """Integrate an ODE system from t0 to t_end using fixed-step RK4."""
    if dt <= 0.0:
        raise ValueError(f"Time step dt must be positive. Got {dt}.")
    if t_end < t0:
        raise ValueError(f"t_end ({t_end}) must be >= t0 ({t0}).")
    t = float(t0)
    y = [float(v) for v in y0]
    times = [t]
    states = [list(y)]
    while t < t_end - 1e-12:
        step = min(dt, t_end - t)
        y = rk4_step(derivs, t, y, step)
        if any(not math.isfinite(v) for v in y):
            raise ConvergenceError("RK4 integration produced non-finite state.")
        t += step
        times.append(t)
        states.append(list(y))
    return times, states


def solve_linear_system(a: list[list[float]], b: list[float]) -> list[float]:
    """Solve Ax = b for small dense systems using Gaussian elimination with partial pivoting."""
    n = len(b)
    if len(a) != n or any(len(row) != n for row in a):
        raise ValueError("Matrix A must be square and match length of b.")
    aug = [list(map(float, a[i])) + [float(b[i])] for i in range(n)]

    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot_row][col]) < 1e-15:
            raise ValueError("Linear system is singular or nearly singular.")
        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
        pivot = aug[col][col]
        for row in range(col + 1, n):
            factor = aug[row][col] / pivot
            for k in range(col, n + 1):
                aug[row][k] -= factor * aug[col][k]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = aug[i][n] - sum(aug[i][j] * x[j] for j in range(i + 1, n))
        x[i] = s / aug[i][i]
    return x
