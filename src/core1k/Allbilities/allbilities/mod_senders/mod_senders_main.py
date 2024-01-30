from ursina import *
from ursina import curve

class Jitter_Teleport_Curve:
    def __init__(self, 
        jitter_duration=1.0, 
        jump_duration=0.01, 
        end_duration=0.04,
        backward_jitter=-0.05,
        forward_jitter=0.01,
    ):
        
        self.combility_backward_jitter = backward_jitter
        self.forward_jitter = forward_jitter
        
        
        # Normalize the durations
        self.total = jitter_duration + jump_duration + end_duration
        self.jitter_duration = jitter_duration / self.total
        self.jump_duration = jump_duration / self.total
        self.end_duration = end_duration / self.total
        self.jitter_ended = False

    def __call__(self, t):
        t /= self.total  # normalize t to the duration
        if t < self.jitter_duration:
            ## Jitter back and forward, mostly back. 
            return self.combility_backward_jitter * t + self.forward_jitter * sin(10 * pi * t)
        else:
            if not self.jitter_ended:
                self.jitter_ended = True
                return 0.93
            else:
                # Use a square root function for the end phase
                end_t = (t - (self.jitter_duration + self.jump_duration)) / self.end_duration
                return 0.93 + 0.07 * (1 - sqrt(1 - min(end_t, 1)))


class Forces:
    def prepare_force(self, direction, energy_distance, type=None):
        type = 'impulse' if type is None else type

        if type not in ['impulse', 'teleport', 'blink']:
            raise ValueError(f'"{type}" is not a valid type for "add_force"')

        initial_direction_vec = self.calculate_user_passed_direction_vec(direction)

        if type == 'teleport':
            custom_curve = Jitter_Teleport_Curve(jitter_duration=0.5, jump_duration=0.01, end_duration=1.5)
            duration = 1.5
        else:
            if type == 'blink':
                custom_curve = curve.linear
                duration = 0.0
            elif type == 'impulse' or type == 'impulse_force':
                custom_curve = curve.out_expo
                duration = 0.3

        # Return the values that will be used as arguments for the use_force function
        return initial_direction_vec, energy_distance, custom_curve, duration, type

    def use_force(self, initial_direction_vec, energy_distance, custom_curve, duration, type):
        if self.get_real_eaat().parent.name == 'environment':
            return
        final_direction_vec = self.calculate_real_time_direction_vec_from_hit(initial_direction_vec)
        ignore_list = self.get_relevant_descendants(self.eaat)
        half_size_eaat = self.eaat.world_scale.x * 0.5

        if type == 'teleport':
            energy_distance = self.calculate_energy_dist_for_teleport_hit(final_direction_vec, energy_distance, ignore_list, half_size_eaat)
        else:
            energy_distance = self.calculate_energy_dist_from_hit(final_direction_vec, energy_distance, ignore_list, half_size_eaat)
        self.eaat.recieve_impulse(final_direction_vec, energy_distance, duration, custom_curve)
        
        ## TODO, REDO this section, too many repetitive if statements
        if type == 'teleport':
            Audio('teleport-90137.mp3', autoplay=True)

        elif type == 'blink':
            Audio('futuristic-smg-sound-effect-100378.mp3', autoplay=True)
            
        else:
            Audio('push_wind_whipy-woosh-transition-38006', autoplay=True)
        
