# Metaphor Knowledge Bases
Katya Ovchinnikova, Ross Israel, Jonathan Gordon

Available abductive knowledge bases are stored in this directory.

## Prefixes

- S#: source domain
- SS#: source subdomain
- T#: target super-domain
- TS#: target domain
- TSS#: target subdomain
- R#: role, e.g., agent
- M#: mapping
- I#: international (i.e., culturally independent)


## Metaphor Source Lexical Axioms

Map linguistic phrases to source domains and subdomains. Source domains
are described in the comments of the KBs and in the government source
lists. As of July 2014, this is in the shared Dropbox folder:
  Metaphor/Option Year 2/Government Documents/meta source list final 062014.xlsx
E.g.,

    (B (name disease)
       (=> (^ (S#DISEASE x :0.45) (SS#DISEASE%TYPE x :0.45))
           (disease-nn e0 x)))

These can also fill in roles. E.g., if someone is sick, she filles in the
R#SICK role for the S#DISEASE frame:

    (B (name sick)
       (=> (^ (S#DISEASE e0 :0.3) (SS#DISEASE%TYPE x :0.3) (R#SICK y e0 :0.3))
           (sick-adj e0 y)))

And if someone cures a disease, she fills in the R#CURE-AGENT role:

    (B (name treat)
       (=> (^ (S#DISEASE x :0.3) (SS#DISEASE%TREATMENT e0 :0.3)
              (R#CURE-AGENT y e0 :0.3))
           (treat-vb e0 y x u2)))

The total costs of the antecedent should be less than 1.

Source axioms are stored under KBs/*/*-sources.txt


## Metaphor Target Lexical Axioms

Map linguistic phrases to target domains and subdomains. E.g.,

    (B (name poverty)
       (=> (^ (T#ECONOMIC-INEQUALITY u :0.45) (TS#POVERTY x :0.45))
           (poverty-nn e0 x)))

    (B (name become-poor)
       (=> (^ (T#ECONOMIC-INEQUALITY u :0.3) (TS#POVERTY e0 :0.3)
              (R#POOR e0 :0.3))
           (^ (become-vb e1 x e0 u) (poor-adj e0 y))))

The total costs of the antecedent should be less than 1.

Target axioms are stored under KBs/*/*-targets.txt


## Target-source Mapping Axioms

We map language-specific concepts to international (language-independent)
ones. This is a holdover from when the domain and subdomain names for
non-English languages were bilingual (e.g., S#ENFERMEDAD/DISEASE). This
was abandoned, presumably so output would match the expected labels. These
axioms look like:

    (B (name disease-map)
       (=> (I#DISEASE x :0.9)
           (S#DISEASE x)))

We then have mapping axioms that operate on international concepts and
make inferences important for explicit interpretation of conceptual
metaphors (comparison of target and source). Mapping concepts that will
appear in the output are prefixed with M#.

E.g., a disease causes a sick entity not to function:

    (B (name disease)
       (=> (^ (M#CAUSE-NOT-FUNCTION e0 :0.3) (M#CAUSING-THING-F x e0 :0.3)
              (M#FUNCTION-AGENT y e0 :0.3))
           (^ (I#DISEASE x) (R#SICK y x))))

If someone or thing cures a disease, it causes the disease not to exit:

    (B (name cure)
       (=> (^ (M#CAUSE-NOT-EXIST e1 :0.3) (M#CAUSING-THING_E y e1 :0.3)
              (M#EXISTING-THING x e1 :0.3))
           (^ (I#CURE e0) (R#CURE-AGENT y e0) (R#SICK x d) (S#DISEASE d))))

NB: Don't use general predicates like 'cause' or 'not' in isolation; use
more complex predicates like 'cause-not-exist' instead. More general
predicates can be unexpectedly unified during abductive inference.

Mapping axioms can be found in 'KBs/common/economic_inequality_ontology.txt'.


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
