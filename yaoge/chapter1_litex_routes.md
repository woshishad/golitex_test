# Chapter 1 Theorems and Problems: Litex Proof Routes

This output follows the theorem-to-litex boundary-probing workflow: preserve the book's proof route, name the counted object first, and mark missing Litex support as a blocker instead of replacing it with arithmetic only.

## ch1_theorem_01_basic_counting

- kind: theorem
- source_section: 1.2 The Basic Principle of Counting
- pages: 17-17
- status: translated
- blocker: 

定理/问题内容:

If experiment 1 has m possible outcomes and, for each outcome of experiment 1, experiment 2 has n possible outcomes, then the two experiments together have mn possible outcomes.

可被 Litex 理解的证明链路:

1. Introduce finite sets A and B for the possible outcomes of the first and second experiments.
2. Represent a two-stage outcome as an ordered pair in cart(A, B).
3. Use Litex finite-set support to prove count(cart(A, B)) = count(A) * count(B).
4. Use count(A)=m and count(B)=n to rewrite the final count as m*n.

Litex 对象/谓词候选:

- `A finite_set`
- `B finite_set`
- `cart(A, B)`
- `count(cart(A, B))`

备注:

Candidate route for direct verification. Keep as translated until a concrete .lit file is generated and run.

## ch1_theorem_02_generalized_counting

- kind: theorem
- source_section: 1.2 The Basic Principle of Counting
- pages: 17-17
- status: translated
- blocker: blocked_by_stdlib

定理/问题内容:

For r staged experiments with n1, n2, ..., nr possible outcomes at successive stages, the total number of outcomes is n1*n2*...*nr.

可被 Litex 理解的证明链路:

1. For a fixed finite number of stages, introduce finite sets A1, ..., Ar.
2. Represent a complete experimental outcome as a tuple in cart(A1, ..., Ar).
3. Use count(cart(A1, ..., Ar)) = count(A1)*...*count(Ar).
4. For arbitrary r, a recursive finite product interface would be needed.

Litex 对象/谓词候选:

- `cart(A1, ..., Ar)`
- `count(cart(...))`
- `finite product over stage counts`

备注:

Fixed arity is checkable; arbitrary r needs a finite-list/product theorem.

## ch1_theorem_03_permutations

- kind: theorem
- source_section: 1.3 Permutations
- pages: 19-19
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

There are n! = n(n-1)...3*2*1 possible linear orderings of n distinct items.

可被 Litex 理解的证明链路:

1. Define the set of no-repeat sequences of length n drawn from an n-element finite set.
2. Expose the staged proof route: n choices for the first position, n-1 for the second, and so on.
3. Prove a bijection between no-repeat sequences and staged choice records.
4. Use the generalized counting principle to obtain n!.

Litex 对象/谓词候选:

- `permutations(S)`
- `no-repeat tuple`
- `factorial(count(S))`

备注:

Needs a permutation/no-repeat sequence object and factorial theorem.

## ch1_theorem_04_repeated_permutations

- kind: theorem
- source_section: 1.3 Permutations
- pages: 20-20
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

If n objects are divided into repeated classes of sizes n1, ..., nr, the number of distinguishable linear arrangements is n!/(n1!...nr!).

可被 Litex 理解的证明链路:

1. Start from labeled permutations of n distinct copies.
2. Define an equivalence relation that swaps objects inside each repeated class.
3. Show every visible arrangement has n1!*...*nr! labeled representatives.
4. Divide n! by the internal class permutation count.

Litex 对象/谓词候选:

- `finite quotient`
- `equivalence classes`
- `factorial`

备注:

Needs quotient counting for indistinguishable objects.

## ch1_theorem_05_combination_formula

- kind: theorem
- source_section: 1.4 Combinations
- pages: 21-22
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

The number of r-element subgroups of an n-element set is C(n,r)=n!/((n-r)!r!).

可被 Litex 理解的证明链路:

1. Define the set of r-element subsets of an n-element finite set.
2. Relate ordered r-tuples without repetition to unordered r-subsets.
3. Show each subset has r! ordered listings.
4. Divide n(n-1)...(n-r+1) by r!.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=r}`
- `no-repeat tuple`
- `choose(n,r)`

备注:

Current blocker: from s in power_set(S) and S finite, Litex does not infer s is finite for count(s).

## ch1_theorem_06_pascal_identity

- kind: theorem
- source_section: 1.4 Combinations
- pages: 22-22
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

C(n,r)=C(n-1,r-1)+C(n-1,r).

可被 Litex 理解的证明链路:

1. Fix one distinguished element of an n-element set.
2. Partition r-subsets by whether they contain that element.
3. Subsets containing it correspond to (r-1)-subsets of the remaining n-1 elements.
4. Subsets not containing it correspond to r-subsets of the remaining n-1 elements.
5. Use disjoint union count to add the two counts.

Litex 对象/谓词候选:

- `fixed-cardinality subsets`
- `disjoint union`
- `count(union(A,B))`

备注:

Needs fixed-cardinality subset count and disjoint partition machinery.

## ch1_theorem_07_binomial_theorem

- kind: theorem
- source_section: 1.4 Combinations
- pages: 23-24
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

(x+y)^n = sum_{k=0}^n C(n,k) x^k y^{n-k}.

可被 Litex 理解的证明链路:

1. Induction route: prove base n=1.
2. Assume the expansion for n-1.
3. Multiply by (x+y) and split into two finite sums.
4. Reindex the two sums.
5. Use Pascal identity to combine coefficients.
6. Combinatorial route: each term chooses which k of n factors contribute x.

Litex 对象/谓词候选:

- `finite sum over k`
- `choose(n,k)`
- `polynomial equality`
- `induction on n`

备注:

Concrete polynomial identities are checkable; the general finite-sum theorem needs more support.

## ch1_theorem_08_multinomial_coefficient

- kind: theorem
- source_section: 1.5 Multinomial Coefficients
- pages: 25-25
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

The number of divisions of n distinct items into r labeled groups of sizes n1,...,nr is n!/(n1!...nr!).

可被 Litex 理解的证明链路:

1. Choose n1 items for group 1.
2. Choose n2 items from the remaining items for group 2.
3. Continue until all labeled groups are filled.
4. Multiply the successive combination counts and simplify to n!/(n1!...nr!).

Litex 对象/谓词候选:

- `labeled group tuple`
- `fixed-cardinality subsets`
- `multinomial coefficient`

备注:

Depends on combination formula and labeled finite partitions.

## ch1_theorem_09_multinomial_theorem

- kind: theorem
- source_section: 1.5 Multinomial Coefficients
- pages: 26-27
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

The expansion of (x1+...+xr)^n is indexed by nonnegative n1+...+nr=n with multinomial coefficients.

可被 Litex 理解的证明链路:

1. Expand the product as n choices of one variable among x1,...,xr.
2. Group terms by how many times each variable is selected.
3. Use the multinomial coefficient to count selections with fixed exponents.
4. Sum over all nonnegative exponent vectors whose entries add to n.

Litex 对象/谓词候选:

- `finite multi-index sum`
- `nonnegative exponent vectors`
- `multinomial coefficient`

备注:

Needs finite multi-index sums and multinomial coefficient interfaces.

## ch1_theorem_10_positive_integer_solutions

- kind: proposition
- source_section: 1.6 Integer Solutions
- pages: 28-28
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

The number of positive integer vectors x1+...+xr=n is C(n-1,r-1).

可被 Litex 理解的证明链路:

1. Line up n indistinguishable objects.
2. Choose r-1 of the n-1 gaps as dividers.
3. Map each divider choice to group sizes x1,...,xr.
4. Map each positive solution back to its divider positions.
5. Use the bijection to get C(n-1,r-1).

Litex 对象/谓词候选:

- `positive solution set`
- `gap set with n-1 elements`
- `fixed-cardinality subsets`
- `bijection`

备注:

Needs integer-solution set counting and fixed-cardinality subset count.

## ch1_theorem_11_nonnegative_integer_solutions

- kind: proposition
- source_section: 1.6 Integer Solutions
- pages: 28-28
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

The number of nonnegative integer vectors x1+...+xr=n is C(n+r-1,r-1).

可被 Litex 理解的证明链路:

1. Transform a nonnegative solution x_i into a positive solution y_i=x_i+1.
2. Then y1+...+yr=n+r.
3. Use Proposition 6.1 on positive solutions of sum n+r.
4. Translate back to obtain C(n+r-1,r-1).

Litex 对象/谓词候选:

- `nonnegative solution set`
- `positive solution set`
- `bijection y_i=x_i+1`

备注:

Needs function/bijection between solution sets and stars-and-bars theorem.

## ch1_problems_01

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

(a) How many different 7-place license plates are possible if the first 2 places are for letters and the other 5 for numbers? (b) Repeat part (a) under the assumption that no letter or number can be repeated in a single license plate.

可被 Litex 理解的证明链路:

1. Identify each position of the sequence.
2. Use the book's staged no-repetition count: each later position has fewer available symbols.
3. Try to represent the actual outcomes as no-repeat tuples.
4. If no-repeat tuple support is missing, record the staged product as a proof fragment and mark the tuple bijection blocked.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `finite symbol sets`
- `staged product`

备注:

Needs no-repeat finite sequence support to prove the outcome set itself.

## ch1_problems_02

- kind: problem
- source_section: problems
- pages: 31-31
- status: translated
- blocker: 

定理/问题内容:

How many outcome sequences are possible when a die is rolled four times, where we say, for instance, that the outcome is 3, 4, 3, 1 if the first roll landed on 3, the second on 4, the third on 3, and the fourth on 1?

可被 Litex 理解的证明链路:

1. Represent each independent position as a finite set.
2. Represent the full outcome as a tuple in cart(S1,...,Sk).
3. Use count(cart(...)) = product of the position counts.
4. Evaluate the resulting product.

Litex 对象/谓词候选:

- `finite sets for positions`
- `cart(S1,...,Sk)`
- `count(cart(...))`

备注:

Candidate route for direct verification. Do not mark checkable until a concrete .lit file is generated and run.

## ch1_problems_03

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Twenty workers are to be assigned to 20 different jobs, one to each job. How many different assign- ments are possible?

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_problems_04

- kind: problem
- source_section: problems
- pages: 31-31
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

John, Jim, Jay, and Jack have formed a band con- sisting of 4 instruments. If each of the boys can play all 4 instruments, how many different arrange- ments are possible? What if John and Jim can play all 4 instruments, but Jay and Jack can each play only piano and drums?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_problems_05

- kind: problem
- source_section: problems
- pages: 31-31
- status: translated
- blocker: 

定理/问题内容:

For years, telephone area codes in the United States and Canada consisted of a sequence of three digits. The first digit was an integer between 2 and 9, the second digit was either 0 or 1, and the third digit was any integer from 1 to 9. How many area codes were possible? How many area codes start- ing with a 4 were possible?

可被 Litex 理解的证明链路:

1. Represent each independent position as a finite set.
2. Represent the full outcome as a tuple in cart(S1,...,Sk).
3. Use count(cart(...)) = product of the position counts.
4. Evaluate the resulting product.

Litex 对象/谓词候选:

- `finite sets for positions`
- `cart(S1,...,Sk)`
- `count(cart(...))`

备注:

Candidate route for direct verification. Do not mark checkable until a concrete .lit file is generated and run.

## ch1_problems_06

- kind: problem
- source_section: problems
- pages: 31-31
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

A well-known nursery rhyme starts as follows: “As I was going to St. Ives I met a man with 7 wives. Each wife had 7 sacks. Each sack had 7 cats. Each cat had 7 kittens... ” How many kittens did the traveler meet?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_problems_07

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

(a) In how many ways can 3 boys and 3 girls sit in ar o w? (b) In how many ways can 3 boys and 3 girls sit in a row if the boys and the girls are each to sit together? (c) In how many ways if only the boys must sit together? (d) In how many ways if no two people of the same sex are allowed to sit together?

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_problems_08

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

How many different letter arrangements can be made from the letters (a) Fluke? (b) Propose? (c) Mississippi? (d) Arrange?

可被 Litex 理解的证明链路:

1. Start from labeled permutations.
2. Identify the internal swaps that do not change the visible outcome.
3. Use quotient counting by repeated classes.
4. Evaluate n! divided by the product of repeated-class factorials.

Litex 对象/谓词候选:

- `labeled permutation`
- `finite quotient`
- `repeated-class factorials`

备注:

Needs quotient counting for repeated/indistinguishable objects.

## ch1_problems_09

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

A child has 12 blocks, of which 6 are black, 4 are red, 1 is white, and 1 is blue. If the child puts the blocks in a line, how many arrangements are pos- sible?

可被 Litex 理解的证明链路:

1. Start from labeled permutations.
2. Identify the internal swaps that do not change the visible outcome.
3. Use quotient counting by repeated classes.
4. Evaluate n! divided by the product of repeated-class factorials.

Litex 对象/谓词候选:

- `labeled permutation`
- `finite quotient`
- `repeated-class factorials`

备注:

Needs quotient counting for repeated/indistinguishable objects.

## ch1_problems_10

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

In how many ways can 8 people be seated in a row if (a) there are no restrictions on the seating arrangement? (b) persons A and B must sit next to each other? (c) there are 4 men and 4 women and no 2 men or 2 women can sit next to each other? (d) there are 5 men and they must sit next to each other? (e) there are 4 married couples and each couple must sit together?

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_problems_11

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

In how many ways can 3 novels, 2 mathematics books, and 1 chemistry book be arranged on a bookshelf if (a) the books can be arranged in any order? (b) the mathematics books must be together and the novels must be together? (c) the novels must be together, but the other books can be arranged in any order?

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_problems_12

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Five separate awards (best scholarship, best lead- ership qualities, and so on) are to be presented to selected students from a class of 30. How many dif- ferent outcomes are possible if (a) a student can receive any number of awards? (b) each student can receive at most 1 award?

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_problems_13

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

Consider a group of 20 people. If everyone shakes hands with everyone else, how many handshakes take place?

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_problems_14

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

How many 5-card poker hands are there?

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_problems_15

- kind: problem
- source_section: problems
- pages: 31-31
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

A dance class consists of 22 students, of which 10 are women and 12 are men. If 5 men and 5 women are to be chosen and then paired off, how many results are possible?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_problems_16

- kind: problem
- source_section: problems
- pages: 31-31
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

A student has to sell 2 books from a collection of 6 math, 7 science, and 4 economics books. How many choices are possible if (a) both books are to be on the same subject? (b) the books are to be on different subjects?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_problems_17

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Seven different gifts are to be distributed among 10 children. How many distinct results are possible if no child is to receive more than one gift?

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_problems_18

- kind: problem
- source_section: problems
- pages: 31-31
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

A committee of 7, consisting of 2 Republicans, 2 Democrats, and 3 Independents, is to be cho- sen from a group of 5 Republicans, 6 Democrats, and 4 Independents. How many committees are possible?

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_problems_19

- kind: problem
- source_section: problems
- pages: 31-32
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

From a group of 8 women and 6 men, a committee consisting of 3 men and 3 women is to be formed. How many different committees are possible if (a) 2 of the men refuse to serve together? (b) 2 of the women refuse to serve together? (c) 1 man and 1 woman refuse to serve together? Problems 17

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_problems_20

- kind: problem
- source_section: problems
- pages: 32-32
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

A person has 8 friends, of whom 5 will be invited to a party. (a) How many choices are there if 2 of the friends are feuding and will not attend together? (b) How many choices if 2 of the friends will only attend together?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_problems_21

- kind: problem
- source_section: problems
- pages: 32-32
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Consider the grid of points shown here. Suppose that, starting at the point labeled A, you can go one step up or one step to the right at each move. This procedure is continued until the point labeled B is reached. How many different paths from A to B are possible? Hint: Note that to reach B from A, you must take 4 steps to the right and 3 steps upward. B A

可被 Litex 理解的证明链路:

1. Represent each path as a word in moves R and U.
2. Fix the number of R and U moves required.
3. Count words with a fixed number of one move type using combinations.

Litex 对象/谓词候选:

- `binary word`
- `fixed-cardinality subset of move positions`
- `choose(n,k)`

备注:

Needs fixed-cardinality subset or fixed-weight word counting.

## ch1_problems_22

- kind: problem
- source_section: problems
- pages: 32-32
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

In Problem 21, how many different paths are there from A to B that go through the point circled in the following lattice? B A

可被 Litex 理解的证明链路:

1. Represent each path as a word in moves R and U.
2. Fix the number of R and U moves required.
3. Count words with a fixed number of one move type using combinations.

Litex 对象/谓词候选:

- `binary word`
- `fixed-cardinality subset of move positions`
- `choose(n,k)`

备注:

Needs fixed-cardinality subset or fixed-weight word counting.

## ch1_problems_23

- kind: problem
- source_section: problems
- pages: 32-32
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

A psychology laboratory conducting dream research contains 3 rooms, with 2 beds in each room. If 3 sets of identical twins are to be assigned to these 6 beds so that each set of twins sleeps in different beds in the same room, how many assignments are possible?

可被 Litex 理解的证明链路:

1. Start from labeled permutations.
2. Identify the internal swaps that do not change the visible outcome.
3. Use quotient counting by repeated classes.
4. Evaluate n! divided by the product of repeated-class factorials.

Litex 对象/谓词候选:

- `labeled permutation`
- `finite quotient`
- `repeated-class factorials`

备注:

Needs quotient counting for repeated/indistinguishable objects.

## ch1_problems_24

- kind: problem
- source_section: problems
- pages: 32-32
- status: translated
- blocker: blocked_by_stdlib

定理/问题内容:

Expand (3x 2 + y)5.

可被 Litex 理解的证明链路:

1. Identify the polynomial expression to expand.
2. For a concrete exponent, use algebraic normalization/equality chains.
3. For a general exponent, use binomial or multinomial coefficient theorem.

Litex 对象/谓词候选:

- `polynomial expression`
- `coefficient formula`
- `finite sums`

备注:

Concrete polynomial identities are often checkable; general finite-sum formulas need stdlib support.

## ch1_problems_25

- kind: problem
- source_section: problems
- pages: 32-32
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

The game of bridge is played by 4 players, each of whom is dealt 13 cards. How many bridge deals are possible?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_problems_26

- kind: problem
- source_section: problems
- pages: 32-32
- status: translated
- blocker: blocked_by_stdlib

定理/问题内容:

Expand (x1 + 2x2 + 3x3)4.

可被 Litex 理解的证明链路:

1. Identify the polynomial expression to expand.
2. For a concrete exponent, use algebraic normalization/equality chains.
3. For a general exponent, use binomial or multinomial coefficient theorem.

Litex 对象/谓词候选:

- `polynomial expression`
- `coefficient formula`
- `finite sums`

备注:

Concrete polynomial identities are often checkable; general finite-sum formulas need stdlib support.

## ch1_problems_27

- kind: problem
- source_section: problems
- pages: 32-32
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

If 12 people are to be divided into 3 committees of respective sizes 3, 4, and 5, how many divisions are possible?

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_problems_28

- kind: problem
- source_section: problems
- pages: 32-32
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

If 8 new teachers are to be divided among 4 schools, how many divisions are possible? What if each school must receive 2 teachers?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_problems_29

- kind: problem
- source_section: problems
- pages: 32-32
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Ten weight lifters are competing in a team weight- lifting contest. Of the lifters, 3 are from the United States, 4 are from Russia, 2 are from China, and 1 is from Canada. If the scoring takes account of the countries that the lifters represent, but not their individual identities, how many different outcomes are possible from the point of view of scores? How many different outcomes correspond to results in which the United States has 1 competitor in the top three and 2 in the bottom three?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_problems_30

- kind: problem
- source_section: problems
- pages: 32-32
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Delegates from 10 countries, including Russia, France, England, and the United States, are to be seated in a row. How many different seat- ing arrangements are possible if the French and English delegates are to be seated next to each other and the Russian and U.S. delegates are not to be next to each other?

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_problems_31

- kind: problem
- source_section: problems
- pages: 32-32
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

If 8 identical blackboards are to be divided among 4 schools, how many divisions are possible? How many if each school must receive at least 1 black- board?

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_problems_32

- kind: problem
- source_section: problems
- pages: 32-32
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

An elevator starts at the basement with 8 peo- ple (not including the elevator operator) and dis- charges them all by the time it reaches the top floor, number 6. In how many ways could the oper- ator have perceived the people leaving the eleva- tor if all people look alike to him? What if the 8 people consisted of 5 men and 3 women and the operator could tell a man from a woman?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_problems_33

- kind: problem
- source_section: problems
- pages: 32-33
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

We have 20 thousand dollars that must be invested among 4 possible opportunities. Each investment must be integral in units of 1 thousand dollars, and there are minimal investments that need to be made if one is to invest in these opportunities. The minimal investments are 2, 2, 3, and 4 thousand dollars. How many different investment strategies are available if (a) an investment must be made in each opportu- nity? (b) investments must be made in at least 3 of the 4 opportunities? 18 Chapter 1 Combinatorial Analysis

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_theoretical_exercises_01

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Prove the generalized version of the basic counting principle.

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_theoretical_exercises_02

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Two experiments are to be performed. The first can result in any one of m possible outcomes. If the first experiment results in outcome i, then the second experiment can result in any of ni possible outcomes, i = 1, 2,..., m. What is the number of possible outcomes of the two experiments?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_theoretical_exercises_03

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

In how many ways can r objects be selected from a set of n objects if the order of selection is consid- ered relevant?

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_theoretical_exercises_04

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

There are ⎨ n r ⎩ different linear arrangements of n balls of which r are black and n -r are white. Give a combinatorial explanation of this fact.

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_theoretical_exercises_05

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Determine the number of vectors (x1,..., xn),s u c h that each xi is either 0 or 1 and n∑ i=1 xi >= k

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_theoretical_exercises_06

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

How many vectors x1,..., xk are there for which each xi is a positive integer such that 1 <= xi <= n and x1 < x2 < ··· < xk?

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_theoretical_exercises_07

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Give an analytic proof of Equation (4.1).

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_theoretical_exercises_08

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Prove that ⎨ n + m r ⎩ = ⎨ n 0 ⎩⎨ m r ⎩ + ⎨ n 1 ⎩⎨ m r - 1 ⎩ +··· + ⎨ n r ⎩⎨ m 0 ⎩ Hint: Consider a group of n men and m women. How many groups of size r are possible?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_theoretical_exercises_09

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Use Theoretical Exercise 8 to prove that ⎨ 2n n ⎩ = n∑ k=0 ⎨ n k ⎩2

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_theoretical_exercises_10

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

From a group of n people, suppose that we want to choose a committee of k, k <= n, one of whom is to be designated as chairperson. (a) By focusing first on the choice of the commit- tee and then on the choice of the chair, argue that there are ⎨ n k ⎩ k possible choices. (b) By focusing first on the choice of the nonchair committee members and then on the choice of the chair, argue that there are⎨ n k - 1 ⎩ (n - k + 1) possible choices. (c) By focusing first on the choice of the chair and then on the choice of the other committee members, argue that there are n ⎨ n - 1 k - 1 ⎩ possible choices. (d) Conclude from parts (a), (b), and (c) that k ⎨ n k ⎩ = (n-k+ 1) ⎨ n k - 1 ⎩ = n ⎨ n - 1 k - 1 ⎩ (e) Use the factorial definition of ⎨ m r ⎩ to verify the identity in part (d).

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_theoretical_exercises_11

- kind: problem
- source_section: theoretical_exercises
- pages: 33-33
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

The following identity is known as Fermat’s com- binatorial identity: ⎨ n k ⎩ = n∑ i=k ⎨ i - 1 k - 1 ⎩ n >= k Give a combinatorial argument (no computations are needed) to establish this identity. Hint: Consider the set of numbers 1 through n. How many subsets of size k have i as their highest- numbered member?

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_theoretical_exercises_12

- kind: problem
- source_section: theoretical_exercises
- pages: 33-34
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

Consider the following combinatorial identity: n∑ k=1 k ⎨ n k ⎩ = n · 2n-1 (a) Present a combinatorial argument for this identity by considering a set of n people and determining, in two ways, the number of pos- sible selections of a committee of any size and a chairperson for the committee. Hint: (i) How many possible selections are there o fac o m m i t t e eo fs i z ek and its chairper- son? (ii) How many possible selections are there of a chairperson and the other commit- tee members? (b) Verify the following identity for n = 1, 2, 3, 4, 5: n∑ k=1 ⎨ n k ⎩ k2 = 2n-2n(n + 1) Theoretical Exercises 19 For a combinatorial proof of the preceding, consider a set of n people and argue that both sides of the identity represent the number of different selections of a committee, its chair- person, and its secretary (possibly the same as the chairperson). Hint: (i) How many different selections result in the committee containing exactly k peo- ple? (ii) How many different selections are there in which the chairperson and the secre- tary are the same? ( ANSWER: n2n-1.) (iii) How many different selections result in the chairperson and the secretary being different? (c) Now argue that n∑ k=1 ⎨ n k ⎩ k3 = 2n-3n2(n + 3)

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_theoretical_exercises_13

- kind: problem
- source_section: theoretical_exercises
- pages: 34-34
- status: translated
- blocker: blocked_by_stdlib

定理/问题内容:

Show that, for n > 0, n∑ i=0 (-1)i ⎨ n i ⎩ = 0 Hint: Use the binomial theorem.

可被 Litex 理解的证明链路:

1. Identify the polynomial expression to expand.
2. For a concrete exponent, use algebraic normalization/equality chains.
3. For a general exponent, use binomial or multinomial coefficient theorem.

Litex 对象/谓词候选:

- `polynomial expression`
- `coefficient formula`
- `finite sums`

备注:

Concrete polynomial identities are often checkable; general finite-sum formulas need stdlib support.

## ch1_theoretical_exercises_14

- kind: problem
- source_section: theoretical_exercises
- pages: 34-34
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

From a set of n people, a committee of size j is to be chosen, and from this committee, a subcommittee of size i, i <= j, is also to be chosen. (a) Derive a combinatorial identity by comput- ing, in two ways, the number of possible choices of the committee and subcommittee- first by supposing that the committee is chosen first and then the subcommittee is chosen, and second by supposing that the subcommittee is chosen first and then the remaining members of the committee are chosen. (b) Use part (a) to prove the following combina- torial identity: n∑ j=i ⎨ n j ⎩⎨ j i ⎩ = ⎨ n i ⎩ 2n-i i <= n (c) Use part (a) and Theoretical Exercise 13 to show that n∑ j=i ⎨ n j ⎩⎨ j i ⎩ (-1)n-j = 0 i < n

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_theoretical_exercises_15

- kind: problem
- source_section: theoretical_exercises
- pages: 34-34
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Let Hk(n) be the number of vectors x1,..., xk for which each xi is a positive integer satisfying 1 <= xi <= n and x1 <= x2 <= ··· <= xk. (a) Without any computations, argue that H1(n) = n Hk(n) = n∑ j=1 Hk-1(j) k > 1 Hint: How many vectors are there in which xk = j? (b) Use the preceding recursion to compute H3(5). Hint: First compute H2(n) for n = 1, 2, 3, 4, 5.

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_theoretical_exercises_16

- kind: problem
- source_section: theoretical_exercises
- pages: 34-34
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Consider a tournament of n contestants in which the outcome is an ordering of these contestants, with ties allowed. That is, the outcome partitions the players into groups, with the first group consist- ing of the players that tied for first place, the next group being those that tied for the next-best posi- tion, and so on. Let N(n) denote the number of dif- ferent possible outcomes. For instance, N(2) = 3, since, in a tournament with 2 contestants, player 1 could be uniquely first, player 2 could be uniquely first, or they could tie for first. (a) List all the possible outcomes when n = 3. (b) With N(0) defined to equal 1, argue, without any computations, that N(n) = n∑ i=1 ⎨ n i ⎩ N(n - i) Hint: How many outcomes are there in which i players tie for last place? (c) Show that the formula of part (b) is equivalent to the following: N(n) = n-1∑ i=0 ⎨ n i ⎩ N(i) (d) Use the recursion to find N(3) and N(4).

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_theoretical_exercises_17

- kind: problem
- source_section: theoretical_exercises
- pages: 34-35
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Present a combinatorial explanation of why⎨ n r ⎩ = ⎨ n r, n - r ⎩. 20 Chapter 1 Combinatorial Analysis

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_theoretical_exercises_18

- kind: problem
- source_section: theoretical_exercises
- pages: 35-35
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Argue that ⎨ n n1, n2,..., nr ⎩ = ⎨ n - 1 n1 - 1, n2,..., nr ⎩ + ⎨ n - 1 n1, n2 - 1,..., nr ⎩ + ··· + ⎨ n - 1 n1, n2,..., nr - 1 ⎩ Hint: Use an argument similar to the one used to establish Equation (4.1).

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_theoretical_exercises_19

- kind: problem
- source_section: theoretical_exercises
- pages: 35-35
- status: translated
- blocker: blocked_by_stdlib

定理/问题内容:

Prove the multinomial theorem.

可被 Litex 理解的证明链路:

1. Identify the polynomial expression to expand.
2. For a concrete exponent, use algebraic normalization/equality chains.
3. For a general exponent, use binomial or multinomial coefficient theorem.

Litex 对象/谓词候选:

- `polynomial expression`
- `coefficient formula`
- `finite sums`

备注:

Concrete polynomial identities are often checkable; general finite-sum formulas need stdlib support.

## ch1_theoretical_exercises_20

- kind: problem
- source_section: theoretical_exercises
- pages: 35-35
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

In how many ways can n identical balls be dis- tributed into r urns so that the ith urn contains at least mi balls, for each i = 1,..., r? Assume that n >= ∑r i=1 mi.

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_theoretical_exercises_21

- kind: problem
- source_section: theoretical_exercises
- pages: 35-35
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Argue that there are exactly ⎨ r k ⎩⎨ n - 1 n - r + k ⎩ solutions of x1 + x2 + ··· + xr = n for which exactly k of the xi are equal to 0.

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_theoretical_exercises_22

- kind: problem
- source_section: theoretical_exercises
- pages: 35-35
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Consider a function f(x1,..., xn) of n variables. How many different partial derivatives of order r does f possess?

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_theoretical_exercises_23

- kind: problem
- source_section: theoretical_exercises
- pages: 35-35
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Determine the number of vectors (x1,..., xn) such that each xi is a nonnegative integer and n∑ i=1 xi <= k

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_self_test_01

- kind: problem
- source_section: self_test
- pages: 35-35
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

How many different linear arrangements are there of the letters A, B, C, D, E, F for which (a) A and B are next to each other? (b) Ai sb e f o r eB? (c) A is before B and B is before C? (d) A is before B and C is before D? (e) A and B are next to each other and C and D are also next to each other? (f) E is not last in line?

可被 Litex 理解的证明链路:

1. Start from labeled permutations.
2. Identify the internal swaps that do not change the visible outcome.
3. Use quotient counting by repeated classes.
4. Evaluate n! divided by the product of repeated-class factorials.

Litex 对象/谓词候选:

- `labeled permutation`
- `finite quotient`
- `repeated-class factorials`

备注:

Needs quotient counting for repeated/indistinguishable objects.

## ch1_self_test_02

- kind: problem
- source_section: self_test
- pages: 35-35
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

If 4 Americans, 3 French people, and 3 British people are to be seated in a row, how many seat- ing arrangements are possible when people of the same nationality must sit next to each other?

可被 Litex 理解的证明链路:

1. Start from labeled permutations.
2. Identify the internal swaps that do not change the visible outcome.
3. Use quotient counting by repeated classes.
4. Evaluate n! divided by the product of repeated-class factorials.

Litex 对象/谓词候选:

- `labeled permutation`
- `finite quotient`
- `repeated-class factorials`

备注:

Needs quotient counting for repeated/indistinguishable objects.

## ch1_self_test_03

- kind: problem
- source_section: self_test
- pages: 35-35
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

A president, treasurer, and secretary, all different, are to be chosen from a club consisting of 10 peo- ple. How many different choices of officers are possible if (a) there are no restrictions? (b) A and B will not serve together? (c) C and D will serve together or not at all? (d) E must be an officer? (e) F will serve only if he is president?

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_self_test_04

- kind: problem
- source_section: self_test
- pages: 35-35
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

A student is to answer 7 out of 10 questions in an examination. How many choices has she? How many if she must answer at least 3 of the first 5 questions?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_self_test_05

- kind: problem
- source_section: self_test
- pages: 35-35
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

In how many ways can a man divide 7 gifts among his 3 children if the eldest is to receive 3 gifts and the others 2 each?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_self_test_06

- kind: problem
- source_section: self_test
- pages: 35-35
- status: translated
- blocker: 

定理/问题内容:

How many different 7-place license plates are pos- sible when 3 of the entries are letters and 4 are digits? Assume that repetition of letters and num- bers is allowed and that there is no restriction on where the letters or numbers can be placed.

可被 Litex 理解的证明链路:

1. Represent each independent position as a finite set.
2. Represent the full outcome as a tuple in cart(S1,...,Sk).
3. Use count(cart(...)) = product of the position counts.
4. Evaluate the resulting product.

Litex 对象/谓词候选:

- `finite sets for positions`
- `cart(S1,...,Sk)`
- `count(cart(...))`

备注:

Candidate route for direct verification. Do not mark checkable until a concrete .lit file is generated and run.

## ch1_self_test_07

- kind: problem
- source_section: self_test
- pages: 35-35
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Give a combinatorial explanation of the identity ⎨ n r ⎩ = ⎨ n n - r ⎩

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_self_test_08

- kind: problem
- source_section: self_test
- pages: 35-35
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Consider n-digit numbers where each digit is one of the 10 integers 0, 1,..., 9. How many such num- bers are there for which (a) no two consecutive digits are equal? (b) 0 appears as a digit a total of i times, i = 0,..., n?

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_self_test_09

- kind: problem
- source_section: self_test
- pages: 35-35
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Consider three classes, each consisting of n stu- dents. From this group of 3 n students, a group of 3 students is to be chosen. (a) How many choices are possible? (b) How many choices are there in which all 3 stu- dents are in the same class? (c) How many choices are there in which 2 of the 3 students are in the same class and the other student is in a different class? (d) How many choices are there in which all 3 stu- dents are in different classes? (e) Using the results of parts (a) through (d), write a combinatorial identity.

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_self_test_10

- kind: problem
- source_section: self_test
- pages: 35-35
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

How many 5-digit numbers can be formed from the integers 1, 2,..., 9 if no digit can appear more than twice? (For instance, 41434 is not allowed.)

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_self_test_11

- kind: problem
- source_section: self_test
- pages: 35-36
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

From 10 married couples, we want to select a group of 6 people that is not allowed to contain a married couple. (a) How many choices are there? (b) How many choices are there if the group must also consist of 3 men and 3 women? Self-Test Problems and Exercises 21

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_self_test_12

- kind: problem
- source_section: self_test
- pages: 36-36
- status: blocked
- blocker: blocked_by_infer_rule

定理/问题内容:

A committee of 6 people is to be chosen from a group consisting of 7 men and 8 women. If the committee must consist of at least 3 women and at least 2 men, how many different committees are possible?

可被 Litex 理解的证明链路:

1. Identify the underlying finite population set.
2. Represent the choice as a fixed-cardinality subset.
3. If there are restrictions, partition the subset family or subtract forbidden subset families.
4. Apply the combination formula or inclusion-exclusion.

Litex 对象/谓词候选:

- `{s power_set(S): count(s)=k}`
- `fixed-cardinality subset count`
- `set partition`

备注:

Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.

## ch1_self_test_13

- kind: problem
- source_section: self_test
- pages: 36-36
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

An art collection on auction consisted of 4 Dalis, 5 van Goghs, and 6 Picassos. At the auction were 5 art collectors. If a reporter noted only the number of Dalis, van Goghs, and Picassos acquired by each collector, how many different results could have been recorded if all of the works were sold?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_self_test_14

- kind: problem
- source_section: self_test
- pages: 36-36
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

Determine the number of vectors (x1,..., xn) such that each xi is a positive integer and n∑ i=1 xi <= k where k >= n.

可被 Litex 理解的证明链路:

1. Represent the allocation or vector as integer variables x1,...,xr.
2. Translate constraints into a sum equation and lower bounds.
3. Shift variables if lower bounds are positive.
4. Apply positive or nonnegative stars-and-bars.

Litex 对象/谓词候选:

- `integer solution set`
- `variable shift`
- `stars-and-bars bijection`

备注:

Needs integer-solution set counting and stars-and-bars theorem.

## ch1_self_test_15

- kind: problem
- source_section: self_test
- pages: 36-36
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

A total of n students are enrolled in a review course for the actuarial examination in probability. The posted results of the examination will list the names of those who passed, in decreasing order of their scores. For instance, the posted result will be “Brown, Cho” if Brown and Cho are the only ones to pass, with Brown receiving the higher score. Assuming that all scores are distinct (no ties), how many posted results are possible?

可被 Litex 理解的证明链路:

1. Represent the outcome as a no-repeat sequence or assignment.
2. Use staged choices: n choices, then n-1, and so on.
3. Prove a bijection between staged records and the source outcome object.
4. Evaluate the product.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `permutation(S)`
- `staged product`

备注:

Needs permutation/no-repeat sequence support.

## ch1_self_test_16

- kind: problem
- source_section: self_test
- pages: 36-36
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

H o wm a n ys u b s e t so fs i z e4o ft h es e t S = {1, 2,...,2 0} contain at least one of the elements 1, 2, 3, 4, 5?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_self_test_17

- kind: problem
- source_section: self_test
- pages: 36-36
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

Give an analytic verification of ⎨n 2 ⎩ = ⎨k 2 ⎩ + k(n - k) + ⎨n - k 2 ⎩,1 <= k <= n Now, give a combinatorial argument for this identity.

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_self_test_18

- kind: problem
- source_section: self_test
- pages: 36-36
- status: translated
- blocker: blocked_by_formulation

定理/问题内容:

In a certain community, there are 3 families con- sisting of a single parent and 1 child, 3 families consisting of a single parent and 2 children, 5 fam- ilies consisting of 2 parents and a single child, 7 families consisting of 2 parents and 2 children, and 6 families consisting of 2 parents and 3 children. If a parent and child from the same family are to be chosen, how many possible choices are there?

可被 Litex 理解的证明链路:

1. Identify the finite outcome object described by the problem.
2. Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.
3. Write the counted object before evaluating arithmetic.
4. Run Litex on the object-level formulation and classify the first failure.

Litex 对象/谓词候选:

- `finite outcome set`
- `count(...)`

备注:

Manual classification needed.

## ch1_self_test_19

- kind: problem
- source_section: self_test
- pages: 36-36
- status: blocked
- blocker: blocked_by_stdlib

定理/问题内容:

If there are no restrictions on where the digits and letters are placed, how many 8-place license plates consisting of 5 letters and 3 digits are possible if no repetitions of letters or digits are allowed. What if the 3 digits must be consecutive?

可被 Litex 理解的证明链路:

1. Identify each position of the sequence.
2. Use the book's staged no-repetition count: each later position has fewer available symbols.
3. Try to represent the actual outcomes as no-repeat tuples.
4. If no-repeat tuple support is missing, record the staged product as a proof fragment and mark the tuple bijection blocked.

Litex 对象/谓词候选:

- `no-repeat tuple`
- `finite symbol sets`
- `staged product`

备注:

Needs no-repeat finite sequence support to prove the outcome set itself.
