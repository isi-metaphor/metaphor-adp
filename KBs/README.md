# Metaphor Knowledge Bases
Jonathan Gordon, Ross Israel, Katya Ovchinnikova

This directory contains the abductive knowledge bases for metaphor
interpretation, divided by language, and scripts for generating axioms.


## Prefixes

- C#: category/schema, e.g., C#HEALTH_AND_SAFETY
- S#: source domain, e.g., S#ADDICTION
- T#: target super-domain, e.g., T#ECONOMIC_INEQUALITY
- TS#: target domain, e.g., TS#POVERTY
- TSS#: target subdomain
- R#: role, e.g., R#THREAT

No longer in use or being phased out:
- SS#: source subdomain, e.g., SS#PARASITE%ACTION
- TSS#: target subdomain
- M#: mapping
- I#: international/culture-independent. (These were used when the source
  and target predicates were language-specific.)


## Predicate Argument Structure

(*-vb e x y u):
- e, eventuality
- x, subject
- y, direct object
- u, indirect object

(*-nn e x):
- e, eventuality
- x, subject

(*-in e x y):
- e, eventuality
- x, head (vb/noun)
- y, dependent

(*-adj e x):
- e, eventuality,
- x, object of modification

(*-rb e1 e2):
- adverb with eventuality e1 modifying eventuality e2


## Rule Weights

The total weight of the left-hand side of the rules should be less than
1 -- typically 0.9.


## Metaphor Source Lexical Axioms

Map linguistic phrases to source domains and subdomains. Source domains
are described in the comments of the KBs and in the government source
lists. E.g.,

    (B (name disease-nn)
       (=> (S#DISEASE e0 :0.9)
           (disease-nn e0 x0)))

These can also fill in roles. E.g., if someone is sick, she fills in the
R#SICK role for the S#DISEASE frame:

    (B (name sick-adj)
       (=> (^ (S#DISEASE e0 :0.45) (R#SICK x0 e0 :0.45))
           (sick-adj e0 x0)))

Source axioms are stored under KBs/*/*-sources.txt


## Metaphor Target Lexical Axioms

Map linguistic phrases to target domains and subdomains. E.g.,

    (B (name poverty-nn)
       (=> (^ (T#ECONOMIC_INEQUALITY u :0.45) (TS#POVERTY x :0.45))
           (poverty-nn e0 x)))

    (B (name become-poor)
       (=> (^ (T#ECONOMIC_INEQUALITY u :0.45) (TS#POVERTY e0 :0.45))
           (^ (become-vb e1 x e0 u) (poor-adj e0 y))))

Target axioms are stored under KBs/*/*-targets.txt


## Rule Format

Abductive axioms have the following format:

```
<axiom> ::= "(B (name " <axiom name> ") (=> " <lhs> <rhs> "))"
<axiom name> ::= <ASCII string, no spaces>
<lhs> ::= <proposition with weight> | "(^ " <conjunction of propositions with weights> ")"
<rhs> ::= <proposition> | "(^ " <conjunction of propositions> ")"
<conjunction of propositions with weights> ::= <proposition with weight> | <proposition with weight> " " <conjunction of propositions with weights>
<conjunction of propositions> ::= <proposition> | <proposition> " " <conjunction of propositions>
<proposition with weight> ::= "(" <proposition name> " " <arguments> " :" <weight> ")"
<proposition> ::= "(" <proposition name> " " <arguments> ")"
<proposition name> ::= <UTF-8 string, no spaces>
<arguments> ::= "" | <argument> | <argument> " " <arguments>
<argument> ::= <ASCII string, no spaces>
<weight> ::= <FLOAT>
```

Example:

```
(B (name conflict-with)
   (=> (conflict e x y g h :0.9)
       (^ (conflict-vb e g u1 u2) (with-in e1 e y))))
(B (name rvatsja-k)
   (=> (^ (conflict c x y g h :0.6) (adversary e1 x y c :0.3))
       (^ (рваться-vb c x u1 u2) (к-in e2 c g))))
```


## Compiling KBs

A knowledge base can be compiled by
[Henry](https://github.com/naoya-i/henry-n700) using the following command:

    henry -m compile_kb -o KB_COMPILED_PATH KB_PATH

where KB_PATH can contain several space-separated paths to different files.
For Mac users, the output path is required to come before the KB_PATH.
