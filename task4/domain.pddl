(define (domain travel-planning)
  (:requirements :typing :action-costs)
  
  (:types
    location - object
  )
  
  (:predicates
    (at ?loc - location)
    (passed-security)
    (boarded)
  )
  
  (:functions
    (total-cost)
  )
  
  (:action take-taxi
    :parameters (?from ?to - location)
    :precondition (and 
                    (at ?from)
                    (= ?from home)
                    (= ?to airport)
                  )
    :effect (and 
              (not (at ?from))
              (at ?to)
              (increase (total-cost) 10) ; taxi is more expensive
            )
  )
  
  (:action take-bus-to-terminal
    :parameters (?from ?to - location)
    :precondition (and 
                    (at ?from)
                    (= ?from home)
                    (= ?to bus-terminal)
                  )
    :effect (and 
              (not (at ?from))
              (at ?to)
              (increase (total-cost) 1)
            )
  )
  
  (:action take-bus-to-airport
    :parameters (?from ?to - location)
    :precondition (and 
                    (at ?from)
                    (= ?from bus-terminal)
                    (= ?to airport)
                  )
    :effect (and 
              (not (at ?from))
              (at ?to)
              (increase (total-cost) 1)
            )
  )
  
  (:action walk-to-security
    :parameters (?from ?to - location)
    :precondition (and 
                    (at ?from)
                    (= ?from airport)
                    (= ?to security)
                  )
    :effect (and 
              (not (at ?from))
              (at ?to)
              (increase (total-cost) 1)
            )
  )
  
  (:action go-through-security
    :parameters (?from ?to - location)
    :precondition (and 
                    (at ?from)
                    (= ?from security)
                    (= ?to post-security)
                    (not (passed-security))
                  )
    :effect (and 
              (not (at ?from))
              (at ?to)
              (passed-security)
              (increase (total-cost) 1)
            )
  )
  
  (:action walk-to-gate
    :parameters (?from ?to - location)
    :precondition (and 
                    (at ?from)
                    (= ?from post-security)
                    (= ?to gate)
                    (passed-security)
                  )
    :effect (and 
              (not (at ?from))
              (at ?to)
              (increase (total-cost) 1)
            )
  )
  
  (:action board-flight
    :parameters (?loc - location)
    :precondition (and 
                    (at ?loc)
                    (= ?loc gate)
                    (passed-security)
                    (not (boarded))
                  )
    :effect (and 
              (boarded)
              (increase (total-cost) 1)
            )
  )
) 