# Section 4.1 – Application Problems (Problems 81–90)

> **Course:** MAT 116 — Precalculus  
> **Textbook:** Sullivan *Precalculus* 10th Edition  
> **Section:** 4.1  
> **Generated:** April 08, 2026

---

## Problem 81

**Type:** Application Problem  

### Given

> A box with no top is to be made from a 12-inch by 12-inch piece of cardboard by cutting equal squares of side x from each corner and folding up the sides. (a) Express the volume V as a function of x. (b) What is the domain of V? (c) Find the maximum volume and the value of x that gives it.

### Step 1: Define Variables and Diagram

Let $x$ = the side length (in inches) of each square cut from the corners. After cutting and folding:\n- Length of box $= 12 - 2x$\n- Width of box $= 12 - 2x$\n- Height of box $= x$

### Step 2: Write the Volume Function

$$V(x) = \text{length} \times \text{width} \times \text{height}$$$$V(x) = (12 - 2x)(12 - 2x)(x)$$

### Step 3: State the Domain

We need each dimension to be **positive**:\n- $x > 0$\n- $12 - 2x > 0 \Rightarrow x < 6$\n\nTherefore the domain is $0 < x < 6$.

### Step 4: Expand V(x)

First multiply the two binomials:$$(12 - 2x)(12 - 2x) = 144 - 24x - 24x + 4x^2 = 4x^2 - 48x + 144$$Now multiply by $x$:$$V(x) = 4x^3 - 48x^2 + 144x$$

### Step 5: Maximize Volume

Take the derivative and set it to zero (Calculus approach), or use a graphing utility:\n$$V'(x) = 12x^2 - 96x + 144$$Setting $V'(x) = 0$ and solving gives the $x$-value that maximises $V$.\n\nUsing the quadratic formula or a graph, find $x = x_{max}$ in the domain $\left(0, 6\right)$.

### Final Answer

> $V(x) = (12 - 2x)(12 - 2x)(x) = 4x^3 - 48x^2 + 144x$, domain: $0 < x < 6$.

---

## Problem 82

**Type:** Application Problem  

### Given

> A box with no top is to be made from a 10-inch by 16-inch piece of cardboard by cutting equal squares of side x from each corner and folding up the sides. (a) Express the volume V as a function of x. (b) What is the domain of V? (c) Find the maximum volume and the value of x that gives it.

### Step 1: Define Variables and Diagram

Let $x$ = the side length (in inches) of each square cut from the corners. After cutting and folding:\n- Length of box $= 10 - 2x$\n- Width of box $= 16 - 2x$\n- Height of box $= x$

### Step 2: Write the Volume Function

$$V(x) = \text{length} \times \text{width} \times \text{height}$$$$V(x) = (10 - 2x)(16 - 2x)(x)$$

### Step 3: State the Domain

We need each dimension to be **positive**:\n- $x > 0$\n- $10 - 2x > 0 \Rightarrow x < 5$ and $16 - 2x > 0 \Rightarrow x < 8$\n\nTherefore the domain is $0 < x < 5$.

### Step 4: Expand V(x)

First multiply the two binomials:$$(10 - 2x)(16 - 2x) = 160 - 20x - 32x + 4x^2 = 4x^2 - 52x + 160$$Now multiply by $x$:$$V(x) = 4x^3 - 52x^2 + 160x$$

### Step 5: Maximize Volume

Take the derivative and set it to zero (Calculus approach), or use a graphing utility:\n$$V'(x) = 12x^2 - 104x + 160$$Setting $V'(x) = 0$ and solving gives the $x$-value that maximises $V$.\n\nUsing the quadratic formula or a graph, find $x = x_{max}$ in the domain $\left(0, 5\right)$.

### Final Answer

> $V(x) = (10 - 2x)(16 - 2x)(x) = 4x^3 - 52x^2 + 160x$, domain: $0 < x < 5$.

---

## Problem 83

**Type:** Application Problem  

### Given

> The revenue R received by a company selling x units of a product is R(x) = -0.5x^2 + 100x. (a) Find the revenue at x = 50 and x = 120. (b) Find the number of units that maximises revenue. (c) What is the maximum revenue?

### Step 1: Identify the Revenue Function

From the problem: $R(x) = -0.5x^2 + 100x$. This is a **downward-opening parabola** (leading coefficient $< 0$), so it has a maximum.

### Step 2: Find Revenue at Given Points

$R(50) = -0.5(50)^2 + 100(50) = -1250 + 5000 = \$3750$

$R(120) = -0.5(120)^2 + 100(120) = -7200 + 12000 = \$4800$

### Step 3: Maximize Revenue

For a quadratic $R(x) = ax^2 + bx + c$, maximum is at $x = -\dfrac{b}{2a}$.

$$x = -\frac{100}{2(-0.5)} = -\frac{100}{-1} = 100 \text{ units}$$

### Step 4: Maximum Revenue

$$R(100) = -0.5(100)^2 + 100(100) = -5000 + 10000 = \$5000$$

The **maximum revenue** is **$5000** at $x = 100$ units.

### Final Answer

> Max revenue = $\$5000$ at $x = 100$ units.

---

## Problem 84

**Type:** Application Problem  

### Given

> A farmer with 200 feet of fencing wants to enclose a rectangular area and then divide it in half with a fence parallel to one of the sides. (a) Express the total area A enclosed as a function of the width w. (b) What is the maximum area? (c) What dimensions give the maximum area?

### Step 1: Set Up Variables

Let $w$ = width of the rectangle (feet). The fence creates 3 widths and 2 lengths.

Constraint: $3w + 2\ell = 200 \Rightarrow \ell = \dfrac{200 - 3w}{2}$

### Step 2: Express Area as Function of w

$$A(w) = w \cdot \ell = w \cdot \frac{200 - 3w}{2} = \frac{200w - 3w^2}{2}$$

$$A(w) = -\frac{3}{2}w^2 + 100w$$

### Step 3: Find the Maximum

Vertex at $w = -\dfrac{100}{2 \cdot (-3/2)} = -\dfrac{100}{-3} = \dfrac{100}{3} \approx 33.33$ ft

### Step 4: Compute Maximum Area

$$A\!\left(\tfrac{100}{3}\right)= -\tfrac{3}{2}\!\left(\tfrac{100}{3}\right)^{\!2} + 100\cdot\tfrac{100}{3}= -\tfrac{3}{2}\cdot\tfrac{10000}{9} + \tfrac{10000}{3}= -\tfrac{5000}{3} + \tfrac{10000}{3} = \tfrac{5000}{3} \approx 1666.67 \text{ ft}^2$$

### Final Answer

> Max area $\approx 1666.67$ ft² at $w = \tfrac{100}{3}$ ft.

---

## Problem 85

**Type:** Application Problem  

### Given

> A manufacturer finds that the cost C (in dollars) of producing x units is C(x) = 0.002x^3 - 3x^2 + 1500x + 4000. Find the production level x that minimises the marginal cost C'(x).

### Step 1: Identify the Marginal Cost

The cost function is $C(x) = 0.002x^3 - 3x^2 + 1500x + 4000$.

Marginal cost = $C'(x)$ (the derivative):

$$C'(x) = 0.006x^2 - 6x + 1500$$

### Step 2: Minimise Marginal Cost

$C'(x)$ is itself a quadratic in $x$, opening upward ($a = 0.006 > 0$). Its minimum occurs at its vertex:

$$x = -\frac{b}{2a} = -\frac{-6}{2(0.006)} = \frac{6}{0.012} = 500 \text{ units}$$

### Step 3: Verify

$$C'(500) = 0.006(500)^2 - 6(500) + 1500 = 1500 - 3000 + 1500 = 0$$

This confirms $x = 500$ is indeed the minimum of the marginal cost.

### Final Answer

> Marginal cost is minimised at $x = 500$ units.

---

## Problem 86

**Type:** Application Problem  

### Given

> The profit P (in thousands of dollars) a company earns from selling x hundred units is P(x) = -x^3 + 6x^2 + 15x - 12. Find all values of x for which P(x) > 0 (profitable range).

### Step 1: Write the Profit Function

$P(x) = -x^3 + 6x^2 + 15x - 12$ (in thousands of dollars, $x$ = hundreds of units).

### Step 2: Find Zeros

Use the Rational Root Theorem — test $x = \frac{p}{q}$ for factors of 12.

Try $x = -3$: $P(-3) = -(-27) + 6(9) + 15(-3) - 12 = 27 + 54 - 45 - 12 = 24 \ne 0$

Try $x = \frac{1}{1} = 1$: $P(1) = -1 + 6 + 15 - 12 = 8 \ne 0$

Use numerical methods or a graphing utility to find the roots approximately, then determine the interval where $P(x) > 0$.

### Step 3: Sign Analysis

Find all real zeros $x_1 < x_2 < x_3$ using a graphing tool. $P(x) > 0$ on the intervals between zeros where the cubic is positive. Because the leading coefficient is $-1 < 0$, the cubic rises on the left and falls on the right.

### Final Answer

> Use sign analysis on $P(x) = -x^3 + 6x^2 + 15x - 12$ to find the profitable range.

---

## Problem 87

**Type:** Application Problem  

### Given

> A projectile is launched from the ground. Its height h (in feet) after t seconds is modelled by h(t) = -16t^2 + 80t. (a) Find the maximum height. (b) When does it return to the ground?

### Step 1: Write the Height Function

$h(t) = -16t^2 + 80t$ (height in feet, $t$ in seconds).
This is a downward-opening parabola (maximum height exists).

### Step 2: Maximum Height (vertex)

Vertex at $t = -\dfrac{80}{2(-16)} = -\dfrac{80}{-32} = 2.5$ seconds.

$$h(2.5) = -16(2.5)^2 + 80(2.5) = -100 + 200 = 100 \text{ feet}$$

### Step 3: When Does It Return to the Ground?

Set $h(t) = 0$: $-16t^2 + 80t = 0 \Rightarrow t(-16t + 80) = 0$

$t = 0$ (launch) or $t = \dfrac{80}{16} = 5$ seconds.

The projectile returns to the ground at $t = 5$ seconds.

### Final Answer

> Max height: 100 ft at $t = 2.5$ s; returns to ground at $t = 5$ s.

---

## Problem 88

**Type:** Application Problem  

### Given

> The population P (in thousands) of a city t years after 2000 is modelled by P(t) = -0.01t^3 + 0.3t^2 + 2t + 50. (a) What was the population in 2000? (b) Predict the population in 2020.

### Step 1: Identify the Model

$P(t) = -0.01t^3 + 0.3t^2 + 2t + 50$ (thousands), $t$ = years after 2000.

### Step 2: Population in 2000 (t = 0)

$$P(0) = -0.01(0)^3 + 0.3(0)^2 + 2(0) + 50 = 50 \text{ thousand}$$

### Step 3: Population in 2020 (t = 20)

$$P(20) = -0.01(8000) + 0.3(400) + 2(20) + 50$$

$$= -80 + 120 + 40 + 50 = 130 \text{ thousand}$$

### Final Answer

> Year 2000: 50,000; Year 2020: 130,000.

---

## Problem 89

**Type:** Application Problem  

### Given

> A tank in the shape of an inverted cone has height 10 m and base radius 4 m. Water is poured in to a depth of x metres. (a) Express the volume V of water as a polynomial in x. (b) Find V when x = 5.

### Step 1: Set Up Similar Triangles

The full cone has height 10 m and base radius 4 m. At depth $x$, the water radius $r$ satisfies:

$$\frac{r}{x} = \frac{4}{10} = \frac{2}{5} \implies r = \frac{2x}{5}$$

### Step 2: Write Volume as a Polynomial

$$V(x) = \frac{1}{3}\pi r^2 x = \frac{1}{3}\pi \left(\frac{2x}{5}\right)^2 x = \frac{1}{3}\pi \cdot \frac{4x^2}{25} \cdot x = \frac{4\pi}{75}x^3$$

### Step 3: Evaluate at x = 5

$$V(5) = \frac{4\pi}{75}(125) = \frac{500\pi}{75} = \frac{20\pi}{3}\approx 20.94 \text{ m}^3$$

### Final Answer

> $V(x) = \dfrac{4\pi}{75}x^3$; $V(5) = \dfrac{20\pi}{3} \approx 20.94$ m³.

---

## Problem 90

**Type:** Application Problem  

### Given

> A wire 36 inches long is cut into two pieces. One piece is bent into a square and the other into a circle. (a) Express the total area A as a function of the side s of the square. (b) Find the value of s that minimises the total area.

### Step 1: Define Variables

Total wire = 36 inches. Let $s$ = side of the square (inches). Wire for square = $4s$. Wire for circle = $36 - 4s$ = circumference $ = 2\pi r$, so $r = \dfrac{36-4s}{2\pi}$.

### Step 2: Express Total Area

$$A(s) = s^2 + \pi r^2 = s^2 + \pi\left(\frac{36 - 4s}{2\pi}\right)^2= s^2 + \frac{(36 - 4s)^2}{4\pi}$$

### Step 3: Find Minimum

Differentiate and set $A'(s) = 0$:

$$A'(s) = 2s + \frac{2(36 - 4s)(-4)}{4\pi} = 2s - \frac{2(36 - 4s)}{\pi}$$

Setting $A'(s) = 0$: $2s\pi = 2(36 - 4s) \Rightarrow \pi s = 36 - 4s$

$$s(\pi + 4) = 36 \implies s = \frac{36}{\pi + 4} \approx 5.04 \text{ inches}$$

### Final Answer

> $A(s) = s^2 + \dfrac{(36-4s)^2}{4\pi}$; minimised at $s = \dfrac{36}{\pi+4} \approx 5.04$ in.

---
