grammar RegiaScript;

//  ──────────────────────────────────────────
//  PARSER RULES
//  ──────────────────────────────────────────

// each program is a set of story definitions, followed by the end of file
program
    : storyDef+ EOF
    ;

//  --- Story Definitions ---

// stories can be default or named ones. 
storyDef
    : defaultStory
    | namedStory
    ;

// default stories are used to give default behaviour to agents. 
// they do not have priority and cannot have phases.
defaultStory
    : DOC_COMMENT* STORY DEFAULT PERIOD duringBlock+
    ;

// named stories are used to represent quests and other narrative sections.
// they have a priority and can have phases.
namedStory
    : DOC_COMMENT* STORY ID PRIORITY NUMBER PERIOD
      declaration*
      phaseDecl*
      duringBlock+
    ;

//  --- Declarations ---

// declarations are used to define actions, events and conditions that can be used in the story.
declaration
    : DOC_COMMENT* actionDecl
    | DOC_COMMENT* eventDecl
    | DOC_COMMENT* conditionDecl
    ;

actionDecl
    : ACTION ID PERIOD
    ;

eventDecl
    : EVENT ID origin PERIOD
    ;

conditionDecl
    : CONDITION ID origin PERIOD
    ;

//  --- Origin Tag ---

// origin tags are used to specify the source of an event or condition.
origin
    : ENVIRONMENT
    | DIRECTOR
    | MYSELF
    | PLAYER
    | TIMER
    ;

//  --- Phase Declaration ---

// a phase is a subsection of a story that can have its own set of rules and behaviours.
phaseDecl
    : DOC_COMMENT* PHASE ID PERIOD
    ;

//  --- Agent Block ---

// agents are the characters or entities that participate in the story. 
// each agent block defines the behaviour of a specific agent within the story.
agentBlock
    : DOC_COMMENT* AGENT ID COLON agentSection*
    ;

//  --- Agent Section ---

// actions, events and conditions can be defined within an agent block
agentSection
    : DOC_COMMENT* actionDecl
    | DOC_COMMENT* eventDecl
    | DOC_COMMENT* conditionDecl
    | whenBlock
    ;

//  --- During Block ---

// during blocks represent the behaviour of an agent during a specific phase of the story.
duringBlock
    : DOC_COMMENT* DURING phaseRef COLON transitionRule* agentBlock+
    ;

transitionRule
    : DOC_COMMENT* TRANSITION TO phaseTarget WHEN ID origin
      (IF condExpr)? PERIOD
    ;

phaseTarget
    : ID
    | END
    ;

// the phase can be a named one or the default ALWAYS
phaseRef
    : ID
    | ALWAYS
    ;

//  --- When Block ---

// when blocks represent the reactions of an agent to specific events and conditions.
whenBlock
    : DOC_COMMENT* WHEN ID origin (IF condExpr)? COLON doSequence
    ;

//  --- Condition Expressions ---

// boolean grammar for conditions, supporting AND, OR and NOT operators, parentheses for grouping.
condExpr
    : condAnd (OR condAnd)*
    ;

condAnd
    : condTerm (AND condTerm)*
    ;

condTerm
    : NOT? condAtom
    ;

condAtom
    : ID origin
    | LPAREN condExpr RPAREN
    ;

//  --- Do Sequence ---

// actions that an agent performs in response to an event and condition.
doSequence
    : doAction (COMMA doAction)* PERIOD
    ;

doAction
    : DO BELIEVE ID
    | DO FORGET  ID
    | DO ID
    ;

//  ──────────────────────────────────────────
//  KEYWORDS
//  ──────────────────────────────────────────

STORY       : 'STORY'       ;
DEFAULT     : 'DEFAULT'     ;
PRIORITY    : 'PRIORITY'    ;
PHASE       : 'PHASE'       ;
AGENT       : 'AGENT'       ;
ACTION      : 'ACTION'      ;
EVENT       : 'EVENT'       ;
CONDITION   : 'CONDITION'   ;
DURING      : 'DURING'      ;
ALWAYS      : 'ALWAYS'      ;
WHEN        : 'WHEN'        ;
IF          : 'IF'          ;
AND         : 'AND'         ;
OR          : 'OR'          ;
NOT         : 'NOT'         ;
DO          : 'DO'          ;
BELIEVE     : 'BELIEVE'     ;
FORGET      : 'FORGET'      ;
ENVIRONMENT : 'ENVIRONMENT' ;
DIRECTOR    : 'DIRECTOR'    ;
MYSELF      : 'MYSELF'      ;
PLAYER      : 'PLAYER'      ;
TIMER       : 'TIMER'       ;
TRANSITION  : 'TRANSITION' ;
TO          : 'TO'         ;
END         : 'END'        ;

//  ──────────────────────────────────────────
//  PUNCTUATION
//  ──────────────────────────────────────────

PERIOD    : '.' ;
COLON     : ':' ;
COMMA     : ',' ;
LPAREN    : '(' ;
RPAREN    : ')' ;

//  ──────────────────────────────────────────
//  PRIMITIVES
//  ──────────────────────────────────────────

NUMBER    : [0-9]+ ;
ID        : [a-zA-Z_][a-zA-Z0-9_]* ;

//  ──────────────────────────────────────────
//  COMMENTS
//  ──────────────────────────────────────────

DOC_COMMENT : '#' [ \t]* '@' ~[\r\n]* ;
COMMENT     : '#' ~[\r\n]* -> skip ;
WS          : [ \t\r\n]+   -> skip ;