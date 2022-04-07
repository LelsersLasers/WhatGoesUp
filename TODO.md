# TODO
Everything

Bugs:
- checkCollide() gives a false positive when self is below hb_other

- 'clean' main() by breaking into functions
    - Ex: master_draw(), set_Delta()/set_FPS(), etc

- good full screen
    - hold a 16:9 ratio
    - scale things based on screen size

- use magic/duner for Vector class?

- delta time 
    - can use clock.tick_busy_loop(FPS)
    - however, tick_busy_loop will make sure actual_fps < FPS
    - so adding in a delta time to adjust for the slower fps is a good idea
