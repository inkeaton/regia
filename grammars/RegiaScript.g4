grammar RegiaScript;

///////////////////
//  PARSER RULES
///////////////////

program
    : declaration* duringBlock* EOF
    ;

//  --- Declarations ---

declaration
    : DOC_COMMENT* storyDecl
    | DOC_COMMENT* actionDecl
    | DOC_COMMENT* eventDecl
    | DOC_COMMENT* conditionDecl
    ;

storyDecl
    : STORY ID PRIORITY NUMBER PERIOD
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

origin
    : ENVIRONMENT
    | DIRECTOR
    | MYSELF
    ;

//  --- During Blocks ---

duringBlock
    : DOC_COMMENT* DURING storyRef COLON whenBlock+
    ;

storyRef
    : ID
    | ALWAYS
    ;

//  --- When Blocks ---

whenBlock
    : DOC_COMMENT* WHEN ID origin (IF condExpr)? COLON doSequence
    ;

//  --- Condition Expressions ---

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

//  --- Do Sequences ---

doSequence
    : doAction (COMMA doAction)* PERIOD
    ;

doAction
    : DO BELIEVE ID
    | DO FORGET  ID
    | DO ID
    ;

///////////////////
//  KEYWORDS
///////////////////

STORY       : 'STORY'       ;
ACTION      : 'ACTION'      ;
EVENT       : 'EVENT'       ;
CONDITION   : 'CONDITION'   ;
PRIORITY    : 'PRIORITY'    ;
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

///////////////////
//  PUNCTUATION
///////////////////

PERIOD    : '.' ;
COLON     : ':' ;
COMMA     : ',' ;
LPAREN    : '(' ;
RPAREN    : ')' ;

///////////////////
//  PRIMITIVES
///////////////////

NUMBER    : [0-9]+ ; // may need decimals?
ID        : [a-zA-Z_][a-zA-Z0-9_]* ;

///////////////////
//  IGNORED
///////////////////
DOC_COMMENT : '#' [ \t]* '@' ~[\r\n]* ;
COMMENT     : '#' ~[\r\n]* -> skip ;
WS          : [ \t\r\n]+   -> skip ;