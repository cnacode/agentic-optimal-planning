(define (problem travel-to-airport)
  (:domain travel-planning)
  
  (:objects
    home airport bus-terminal security post-security gate - location
  )
  
  (:init
    (at home)
    (= (total-cost) 0)
  )
  
  (:goal
    (boarded)
  )
  
  (:metric minimize (total-cost))
) 