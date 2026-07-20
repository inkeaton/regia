# BNF Grammar
---

## 1. File structure

```
<program>        ::= <item> <program-tail>
<program-tail>   ::= <item> <program-tail>
                   |

<item>           ::= <element-decl>
                   | <playbook-def>
                   | <plot-def>

<element-decl>   ::= <action-decl>
                   | <event-decl>
                   | <fact-decl>
```

## 2. Base element declarations

```
<action-decl>    ::= 'ACTION' ID <opt-param-names> '.'
<event-decl>     ::= 'EVENT' ID <opt-event-origin> '.'
<fact-decl>      ::= 'FACT' ID <opt-param-names> '.'

<opt-param-names> ::= <param-names>
                    |

<param-names>    ::= '(' ID <id-tail> ')'
<id-tail>        ::= ',' ID <id-tail>
                   |

<opt-event-origin> ::= <event-origin>
                     |

<event-origin>   ::= 'SELF'
                   | 'ENVIRONMENT'
```

## 3. Playbooks

```
<playbook-def>       ::= 'PLAYBOOK' ID ':' <pb-when-block> <playbook-tail>
<playbook-tail>      ::= <pb-when-block> <playbook-tail>
                       |

<pb-when-block>      ::= 'WHEN' ID <opt-priority> <opt-temper> ':' <pb-when-body>

<opt-priority>       ::= <priority>
                       |
<priority>           ::= 'PRIORITY' NUMBER

<opt-temper>         ::= <temper>
                       |
<temper>             ::= 'TEMPER' <temper-entry> <temper-entry-tail> <opt-effects>
<temper-entry-tail>  ::= ',' <temper-entry> <temper-entry-tail>
                       |
<temper-entry>       ::= ID '(' FLOAT ')'

<opt-effects>        ::= <effects>
                       |
<effects>            ::= 'EFFECTS' <temper-entry> <temper-entry-tail>

<pb-when-body>       ::= <pb-body-item> <pb-body-item-tail> <opt-pb-else-branch>
<pb-body-item-tail>  ::= <pb-body-item> <pb-body-item-tail>
                       |
<pb-body-item>       ::= <pb-stmt>
                       | <pb-if-branch>
<pb-stmt>            ::= <do-stmt>
                       | <signal-stmt>

<pb-if-branch>       ::= 'IF' <condition> ':' <pb-stmt> <pb-stmt-tail>
<pb-stmt-tail>       ::= <pb-stmt> <pb-stmt-tail>
                       |

<opt-pb-else-branch> ::= <pb-else-branch>
                       |
<pb-else-branch>     ::= 'ELSE' ':' <pb-stmt> <pb-stmt-tail>
```

### Actions and signals

```
<do-stmt>        ::= 'DO' <action-name> <opt-arg-list> '.'
<signal-stmt>    ::= 'SIGNAL' ID <opt-arg-list> '.'

<action-name>    ::= ID
                   | 'TELL'
                   | 'BROADCAST'
                   | 'ACHIEVE'
                   | 'BELIEVE'
                   | 'FORGET'
                   | 'PRINT'

<opt-arg-list>   ::= <arg-list>
                   |
<arg-list>       ::= '(' <arg> <arg-tail> ')'
<arg-tail>       ::= ',' <arg> <arg-tail>
                   |
<arg>            ::= ID
                   | NUMBER
                   | STRING
```

## 4. Plots

```
<plot-def>          ::= 'PLOT' ID '.' <plot-header> <during-block> <during-block-tail>
<during-block-tail> ::= <during-block> <during-block-tail>
                      |

<plot-header>       ::= <header-item> <header-item-tail>
<header-item-tail>  ::= <header-item> <header-item-tail>
                      |
<header-item>       ::= <phase-decl>
                      | <role-decl>

<phase-decl>        ::= 'PHASE' ID <opt-initial> '.'
<opt-initial>       ::= 'INITIAL'
                      |
<role-decl>         ::= 'ROLE' ID '.'

<during-block>        ::= 'DURING' <during-target> ':' <during-content> <during-content-tail>
<during-content-tail> ::= <during-content> <during-content-tail>
                        |
<during-target>       ::= ID
                        | 'PLOT'

<during-content>    ::= <on-enter>
                      | <on-exit>
                      | <plot-when-block>



<on-enter>              ::= 'ON' 'ENTER' ':' <imperative-stmt> <imperative-stmt-tail>
<on-exit>               ::= 'ON' 'EXIT' ':' <imperative-stmt> <imperative-stmt-tail>
<imperative-stmt-tail>  ::= <imperative-stmt> <imperative-stmt-tail>
                          |
```

### Plot WHEN blocks

```
<plot-when-block>       ::= 'WHEN' ID <opt-priority> ':' <plot-when-body>
<plot-when-body>        ::= <plot-body-item> <plot-body-item-tail> <opt-plot-else-branch>
<plot-body-item-tail>   ::= <plot-body-item> <plot-body-item-tail>
                          |
<plot-body-item>        ::= <imperative-stmt>
                          | <plot-if-branch>

<plot-if-branch>        ::= 'IF' <condition> ':' <imperative-stmt> <imperative-stmt-tail>
<opt-plot-else-branch>  ::= <plot-else-branch>
                          |
<plot-else-branch>      ::= 'ELSE' ':' <imperative-stmt> <imperative-stmt-tail>
```

### Imperative statements

```
<imperative-stmt> ::= <assign-stmt>
                   | <unassign-stmt>
                   | <world-do-stmt>
                   | <role-do-stmt>

<assign-stmt>     ::= 'ASSIGN' ID 'TO' ID '.'
<unassign-stmt>   ::= 'UNASSIGN' ID 'FROM' ID '.'
<world-do-stmt>   ::= 'WORLD' 'DO' <action-name> <opt-arg-list> '.'
<role-do-stmt>    ::= ID 'DO' <action-name> <opt-arg-list> '.'
```

## 5. Conditions

```
<condition>          ::= <condition-and> <condition-or-tail>
<condition-or-tail>  ::= 'OR' <condition-and> <condition-or-tail>
                       |

<condition-and>      ::= <condition-atom> <condition-and-tail>
<condition-and-tail> ::= 'AND' <condition-atom> <condition-and-tail>
                       |

<condition-atom>     ::= 'NOT' <condition-atom>
                       | <fact-ref>
                       | '(' <condition> ')'

<fact-ref>           ::= ID
                       | ID '(' <arg> <arg-tail> ')'
```

## 6. Lexical terminals

```
ID          ::= [a-zA-Z_][a-zA-Z0-9_]*
NUMBER      ::= [0-9]+
FLOAT       ::= -?[0-9]+(\.[0-9]+)?
STRING      ::= "[^"]*"
```

Reserved words kept as named terminals: `SELF`, `ENVIRONMENT`,
`TELL`, `BROADCAST`, `ACHIEVE`, `BELIEVE`, `FORGET`, `PRINT`.

---