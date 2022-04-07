# TODO
Everything

- 'clean' main() by breaking into functions
    - Ex: master_draw(), set_Delta()/set_FPS(), etc

- good full screen

- use magic/duner for Vector class?

- delta time 
    - can use clock.tick_busy_loop(FPS)
    - however, tick_busy_loop will make sure actual_fps < FPS
    - so adding in a delta time to adjust for the slower fps is a good idea
