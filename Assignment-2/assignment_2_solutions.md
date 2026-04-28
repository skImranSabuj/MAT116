# Assignment-2 Solutions (MAT 116)

> Spring 2026, DMP NSU  
> Lecturer-style model solutions with full steps and side notes

---

## 1(a) Graph by transformations

Given:

$$
f(x)=2(x-2)^4+1
$$

Start from the parent function:

$$
y=x^4
$$

### Step-by-step transformations

1. Replace $x$ by $(x-2)$: shift right by $2$ units.
2. Multiply by $2$: vertical stretch by factor $2$.
3. Add $1$: shift up by $1$ unit.

So the graph is an upward-opening quartic with vertex at:

$$
(2,1)
$$

Axis of symmetry:

$$
x=2
$$

Domain:

$$
(-\infty,\infty)
$$

Range:

$$
[1,\infty)
$$

Useful points (from transformed parent points):

- $x=1$: $f(1)=2(1-2)^4+1=3$
- $x=3$: $f(3)=3$
- $x=0$: $f(0)=2(16)+1=33$
- $x=4$: $f(4)=33$

**Side note:** Because the power is even ($4$), both ends rise to $+\infty$, and the graph is symmetric about $x=2$.

### Final answer

$$
\text{Graph of } f(x)=2(x-2)^4+1 \text{ is } y=x^4 \text{ shifted right 2, stretched by 2, and shifted up 1.}
$$

---

## 1(b) Zero behavior and end behavior

Given:

$$
f(x)=2(x+3)(x^2+4)^3
$$

### Zeros and behavior near each x-intercept

For x-intercepts, set $f(x)=0$:

$$
2(x+3)(x^2+4)^3=0
$$

- $x+3=0 \Rightarrow x=-3$ (real zero, multiplicity $1$)
- $x^2+4=0 \Rightarrow x=\pm 2i$ (not real, so no x-intercepts)

Therefore the only x-intercept is:

$$
(-3,0)
$$

Since multiplicity at $x=-3$ is odd ($1$), the graph **crosses** the x-axis there.

Sign check around $x=-3$:

- If $x<-3$, then $(x+3)<0$ and $(x^2+4)^3>0$, so $f(x)<0$.
- If $x>-3$, then $(x+3)>0$ and $(x^2+4)^3>0$, so $f(x)>0$.

So it crosses from negative to positive.

### End behavior

Leading term:

$$
2(x)(x^2)^3=2x^7
$$

Hence for large $|x|$, the graph resembles:

$$
y=2x^7
$$

So:

$$
\lim_{x\to\infty} f(x)=\infty,
\qquad
\lim_{x\to-\infty} f(x)=-\infty
$$

**Side note:** Degree $7$ (odd) with positive leading coefficient always gives left tail down, right tail up.

### Final answer

$$
\text{Only real x-intercept: }x=-3\text{ (crosses). End behavior resembles }y=2x^7.
$$

---

## 2) Asymptotes of a rational function

Given:

$$
f(x)=\frac{x^3-1}{x^2-5x-14}
$$

Factor denominator and numerator:

$$
x^2-5x-14=(x-7)(x+2),
\qquad
x^3-1=(x-1)(x^2+x+1)
$$

No common factor, so vertical asymptotes come from denominator zeros:

$$
x=7,\quad x=-2
$$

### Horizontal/oblique asymptote

Degree(numerator) $=3$, degree(denominator) $=2$, difference $=1$.
So there is an **oblique (slant)** asymptote.

Polynomial division:

$$
\frac{x^3-1}{x^2-5x-14}=x+5+\frac{39x+69}{x^2-5x-14}
$$

Thus slant asymptote is:

$$
y=x+5
$$

No horizontal asymptote (because degree of numerator is larger than denominator by 1).

**Side note:** A slant asymptote exists exactly when degree(numerator) is one more than degree(denominator).

### Final answer

- Vertical asymptotes: $x=7$, $x=-2$
- Horizontal asymptote: none
- Oblique asymptote: $y=x+5$

---

## 3) Analyze the graph

Given:

$$
f(x)=\frac{x^2}{x^2+x-6}=\frac{x^2}{(x+3)(x-2)}
$$

### 1. Domain

$$
x\neq -3,\;2
$$

### 2. Intercepts

- $x$-intercepts: numerator $x^2=0 \Rightarrow x=0$ (multiplicity 2), so $(0,0)$
- $y$-intercept: $f(0)=0$, so $(0,0)$

### 3. Vertical asymptotes

Denominator $=0$ at $x=-3,2$ and no cancellation, so:

$$
x=-3,\quad x=2
$$

Behavior:

- $x\to -3^-: f(x)\to +\infty$
- $x\to -3^+: f(x)\to -\infty$
- $x\to 2^-: f(x)\to -\infty$
- $x\to 2^+: f(x)\to +\infty$

### 4. Horizontal asymptote

Degrees equal, so:

$$
y=\frac{1}{1}=1
$$

Crossing horizontal asymptote:

$$
\frac{x^2}{x^2+x-6}=1 \Rightarrow x^2=x^2+x-6 \Rightarrow x=6
$$

So it crosses at $(6,1)$.

### 5. Sign of function

Using test intervals from critical points $-3,0,2$:

- $(-\infty,-3)$: positive
- $(-3,0)$: negative
- $(0,2)$: negative (touches 0 at $x=0$)
- $(2,\infty)$: positive

Because the zero at $x=0$ has multiplicity 2, the graph touches the x-axis at $(0,0)$ and turns back.

**Side note:** Multiplicity 2 at an intercept means "touch and bounce," not crossing.

### Final answer

- Domain: $\mathbb{R}\setminus\{-3,2\}$
- Intercepts: $(0,0)$
- Vertical asymptotes: $x=-3$, $x=2$
- Horizontal asymptote: $y=1$ (crossed at $(6,1)$)
- Sign: positive on $(-\infty,-3)\cup(2,\infty)$, negative on $(-3,0)\cup(0,2)$

---

## 4) Solve the inequality algebraically

Given:

$$
\frac{5}{x-3}\le \frac{3}{x+1}
$$

Bring all terms to one side:

$$
\frac{5}{x-3}-\frac{3}{x+1}\le 0
$$

Common denominator:

$$
\frac{5(x+1)-3(x-3)}{(x-3)(x+1)}\le 0
$$

$$
\frac{2x+14}{(x-3)(x+1)}\le 0
$$

$$
\frac{x+7}{(x-3)(x+1)}\le 0
$$

Critical numbers:

- Zero of numerator: $x=-7$ (included, since $\le 0$)
- Undefined points: $x=-1,3$ (excluded)

Sign chart intervals:

- $(-\infty,-7)$: negative
- $(-7,-1)$: positive
- $(-1,3)$: negative
- $(3,\infty)$: positive

Take negative plus zero point:

$$
(-\infty,-7]\cup(-1,3)
$$

**Side note:** Never include values that make a denominator zero, even in $\le$ or $\ge$ inequalities.

### Final answer

$$
\boxed{(-\infty,-7]\cup(-1,3)}
$$

---

## 5) Real zeros using Rational Zeros Theorem

Given:

$$
f(x)=2x^4+x^3-7x^2-3x+3
$$

### Step 1: Rational candidates

By Rational Zeros Theorem:

$$
\text{Possible rational zeros }=\pm1,\pm3,\pm\frac12,\pm\frac32
$$

### Step 2: Test candidates

- $f(-1)=0 \Rightarrow (x+1)$ is a factor
- $f\!\left(\frac12\right)=0 \Rightarrow (2x-1)$ is a factor

After factoring fully:

$$
f(x)=(x+1)(2x-1)(x^2-3)
$$

### Step 3: Solve remaining factor

$$
x^2-3=0 \Rightarrow x=\pm\sqrt{3}
$$

All real zeros:

$$
-1,\;\frac12,\;\sqrt3,\;-\sqrt3
$$

**Side note:** Rational Zeros Theorem finds only rational candidates; irrational zeros can appear from remaining irreducible factors.

### Final answer

$$
\boxed{x=-1,\;x=\frac12,\;x=\pm\sqrt3}
$$

---

## 6(a) Logarithmic equation

Given:

$$
\log_3(x+1)+\log_3(x+4)=2
$$

### Step 1: Domain

$$
x+1>0,\;x+4>0 \Rightarrow x>-1
$$

### Step 2: Combine logs

$$
\log_3\big((x+1)(x+4)\big)=2
$$

Convert to exponential form:

$$
(x+1)(x+4)=3^2=9
$$

$$
x^2+5x+4=9
$$

$$
x^2+5x-5=0
$$

### Step 3: Solve quadratic

$$
x=\frac{-5\pm\sqrt{25+20}}{2}=\frac{-5\pm3\sqrt5}{2}
$$

### Step 4: Check domain

- $x=\dfrac{-5-3\sqrt5}{2}< -1$ (reject)
- $x=\dfrac{-5+3\sqrt5}{2}> -1$ (accept)

### Final answer

$$
\boxed{x=\frac{-5+3\sqrt5}{2}}
$$

---

## 6(b) Exponential equation

Given:

$$
25^x-8\cdot5^x=-16
$$

Write $25^x=(5^2)^x=5^{2x}$ and let $y=5^x$:

$$
y^2-8y=-16
$$

$$
y^2-8y+16=0
$$

$$
(y-4)^2=0 \Rightarrow y=4
$$

So:

$$
5^x=4 \Rightarrow x=\log_5 4
$$

Approximation:

$$
x\approx 0.8614
$$

**Side note:** Substitution $y=5^x$ converts many exponential equations into standard quadratics.

### Final answer

$$
\boxed{x=\log_5 4\approx 0.8614}
$$

---

## Final compact answer sheet

1(a) Transformations of $y=x^4$: right 2, vertical stretch by 2, up 1; vertex $(2,1)$, axis $x=2$.  
1(b) Only real x-intercept at $x=-3$ (crosses). End behavior like $y=2x^7$: left down, right up.  
2) VA: $x=7,-2$; HA: none; oblique asymptote: $y=x+5$.  
3) Domain $\mathbb{R}\setminus\{-3,2\}$, intercept $(0,0)$, VA at $x=-3,2$, HA $y=1$.  
4) Solution set: $(-\infty,-7]\cup(-1,3)$.  
5) Real zeros: $x=-1,\frac12,\pm\sqrt3$.  
6(a) $x=\dfrac{-5+3\sqrt5}{2}$.  
6(b) $x=\log_5 4\approx0.8614$.
