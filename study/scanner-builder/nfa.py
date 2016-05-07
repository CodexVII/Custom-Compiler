##--------------------------------------------------------------------------------------
##
## Class NFA represents a nondeterministic finite automaton.
##
## NFA itself is an abstract class.  Its subclasses, PrimitiveNFA, ChoiceNFA,
## CompositeNFA, ClosureNFA and OuterChoiceNFA do the work of generating NFAs.
## NFA inherits some of its functionality from base class FA.
##
##
## Fields are:
##
##    startState:  The first state in the NFA, a State object.
##
##    finalState:  The final state in the NFA, a State object.  N.B. this exists for
##                 NFAs generated by PrimitiveNFA, ChoiceNFA, CompositeNFA and
##                 ClosureNFA (i.e., the Thompson NFAs).  It doesn't exist in
##                 OuterChoiceNFA, which generates a non-Thompson NFA that may
##                 have multiple final states (this is used to represent "outer
##                 choices", where it may be desirable for the NFA to be able to
##                 recognise different categories of input, represented internally
##                 as a number of differnt Thompson machines linked by a common
##                 start state).  If this is an "OuterChoiceNFA", it has a list
##                 "finalStates", instead of "finalState".
##
##
##    regExpr:     The RE recognised by this NFA. N.B. this exists for
##                 NFAs generated by PrimitiveNFA, ChoiceNFA, CompositeNFA and
##                 ClosureNFA (i.e., the Thompson NFAs).  It doesn't exist in
##                 OuterChoiceNFA, which generates a non-Thompson NFA that may
##                 have multiple final states (this is used to represent "outer
##                 choices", where it may be desirable for the NFA to be able to
##                 recognise different categories of input, represented internally
##                 as a number of differnt Thompson machines linked by a common
##                 start state).  If this is an "OuterChoiceNFA", it has a list
##                 "regExprs", instead of "regExpr".
##
##     width:      The width of the graphical representation of this NFA in the
##                 internal millimetre-based co-ordinate system.
##                 The (implicit) assumption is that we are using a
##                 millimetre-based co-ordinate system (x across, y up), with states
##                 represented graphically as circles with diameter 10mm.
##                 The Python representation of a position is as a 2-tuple of
##                 integers, (x,y).
##
##     height:     The height of this NFA.
##
##     alphabet:   A set of characters: the input alphabet of this NFA.
##
##     stateCount: The number of states in this NFA.
##
##
## Most of the methods in the class are really only of concern in the construction
## of new NFAs from old ones, all the subclasses apart from PrimitiveNFA take NFA
## objects as inputs to their constructors and generate new NFAs from them.  The
## exceptions are the "output" methods, which write descriptions of the NFA to
## stdout in various formats:
##
##     output_plain()   A simple textual representation of the NFA.
##     output_dot()     The NFA described in a DOT-format.
##     output_table()   A tabular representation of the NFA.
##
## These methods are inherited from base class FA.  Also useful and
## inherited from FA is "listStates".
##
##
## One useful method provided by the NFA class is "scan".  This takes a string
## of characters and scans it according to the NFA.  It reports accept/reject and
## prints out information about the state sets travered by the automaton on
## scanning a string.  It essentially performs an "interpreted subset construction",
## i.e., building the state sets used by the NFA to DFA construction "on the fly"
##
## Examples of the use of scan:
##
##    >>> nfa=parseREs('abb (a|b)*abb')
##    >>> nfa.scan('abb')
##    Initial set of states (before any input read): [0, 1, 5, 6, 7, 8, 9]
##    (No current accepting state)
##
##    Reading 'a' moves automaton to state set [2, 6, 7, 8, 9, 10, 11, 14]
##    (No current accepting state)
##
##    Reading 'b' moves automaton to state set [3, 6, 7, 8, 9, 12, 13, 14]
##    (No current accepting state)
##
##    Reading 'b' moves automaton to state set [4, 6, 7, 8, 9, 12, 14, 15]
##    (Current accepting state(s) = [4, 15])
##
##    All input read: scanner halted
##    Final set of automaton states: [4, 6, 7, 8, 9, 12, 14, 15]
##    Accepting states are: [4, 15]
##    Machine accepts on state 4
##    All input accepted
##    >>> nfa.scan('abbaa')
##    Initial set of states (before any input read): [0, 1, 5, 6, 7, 8, 9]
##    (No current accepting state)
##
##    Reading 'a' moves automaton to state set [2, 6, 7, 8, 9, 10, 11, 14]
##    (No current accepting state)
##
##    Reading 'b' moves automaton to state set [3, 6, 7, 8, 9, 12, 13, 14]
##    (No current accepting state)
##
##    Reading 'b' moves automaton to state set [4, 6, 7, 8, 9, 12, 14, 15]
##    (Current accepting state(s) = [4, 15])
##
##    Reading 'a' moves automaton to state set [6, 7, 8, 9, 10, 11, 14]
##    (Current accepting state(s) = [4, 15]) , N.B., unchanged
##
##    Reading 'a' moves automaton to state set [6, 7, 8, 9, 10, 11, 14]
##    (Current accepting state(s) = [4, 15]) , N.B., unchanged
##
##    All input read: scanner halted
##    Final set of automaton states: [6, 7, 8, 9, 10, 11, 14]
##    Accepting states are: [4, 15]
##    Machine accepts on state 4
##    Accepting state is not in the final set of NFA states => some input ignored
##
##
## N.B., note one important point.  If an NFA object is created and subsequently
## used as an argument in the creation of another NFa, it is typically "junked"
## by that operation and cannot be meaningfully accessed thereafter.  This is
## because of the way in which the various object constructors work, changing
## the state numbers and positions of the states from the NFAs they employ to
## build a new NFA.  So, in general, once an NFA object is used as an argument
## in the construction of a new NFA object, it is "gone" and can't be
## re-used or accessed again (you can look at it, but the results generally
## won't be meaningful).  The moral of the story: use (display etc.) an
## NFA object *before* using it to build another. And also, don't be tempted
## to use the *same* NFA object twice in constructing a bigger NFA, the
## results will be junk.  The arguments to each NFA constructor *must*
## themselves be unique NFAs, with unique states.
##
## Internally each NFA is represented as a graph of State objects, accessable
## from its head via the "startState" instance variable.  Bigger NFAs
## reuse part of the graph in various ways, which is why argument NFAs get
## junked, they still have references to pieces of the State graph, but the
## constructors using them re-use (they don't copy) the underlying State
## graph and modify it at will, so the "startState" pointer of an argument
## NFA is not necessarily pointing at anything meaningful when the
## constructor is finished.
##
## N.B.  Method "listStates" is a useful way of examining all the states
## currently in the NFA.
##
##
from state import State
from connector import *
from fa import FA

class NFA(FA):
    "Base class representing NFA objects."

    def renumber(this,initialVal):
        "Re-label all the states in this NFA with consecutive numbers."
        number = initialVal
        stateQueue = [this.startState]
        visited = set([])
        while stateQueue != []:
            state = stateQueue.pop(0)
            if not state in visited:
                state.name = number
                visited.add(state)
                for successor in state.successors: stateQueue.append(successor[1])
                number += 1
        return number

    ## Translate an NFA around in the scene graph by dx and dy.  Used to reposition "element"
    ## NFAs when building a larger NFA.
    def repositionStates(this,dx,dy):
        "Change the location of all state objects in this NFA by a constant (dx,dy) amount."
        stateQueue = [this.startState]
        visited = set([])
        while stateQueue != []:
            state = stateQueue.pop(0)
            if not state in visited:
                state.position = (state.position[0]+dx,state.position[1]+dy)
                visited.add(state)
                for successor in state.successors: stateQueue.append(successor[1])

    ## Include output_dot method which supplies a default title
    ## to the superclass method output_dot(title).
    def output_dot(this):
        FA.output_dot(this,"NFA")

    ## Also include output_plain method supplying a default title and NFA
    ## type to the superclass (FA) method output_plain(title,fa_type).  Note
    ## that an NFA is assumed to be non-Thompson unless derived from a
    ## ThomsponNFA subclass, so reports nfa_type as "Non-Thompson" by default.
    def output_plain(this):
        FA.output_plain(this,"NFA","Non-Thompson NFA")


    ##-----------------------------------------------------------------------------------
    ##
    ##  scan:  An NFA-based (i.e., nondeterministic) scanner.  Works by building state
    ##         sets "on the fly".
    ##
    def scan(this,string):
        "Scan a string using the NFA."
        pos = 0
        inputChars = list(string)
        closure = this.epsilonClosure([this.startState])
        print "Initial set of states (before any input read):", this.getStateNames(closure)
        accepting_states = this.getAccepting(closure)
        if len(accepting_states) > 0:
            current_accepting_states = this.getStateNames(accepting_states)
            print "(Current accepting state(s) = %s)" % current_accepting_states
        else:
            current_accepting_states = []
            print "(No current accepting state)"
        while pos < len(inputChars):
            nextStates = this.nextStates(closure, inputChars[pos])
            closure = this.epsilonClosure(nextStates)
            accepting_states = this.getAccepting(closure)
            print "\nReading '%c' moves automaton to state set %s" %\
                  (inputChars[pos],this.getStateNames(closure))
            if len(accepting_states) > 0:
                current_accepting_states = this.getStateNames(accepting_states)
                changed = True
            else:
                changed = False
            if len(current_accepting_states) > 0:
                print "(Current accepting state(s) = %s)" % current_accepting_states,
                if changed:
                    print ""
                else:
                    print ", N.B., unchanged"
            else:
                print "(No current accepting state)"
            pos += 1

        print "\nAll input read: scanner halted"
        final_state_names = this.getStateNames(closure)
        print "Final set of automaton states:", final_state_names
        if len(current_accepting_states) == 0:
            print "No accepting state available: all input rejected."
        else:
            print "Accepting states are:", current_accepting_states
            print "Machine accepts on state", current_accepting_states[0]
            if current_accepting_states[0] in final_state_names:
                print "All input accepted"
            else:
                print "Accepting state is not in the final set of NFA states => some input ignored"

    ##
    ##  This is part of the NFA scanner: it constructs the epsilon closure of
    ##  a set of NFA states (represented as a list of State objects).
    ##
    def epsilonClosure(this, stateSet):
        "Close a set of NFA states."
        queue = stateSet[:]
        while len(queue) > 0:
            state = queue[0]
            queue = queue[1:]
            for s in state.successors:
                if s[0] == 'eps' and s[1].name not in stateSet:
                    stateSet.append(s[1])
                    queue.append(s[1])
        return stateSet

    ##
    ##  Also part of the NFA scanner.  It takes a state set (represented simply as
    ##  a list of State objects, and a character, and returns a list of State objects
    ##  representing all states reachable from the input set on the given character.
    ##
    def nextStates(this, stateSet, char):
        "See where a transition on a given character will take a set of NFA states."
        target = []
        for state in stateSet:
            for s in state.successors:
                if s[0] == char and s[1].name not in target: target.append(s[1])
        return target

    ##
    ##  Support routines for the NFA scanner.
    ##
    ##  getStateNames takes a list of NFA states (State objects) and returns a sorted
    ##  list of their names (since these are NFA states, this is a list of ints).
    ##
    def getStateNames(this, statelist):
        "Return a sorted list of state names in the list of states 'statelist'"
        names = [int(s.name) for s in statelist]
        names.sort()
        return names

    ##
    ##  getAccepting takes a list of NFA states (State objects) and returns a list
    ##  of all the States in the input that are accepting ones.  Does this by
    ##  checking that a state has no successors (length of its "successors" field
    ##  is zero).
    ##
    def getAccepting(this, statelist):
        "Return a list of the accepting states in statelist."
        accepting = []
        for s in statelist:
            if len(s.successors) == 0:  accepting.append(s)
        return accepting


##------------------------------------------------------------------------------
##
## Thompson NFA is a base-class for NFAs created using Thompson's
## construction.  This class is mainly used for type identification if needed.
##
## Note how method "showREcolumn" from base class FA (FA --> NFA --> ThompsonNFA)
## is overridden here to disable the display of regular expressions in tables
## generated from Thompson NFAs.
##
## A version of "output_plain" is also provided to invoke the RE version with
## appropriate parameters.
##

class ThompsonNFA(NFA):
    "Abstract class used to type Thompson NFAs."

    def showREcolumn(this):
        """Thompson NFA implementation of showREcolumn: returns False, meaning that tables
           should *not* display a column at their right-hand-sides with regular expressions
           associated with accepting states."""
        return False

    def output_plain(this):
        FA.output_plain(this,"NFA","Thompson NFA")


##------------------------------------------------------------------------------
##
## This represents an NFA with 2 states and a single transition on a character.
##
##                      ch
##                   0 ----> 1
##
## The result is a 2-state Thompson NFA.
##
## Use:   nfa=PrimitiveNFA('a')     ## Create a recogniser NFA for character 'a'
##

class PrimitiveNFA(ThompsonNFA):
    "Represents a primitive NFA (two states, single transition on 'ch'."
    def __init__(this,ch):
        assert isinstance(ch,str)
        this.startState = State(0,(5,5),None)
        this.finalStates = [State(1,(25,5),[])]
        this.startState.successors = [(ch,this.finalStates[0],
                                       Straight(this.startState,this.finalStates[0],ch))]
        this.width = 30
        this.height = 10
        this.alphabet = set([ch])
        this.stateCount = 2
        this.regExprs = [ch]
        this.rePrecedence = 30  ## RE precedence for formatting operations (highest).

##------------------------------------------------------------------------------
##
## This represents an NFA that allows a choice between two smaller NFAs.
##
##
## Use:   nfa1=PrimitiveNFA('a')
##        nfa2=PrimitiveNFA('b')
##        nfa3=ChoiceNFA(nfa1,nfa2)   ## nfa3 is a recogniser for (a|b).
##
## N.B. Once nfa3 is created, nfa1 and nfa2 are no longer useful, they will be
## modified in various ways by the construction of nfa3, and should not be
## accessed directly thereafter.  Thus, a better (safer) way to build a
## recogniser for (a|b) is:
##
##        nfa=ChoiceNFA(PrimitiveNFA('a'),PrimitiveNFA('b'))
##

class ChoiceNFA(ThompsonNFA):
    "Represents an NFA that allows nondeterministic choice between two more primitive NFAs."
    def __init__(this,nfa1,nfa2):
        assert isinstance(nfa1,ThompsonNFA) and isinstance(nfa2,ThompsonNFA)
        widthNFA1 = nfa1.width
        widthNFA2 = nfa2.width
        if widthNFA1 >= widthNFA2:
            dxNFA1 = 20
            dxNFA2 = 20 + (widthNFA1 - widthNFA2) / 2
            finalStateX = 35 + widthNFA1
            this.width = widthNFA1 + 40
        else:
            dxNFA1 = 20 + (widthNFA2 - widthNFA1) / 2
            dxNFA2 = 20
            finalStateX = 35 + widthNFA2
            this.width = widthNFA2 + 40
        this.height = nfa1.height + nfa2.height + 10
        dyNFA1 = 10 + nfa2.height
        nfa1.repositionStates(dxNFA1,dyNFA1)
        nfa2.repositionStates(dxNFA2,0)
        this.startState = State(0,(5,5+nfa2.height),[])
        this.finalStates = [State(1,(finalStateX,5+nfa2.height),[])]
        nfa1.finalStates[0].successors = \
            [(FA.EPS, this.finalStates[0], Straight(nfa1.finalStates[0],this.finalStates[0]))]
        nfa2.finalStates[0].successors = \
            [(FA.EPS, this.finalStates[0], Straight(nfa2.finalStates[0],this.finalStates[0]))]
        this.startState.successors = \
            [(FA.EPS, nfa1.startState, Straight(this.startState,nfa1.startState)),
             (FA.EPS, nfa2.startState, Straight(this.startState,nfa2.startState))]
        this.renumber(0)
        this.alphabet = nfa1.alphabet.union(nfa2.alphabet)
        this.alphabet.add(FA.EPS)
        this.stateCount = nfa1.stateCount + nfa2.stateCount + 2
        this.rePrecedence = 0  ## RE precedence for formatting operations (lowest).
        this.regExprs = ["%s|%s" % (nfa1.regExprs[0],nfa2.regExprs[0])]


##------------------------------------------------------------------------------
##
## This represents an NFA that concatenates two smaller NFAs by merging the
## final state of the first with the initial state of the second.
##
## Use:   nfa1=PrimitiveNFA('a')
##        nfa2=PrimitiveNFA('b')
##        nfa3=CompositeNFA(nfa1,nfa2)   ## nfa3 is a recogniser for (ab).
##
## N.B. Once nfa3 is created, nfa1 and nfa2 are no longer useful, they will be
## modified in various ways by the construction of nfa3, and should not be
## accessed directly thereafter.  Thus, a better (safer) way to build a
## recogniser for (ab) is:
##
##        nfa=CompositeNFA(PrimitiveNFA('a'),PrimitiveNFA('b'))
##

class CompositeNFA(ThompsonNFA):
    "Represents an NFA made by merging two others by state combining."
    def __init__(this,nfa1,nfa2):
        assert isinstance(nfa1,ThompsonNFA) and \
               isinstance(nfa2,ThompsonNFA)
        ## Align composite NFA on y's of final nfa1 and initial nfa2.
        dy = nfa1.finalStates[0].position[1] - nfa2.startState.position[1]
        if dy >= 0:   ## Move nfa2 up to align with nfa1
            nfa2.repositionStates(nfa1.width-10, dy)
            this.height = max(nfa1.height,nfa2.height+dy)
        else:         ## Move nfa1 up to align with nfa2
            dy = -dy
            nfa1.repositionStates(0, dy)
            nfa2.repositionStates(nfa1.width-10, 0)
            this.height = max(nfa1.height+dy,nfa2.height)
        this.width = nfa1.width + nfa2.width - 10
        nfa1.finalStates[0].successors = nfa2.startState.successors
        this.startState = nfa1.startState
        this.finalStates = nfa2.finalStates
        this.renumber(0)
        this.alphabet = nfa1.alphabet.union(nfa2.alphabet)
        this.stateCount = nfa1.stateCount + nfa2.stateCount - 1
        this.rePrecedence = 10 ## RE precedence for formatting operations.
        if nfa1.rePrecedence < 10: fmtStr = "(%s)"
        else: fmtStr = "%s"
        if nfa2.rePrecedence < 10: fmtStr += "(%s)"
        else: fmtStr += "%s"
        this.regExprs = [fmtStr % (nfa1.regExprs[0],nfa2.regExprs[0])]


##------------------------------------------------------------------------------
##
## This represents an NFA that recognises the Kleene closure of the regular
## expression recognised by its argument NFA.
##
## Use:   nfa1=PrimitiveNFA('a')
##        nfa2=ClosureNFA(nfa1,nfa2)   ## nfa2 is a recogniser for (a*).
##
## N.B. Once nfa2 is created, nfa1 and is no longer useful.  A better
## (safer) way to build a recogniser for (a*) is:
##
##        nfa=ClosureNFA(PrimitiveNFA('a'))
##
class ClosureNFA(ThompsonNFA):
    "The Kleene closure of an NFA."
    def __init__(this,nfa):
        assert isinstance(nfa,ThompsonNFA)
        nfa.repositionStates(20,10)
        this.width = nfa.width+40
        this.height = nfa.height+20
        this.startState = State(0,(5,nfa.startState.position[1]),None)
        this.finalStates = [State(1,(nfa.width+35,nfa.finalStates[0].position[1]),[])]
        this.startState.successors = \
            [(FA.EPS, nfa.startState, Straight(this.startState,nfa.startState)),
             (FA.EPS,this.finalStates[0], CurvedNFA(this.startState,this.finalStates[0],\
                                                    nfa.height+20))]
        nfa.finalStates[0].successors = \
            [(FA.EPS, this.finalStates[0], Straight(nfa.finalStates[0],this.finalStates[0])),\
             (FA.EPS, nfa.startState, CurvedNFA(nfa.finalStates[0],nfa.startState,0))]
        this.renumber(0)
        this.alphabet = nfa.alphabet
        this.alphabet.add(FA.EPS)
        this.stateCount = nfa.stateCount + 2
        this.rePrecedence = 20 ## RE precedence for formatting operations.
        if nfa.rePrecedence < 20: fmtStr = "(%s)*"
        else: fmtStr = "%s*"
        this.regExprs = [fmtStr % nfa.regExprs[0]]


##------------------------------------------------------------------------------
##
## This represents an NFA that allows an "outer choice" between the REs
## recognised by a list of argument NFAs.
##
## Use:   nfa1=PrimitiveNFA('a')
##        nfa2=PrimitiveNFA('b')
##        nfa3=PrimitiveNFA('c')
##        nfa4=OuterChoiceNFA([nfa1,nfa2,nfa3])   ## nfa4 is a recogniser for
##                                                ## (a|b|c).
##
## N.B. Once nfa4 is created, nfa1..3 are modified and no longer useful.
##
## So: what's the difference between an "Outer Choice" NFA and a normal
## Thompson NFA recognising (a|b|c)?
##
## First of all, this machine has 3 final states, whereas the Thomspon
## machine has only one; is is non-Thompson, so it can't be re-used in
## further NFA construction; and it is designed to allow the "branch"
## chosen by a specific input string to be recognised.  This is essentially
## how Lex and flex implement their "action statements", each different
## RE in a Lex/flex input becomes a different branch (with a different
## final state) in the NFA.  When this is translated by the subset
## construction into a DFA, the machine can use the NFA state set of the
## halting state of the machine to decide what action to take.  Note that
## if there are multiple NFA final states associated with the DFA halting
## state, the machine can decide between them using a simple priority
## scheme, typically the action associated with the lowest numbered
## NFA state is triggered.
##
class OuterChoiceNFA(NFA):
    "An 'Outer Choice' (non-Thompson) NFA merging a group of recognisers."
    def __init__(this,nfalist):
        assert isinstance(nfalist,list)
        nfa_count = len(nfalist)
        height = 0
        heights = nfa_count*[0]
        width = 0
        for i in range(nfa_count-1,-1,-1):
            assert isinstance(nfalist[i],ThompsonNFA)
            heights[i] = height
            height += (nfalist[i].height + 10)
            width = max(width,nfalist[i].width)
        this.height = height - 10
        this.width = width + 20
        this.startState=State(0,(5,(height-10)/2),nfa_count*[None])
        this.finalStates = nfa_count*[None]
        this.regExprs=nfa_count*[None]
        this.alphabet = set([])
        this.stateCount = 1
        statenum = 1
        for (i,nfa) in enumerate(nfalist):
            nfa.repositionStates(20,heights[i])
            statenum = nfa.renumber(statenum)
            this.startState.successors[i] = \
                (NFA.EPS,nfa.startState,Straight(this.startState,nfa.startState))
            this.finalStates[i] = nfa.finalStates[0]
            this.regExprs[i] = nfa.regExprs[0]
            this.alphabet.update(nfa.alphabet)
            this.stateCount += nfa.stateCount
        this.alphabet.add(FA.EPS)


##------------------------------------------------------------------------------
##
## End of NFA and subclass definitions.
##
##------------------------------------------------------------------------------

