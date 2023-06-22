from manim import *

def play_sequence_in_background(scene, anims):
    current_anim = None
    mobj_updater = None
    def updater(dt):
        nonlocal current_anim, mobj_updater
        if (current_anim is None 
          or mobj_updater not in current_anim.mobject.updaters):
            if not anims:
                scene.remove_updater(updater)
                return            
            current_anim = anims.pop(0)
            scene.add(current_anim.mobject)
            turn_animation_into_updater(current_anim)
            mobj_updater = current_anim.mobject.updaters[-1]
    return updater

def join_all(scene, *updaters):
    def condition():
        return not (set(updaters) & set(scene.updaters))
    return condition