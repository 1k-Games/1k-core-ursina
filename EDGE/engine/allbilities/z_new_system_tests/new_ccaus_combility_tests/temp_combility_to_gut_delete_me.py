


class Mod_Utility_Functions:
    ########################################
    #### ALL MOD UTILITY FUNCTIONS      ####
    ########################################

    class rotations:
        
        def calculate_rotation_from_direction(self, direction):
            # Convert the direction vector to a rotation
            rotation_y = -math.degrees(math.atan2(direction.x, direction.z))
            
            # Clamp direction.y to the range -1 to 1 to avoid math domain errors
            clamped_y = max(min(direction.y, 1), -1)
            rotation_x = -math.degrees(math.asin(clamped_y))

            # Ensure rotation_y is in the range [0, 360)
            if rotation_y < 0:
                rotation_y += 360

            return (rotation_x, rotation_y, 0)

        def calculate_user_passed_direction_vec(self, direction):
            direction_mapping = {
                "forward": Vec3(0, 0, 1),
                "push": Vec3(0, 0, 1),
                "back": Vec3(0, 0, -1),
                "backward": Vec3(0, 0, -1),
                "pull": Vec3(0, 0, -1),
                "left": Vec3(1, 0, 0),
                "right": Vec3(-1, 0, 0),
                "up": Vec3(0, 1, 0),
                "down": Vec3(0, -1, 0),
            }
            if isinstance(direction, str):
                direction = direction.lower()
                if direction not in direction_mapping:
                    raise ValueError(f"Invalid direction: {direction}")
                direction_vec = direction_mapping[direction]
            elif isinstance(direction, Vec3):
                direction_vec = direction
            else:
                raise TypeError("direction must be a string or a Vec3 instance")

            # Normalize, which means the Vector now has a total length of 1!!!
            direction_vec = direction_vec.normalized()
            return direction_vec
        
        def look_at_in_local_space(self, entity, target):
            target_position = target.world_position if isinstance(target, Entity) else Vec3(*target)
            entity.lookAt(scene, target_position)
        
        
    class distance:
        
        def last_vert_path_z_distance(self, vertices):
            first_vertex = vertices[0]
            farthest_vertex = max(vertices, key=lambda vertex: vertex[2])
            return abs(farthest_vertex[2] - first_vertex[2])
        
        
        def get_length_of_path(self, vertices, scale=1):
            '''
            - Used for calculating the overall distance that this path covers, and thus
            its energy usage
            - the same Max range on a curve/segmented line will be more energy than a straight line. 
            
            - need to add the calculation with the max range, unless that is already
            accounted for here. Actually it is not counted. 
                - It might be if I used self.path_raycast_ent.model.vertices, if not will have to calculate
                via the scale etc. 
                
            '''
            
            
            total_length = 0
            num_vertices = len(vertices)
            for i in range(num_vertices - 1):
                total_length += distance(vertices[i], vertices[i+1])
                # pt(vertices[i], vertices[i+1], total_length)
                
            return total_length * scale, num_vertices
        
        
    class descendants:
        
        def _get_descendants(self, entity, max_depth=15):
            if max_depth <= 0:
                pt(self.eaat)
                pt.ex()
                return []
            descendants = []
            for child in entity.children:
                descendants.append(child)
                descendants.extend(self._get_descendants(child, max_depth - 1))
            return descendants

        def get_relevant_descendants(self, entity):
            relevant_names = ['scene', 'enemies', 'local_objects', 'npcs', 'teammates']
            while entity.parent and entity.parent.name not in relevant_names:
                entity = entity.parent
            return [entity] + self._get_descendants(entity)
        
        
    class damage:
        def angle_between(self, u, v):
            dot_product = u.dot(v)
            magnitude_u = math.sqrt(u.dot(u))
            magnitude_v = math.sqrt(v.dot(v))

            cos_angle = dot_product / (magnitude_u * magnitude_v)
            cos_angle = max(min(cos_angle, 1), -1)
            angle = math.degrees(math.acos(cos_angle))
            
            return 180 - angle
        
        def calculate_adjusted_damage(self, damage):
            
            ## Vector from Center of Bubble shield to the hit point
            hit_vector = self.hit_info.world_point - self.hit_info.entity.world_position
            # pt(self.hit_info.world_normal, hit_vector)
            
            ## Angle between the projectile and the center of shield
            angle = self.angle_between(-self.hit_direction, hit_vector)
            
            ## Create a sweet spot for max damage. 
            if angle <= 12:
                return damage 
            
            #################################################
            # Damage calc - 
            #################################################
            #    return damage * (1 - (angle / 100) * 0.3)
            #       (angle /100) is just getting angle in decimal form. 
            #   return damage * (1 - (angle / 83) * 0.3)
            #       (angle/83) is getting something more accurate because thats about the max
            #       angle we can hit against the sphere ~ 83 degrees
            #   0.3: 
            #       (0.3) means that we can take away a maximum of 0.3 damage away, so 70% damage 
            #       minimum is counted at the extremes)
            #
            return damage * (1 - (angle / 83) * 0.3)
            #################################################
        
        def cause_damage(self, damage):
            if self.get_real_eaat().parent.name == 'environment':
                return
            if self.hit_info is not None:
                
                adjusted_damage = self.calculate_adjusted_damage(damage)
                
                self.eaat.recieve_damage(adjusted_damage, self.hit_info.world_point, self.hit_info.world_normal)
                pt(self.eaat.name, damage, adjusted_damage)
            else:
                
                self.eaat.recieve_damage(damage, self.eaat.world_position, self.eaat.forward)

        def _add_damage(self, dmg_amt):
            self.dmg_amt = dmg_amt
        
        
    class Raycast_Shooting:
        
        ###########
        # Raycast Shooting
        ###########
        def shoot(self):
            
            if self in self.path_target_types:
                self.eaat = self
                self.perform_actions()
            elif self.slot_owner in self.path_target_types:
                self.eaat = self.slot_owner.shield ## NOTE: Shield sends all functions to the EnergyBeing anyways, 
                                                    ## But now the owner will be treated exactly in the same logic 
                                                    ## as any other entity type of the target_types. 
                self.perform_actions()
            else:
                self._choose_ray_type()

        def _choose_ray_type(self):
            self.parent_targets_to_targeted_entities()
            self.traverse_target = getattr(self, "targeted_entities", None)

            path_raycast_ent = getattr(self, f"path_raycast_ent")
            raycast_vertices = getattr(self, f"path_raycast_vertices", [Vec3(0,0,0)])

            if len(raycast_vertices) == 2:
                self._straight_raycast(path_raycast_ent, raycast_vertices)
            else:
                self._segmented_linecast(path_raycast_ent, raycast_vertices)

        def _straight_raycast(self, path_raycast_ent, raycast_vertices):

            start_vertex = self.ccaus_barrel_end.world_position
            end_vertex = scene.getRelativePoint(path_raycast_ent, raycast_vertices[1])
            self._process_hit_info(start_vertex, end_vertex)

        def _segmented_linecast(self, path_raycast_ent, raycast_vertices):
            vertices = [self.world_position] + [scene.getRelativePoint(path_raycast_ent, vertex) for vertex in raycast_vertices]
            
            for i in range(len(vertices) - 1):
                hit_occurred = self._process_hit_info(vertices[i], vertices[i + 1], index=i)
                if hit_occurred:
                    break
                
        def _process_hit_info(self, start_vertex, end_vertex, index=1):
            # pt(start_vertex, end_vertex, index)
            
            hit_info = linecast(
                start_vertex, end_vertex,
                debug=True,
                debug_time=1,
                traverse_target=self.traverse_target,
                ignore=self.ignore_list)
            
            self.start_pos = start_vertex
            self.end_pos = end_vertex
            self.hit_direction = (self.start_pos - self.end_pos).normalized()
            
            return self.actions_if_hit(hit_info, index)
        
        def actions_if_hit(self, hit_info, index):
            if hit_info.hit:
                # pt.c('hit')
                
                self.hit_info = hit_info
                self.index_of_last_point_before_hit = index
                self.eaat = hit_info.entity
                self.perform_actions()
                
                return True  # Return True if a hit occurred
            
            return False  # Return False if no hit occurred
        
        
class Mod_Trajectories:
    from create_mesh_path import Mesh_Creator
    
    class Path:
        from ursina import curve


        def prepare_path(self):
            self.path_range()
            
        def path_range(self, range=1):
            self.path_range = range
            
        def path_speed(self, speed=inf):
            self.path_speed = speed
            
        def compile_path(self, range=1, rotation=(0,0,0)):
            self.path_range = range ## TODO, make the range actually set from the mod, not here. 
            
            visual_vertices_attr = f"path_visual_vertices"
            raycast_vertices_attr = f"path_raycast_vertices"
            
            visual_vertices = getattr(self, visual_vertices_attr, [Vec3(0,0,0)])
            raycast_vertices = getattr(self, raycast_vertices_attr, [Vec3(0,0,0)])
            
            if len(visual_vertices) == 1:
                visual_vertices.append(Vec3(visual_vertices[0]) + Vec3(0, 0, 1))
                raycast_vertices.append(Vec3(raycast_vertices[0]) + Vec3(0, 0, 1))
            # pt('compile', visual_vertices)
            
            setattr(self, visual_vertices_attr, visual_vertices)
            setattr(self, raycast_vertices_attr, raycast_vertices)
            
            z_dist = self.last_vert_path_z_distance(visual_vertices)
            z_scale = range / z_dist
            
            # visual_vertices = [v * z_scale for v in visual_vertices]
            # raycast_vertices = [v * z_scale for v in raycast_vertices]
            # pt(visual_vertices)
            
            
            
            
            num_sides = 4
            rotation_mesh = 45
            diameter=.5 / z_scale  ## Must divide the radius I want by the z_scale or else
                                    ## it'll get crazily stretched out. 
            
            new_vertices, triangles, new_uvs, new_normals = self.mesh_creator.create_mesh_data(
                visual_vertices, 
                num_sides=num_sides, 
                rotation=rotation_mesh,
                # diameter=0.025,
                diameter=diameter,
                interpolate=False,
                )
            visual_mesh = Mesh(vertices=new_vertices, triangles=triangles, uvs=new_uvs, normals=new_normals, mode='triangle')
            visual_ent = Entity(name='visual_ent',
                parent=self.ccaus_barrel_end, 
                model=visual_mesh, 
                color=Color(1,1,0,0.6))
            self.track_spawned_sub_entity(visual_ent)
            
            new_vertices, triangles, new_uvs, new_normals = self.mesh_creator.create_mesh_data(
                raycast_vertices,
                num_sides=num_sides,
                rotation=rotation_mesh,
                # diameter=0.025,
                diameter=diameter,
                interpolate=False,
                )
            path_mesh = Mesh(vertices=new_vertices, triangles=triangles, uvs=new_uvs, normals=new_normals, mode='triangle')
            path_raycast_ent = Entity(name='visual_ent',
                parent=self.ccaus_barrel_end, 
                model=path_mesh, 
                color=Color(1,0.647,0,0.6))
            self.track_spawned_sub_entity(path_raycast_ent)
            
            
            
            
            # visual_ent = Entity(name='visual_ent',
            #     parent=self.ccaus_barrel_end,
            #     model=Mesh(vertices=visual_vertices, mode='line', 
            #         thickness=33, 
            #         render_points_in_3d=False,
            #         ),
            #     color=color.rgba(1,1,0,.6))
            
            # path_raycast_ent = Entity(name='path_raycast_ent',
            #     parent=self.ccaus_barrel_end,
            #     model=Mesh(vertices=raycast_vertices, mode='line',
            #         thickness=4,
            #         render_points_in_3d=False
            #     ),
            #     color=color.rgba(1, .647, 0, .85))
            
            for entity in [visual_ent, path_raycast_ent]:
                entity.rotation = rotation
                entity.scale = z_scale

                
            setattr(self, f"path_visual_ent", visual_ent)
            setattr(self, f"path_raycast_ent", path_raycast_ent)
            
        def _extend_raycast_vertices(self, incoming_visual_vertices, incoming_raycast_vertices):
            """
            This method extends the path vertices for a given path type.

            Parameters:
            vertices (list): A list of vertices to extend the path.
            
            
            """
            
            visual_vertices_attr = f"path_visual_vertices"
            raycast_vertices_attr = f"path_raycast_vertices"


            ## Get vertices lists of paths
            ## If they don't exist, create them. 
            ## For example: self.path_visual_vertices = []
            visual_vertices = getattr(self, visual_vertices_attr, [Vec3(0,0,0)])
            raycast_vertices = getattr(self, raycast_vertices_attr, [Vec3(0,0,0)])
            # pt('_extend path 1', visual_vertices)
            
            
            ## extend
            visual_vertices.extend(incoming_visual_vertices)
            raycast_vertices.extend(incoming_raycast_vertices)
            # pt('_extend path 2', visual_vertices)
            
            # Set the visual and path vertices attributes of the object to the updated lists
            setattr(self, visual_vertices_attr, visual_vertices)
            setattr(self, raycast_vertices_attr, raycast_vertices)
            
            return visual_vertices, raycast_vertices
        
        def add_points_to_path(self, *vertices):
            # pt('add_points', vertices)
            
            self._extend_raycast_vertices(vertices, vertices)
        
        def add_curve_to_path(self, *args, **kwargs):
            # pt('add curve', curve)
            
            visual_curve_vertices, path_curve_vertices,  = self._create_curve(*args, **kwargs)
            
            self._extend_raycast_vertices(visual_curve_vertices, path_curve_vertices)
        
        def _create_curve(self, 
                scale=(1,1,1), 
                circle_degrees=360, 
                visual_resolution=22, 
                path_resolution=6,
                existing_visual_vertices=None, 
                existing_raycast_vertices=None,
        ):
            # pt(self.name, visual_resolution, path_resolution, existing_visual_vertices, existing_raycast_vertices)
            
            
            ## Normalize scale
            max_scale_value = max(scale)
            normalized_scale = Vec3(*tuple(s / max_scale_value for s in scale))

            ## Setup a circle with specified resolution
            circle_resolution = 56
            circle_points = [Vec3(0, math.sin(2 * math.pi * i / circle_resolution), -math.cos(2 * math.pi * i / circle_resolution)) for i in range(circle_resolution)]
            points_to_include = int(circle_resolution * (circle_degrees / 360)) + 1

            ## Create vertices for the mesh based on the included points
            visual_vertices = [v - Vec3(0, 0, -1) for v in circle_points[:points_to_include]]
            pt(visual_vertices)
            pt(visual_resolution)
            # pt.ex()
            ## Close the circle when circle_degrees is 360
            if circle_degrees == 360:
                visual_vertices.append(visual_vertices[0])

            ## Reduce the resolution of visual_vertices
            step_size = len(visual_vertices) / visual_resolution
            reduced_visual_vertices = [visual_vertices[int(i * step_size)] for i in range(visual_resolution - 1)]
            reduced_visual_vertices.append(visual_vertices[-1])
            visual_vertices = reduced_visual_vertices
            
            ## Create reduced vertices for raycasting based on reduced_visual_vertices
            raycast_vertices = visual_vertices[::len(visual_vertices) // path_resolution]

            ## If an existing user-created path exists, offset each new vertex
            ### by where the last vertex of the existing path is. So it starts correctly
            if existing_visual_vertices is not None and len(existing_visual_vertices) > 1:
                last_vertex = existing_visual_vertices[-1]
                visual_vertices = [v + last_vertex for v in visual_vertices]
                        
            if existing_raycast_vertices is not None and len(existing_raycast_vertices) > 1:
                last_vertex = existing_raycast_vertices[-1]
                raycast_vertices = [v + last_vertex for v in raycast_vertices]
                
            ## Scaled
            visual_vertices = [v * normalized_scale for v in visual_vertices]
            raycast_vertices = [v * normalized_scale for v in raycast_vertices]
        
            return visual_vertices, raycast_vertices ## Only for functions that need a curve but that don't get added to the path vertices
        
        def add_path_rotation(self, rotation=(0,0,0)):
            self.path_rotation = rotation
        
        
    class Speed:
        
        def add_speed(self, speed):
            self.speed = speed
        
        
    class Target_Types:
        
        
        ##################
        # Target Types
        ##################
        self.path_target_types = None     ## TODO These might not be necessary to initialize here
        
        
        ### TODO Instead of these being heavy entities:
        ###      Try my lightest or one of my lightest "light_entities" 
        ###     - Probably try to get rid of assistant targets
        ###     - Probably change the name to ""
        self.targeted_entities = Entity(name='targeted_entities') ## shooting raycasts/interceptions



        def add_target_types(self, general=None, specific=None):

            
            ''' Types of targets:  (aka set_target_types)
            - Any number of enemies/teammates/shields/npcs etc. 
            - Or:
                - self (this combility)
                - owner of the slot this combility is connected to.
                
                '''
            enemies, teammates, npcs, local_objects, environment = self.level_target_types 
            if general is None:
                general = {enemies, npcs, local_objects, environment}

            if self in general and len(general) > 1:
                raise ValueError("'this combility (self)' cannot coexist with other target types")
            if self.slot_owner in general and len(general) > 1:
                raise ValueError("'slot_owner' cannot coexist with other target types")
            
            setattr(self, f'path_target_types', general)
            # self.path_target_types = general
            
            ######################
            # specific targets
            ######################
            if specific is None:
                self.specific_target = "energy_being"
                setattr(self, f'path_target_types', general)
            elif specific in ["eb_body", "eb_shield"]:
                self.specific_target = specific
            
            ########
            # if any combination of the following is true: 
            # - ["eb_body", "eb_shield"]
            # - ["eb_shield", "eb_body"]
            # - ["eb_body", "eb_shield", "energy_being"]
            # - ["energy_being", "eb_body", "eb_shield"]
            # - etc.
            
            elif set(specific).issubset({"eb_body", "eb_shield", "energy_being"}):
                self.specific_target = "energy_being"
            else:
                raise ValueError(f'Specific type must be "energy_being", "eb_body", or "eb_shield". Not "{specific}"')
            ########################
            
            if self not in general and self.slot_owner not in general:
                self.parent_targets_to_targeted_entities()
            
            # pt(self.name, self.path_target_types, self.specific_target)
        
        def parent_targets_to_targeted_entities(self, debug=False):
            ''' 
            - This is happening in 20-35us depending on the amount of target_types, 
            - This is far faster than even a single extra linecast of 200-300us. 
            - This requires only one linecast to the self.targeted_entities '''
            
            if debug:
                pt.c('Deugging parent_targets_to_targeted_entities')
                target_types = getattr(self, f"path_target_types", [])
                targeted_entities_target_types = getattr(self, f"targeted_entities", None)
                pt(self.name, target_types, targeted_entities_target_types, targeted_entities_target_types.children)
                
            for target in getattr(self, f"path_target_types", []):
                target.parent = getattr(self, f"targeted_entities", None)
            
        def get_real_eaat(self):
            # pt(self.eaat, self.eaat.parent, self.eaat.parent.parent, self.eaat.parent.parent.parent)
            
            eaat = self.eaat ## local var For faster access
            
            ## Organized by likelyhood of being shot.
            if isinstance(eaat, Shield):
                
                # pt(eaat.parent.parent.parent)
                return eaat.parent.parent.parent
            elif eaat.parent.name == 'environment':
                
                return eaat
            elif isinstance(eaat, (EnergyBeing, EG_Object)):
                
                return eaat
            elif isinstance(e, Character):
                
                return eaat.parent
            elif isinstance(e, Core):
                
                return eaat.parent.parent
            else:
                
                return eaat
        
        
class Mod_Actions:
    ################################
    #        -Mod Actions          #
    ################################

    class Force:
        from ursina import curve


        def calculate_energy_dist_for_teleport_hit(self, initial_direction_vec, intial_energy_distance, ignore_list, half_size_eaat):
            original_world_position_eaat = self.eaat.world_position
            total_energy_distance = intial_energy_distance  # Initialize total_energy_distance with the initial energy amount
            energy_distance = intial_energy_distance
            attempt = 0
            while True:
                attempt +=1
                if attempt == 4:
                    self.eaat.world_position = original_world_position_eaat
                    pt('max teleportation bonus through geometry reached, cancelling telport')
                    return total_energy_distance
                destination = self.eaat.world_position + initial_direction_vec * energy_distance
                self.eaat.world_position = destination
                    
                hit_info = self.eaat.intersects(ignore=ignore_list)
                if hit_info.hit:
                    energy_distance += 1
                    total_energy_distance += energy_distance  # Increase the total_energy_distance by 1
                else:
                    forward_hit_info = raycast(self.eaat.world_position, 
                        initial_direction_vec, distance=200, ignore=ignore_list)
                    backward_hit_info = raycast(self.eaat.world_position, 
                        -initial_direction_vec, distance=energy_distance, ignore=ignore_list, debug=True)
                    if backward_hit_info.hit and forward_hit_info.hit and backward_hit_info.entity == forward_hit_info.entity:
                        energy_distance = forward_hit_info.distance
                    else:
                        self.eaat.world_position = original_world_position_eaat
                        break
                    
            return total_energy_distance
        
        def _calculate_energy_dist_from_hit(self, direction_vec, energy_amount, ignore_list, half_size_eaat):
            hit_info = raycast(self.eaat.world_position, direction_vec,
                            ignore=ignore_list,
                            distance=energy_amount + half_size_eaat, debug=True)
            if hit_info.hit:
                return distance(self.eaat.world_position, hit_info.world_point) - half_size_eaat
            return energy_amount

        def calculate_real_time_direction_vec_from_hit(self, direction_vec):
            if self.hit_info and self.hit_info.hit:
                forward = Vec3(-self.hit_direction)
                right = Vec3(forward.cross(Vec3(0, 1, 0)).normalized())
                up = Vec3(right.cross(forward).normalized())
                return direction_vec.x * right + direction_vec.y * up + direction_vec.z * forward
            else:
                return direction_vec.x * self.ccaus_barrel_end.right + direction_vec.y * self.ccaus_barrel_end.up + direction_vec.z * self.ccaus_barrel_end.forward

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
                energy_distance = self._calculate_energy_dist_from_hit(final_direction_vec, energy_distance, ignore_list, half_size_eaat)
            self.eaat.recieve_impulse(final_direction_vec, energy_distance, duration, custom_curve)
            
            ## TODO, REDO this section, too many repetitive if statements
            if type == 'teleport':
                Audio('teleport-90137.mp3', autoplay=True)

            elif type == 'blink':
                Audio('futuristic-smg-sound-effect-100378.mp3', autoplay=True)
                
            else:
                Audio('push_wind_whipy-woosh-transition-38006', autoplay=True)
        
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
                return self.combility_backward_jitter * t + self.forward_jitter * math.sin(10 * pi * t)
            else:
                if not self.jitter_ended:
                    self.jitter_ended = True
                    return 0.93
                else:
                    # Use a square root function for the end phase
                    end_t = (t - (self.jitter_duration + self.jump_duration)) / self.end_duration
                    return 0.93 + 0.07 * (1 - sqrt(1 - min(end_t, 1)))


    class demo_lasers:
        ###############################
        ## DON'T DELETE these!!!!
        ## THIS IS THE ORIGINAL ONE. THE ONE BENEATH WAS JUST FOR TESTING the visuals
        ###############################
        # def prepare_dmg_developer_laser(self, energy_amount=100):
        #     damage = energy_amount * 1
        #     return damage
        
        # def use_dmg_developer_laser(self, damage):
        #     '''Testing laser for developers only. 
            
        #     - 1:1 ratio of damage to energy '''
        #     self.cause_damage(damage)
            
        #     self.projectile_visual_ent.texture = 'laser_white_kisspng-light-special-effects-photoscape-transparency-and-color-light-effect-5aae700a43a5c7.2554474615213813862771' 
        #     self.projectile_visual_ent.color = color.red
            
        #     self.projectile_path_raycast_ent.texture = 'laser_white_kisspng-light-special-effects-photoscape-transparency-and-color-light-effect-5aae700a43a5c7.2554474615213813862771' 
        #     self.projectile_path_raycast_ent.color = color.yellow
        #     laser_sound = Audio('laser_pulse_lazerius-139178', autoplay=True)

        ######################################
        ## TEMP - CREATED FOR TESTING VISUALS/AUDIO
        ######################################
        def prepare_dmg_developer_laser(self, energy_amount=100):
            damage = energy_amount * 1
            self.dmg_dev_laser_offset = 0
            return damage
        
        def use_dmg_developer_laser(self, damage):
            '''Testing laser for developers only. 

            - 1:1 ratio of damage to energy '''
            self.cause_damage(damage)

            original_texture = self.projectile_visual_ent.texture
            original_color = self.projectile_visual_ent.color
            original_texture_offset = self.projectile_visual_ent.texture_offset

            self.projectile_visual_ent.texture = 'laser_white_kisspng-light-special-effects-photoscape-transparency-and-color-light-effect-5aae700a43a5c7.2554474615213813862771' 
            self.projectile_visual_ent.color = color.red

            self.projectile_path_raycast_ent.texture = 'laser_white_kisspng-light-special-effects-photoscape-transparency-and-color-light-effect-5aae700a43a5c7.2554474615213813862771' 
            self.projectile_path_raycast_ent.color = color.yellow
            laser_sound = Audio('laser_pulse_lazerius-139178', autoplay=True)

            # Animate the texture offset for half a second
            for i in range(35):  # 10 steps in the animation
                invoke(self.animate_texture_offset, delay=i*0.05)  # 0.05 seconds delay between each step

            # Return to the original colors, textures, and texture offset after half a second
            invoke(self.reset_visuals, original_texture, original_color, original_texture_offset, delay=0.5)

        def animate_texture_offset(self):
            self.dmg_dev_laser_offset += time.dt * -11
            self.projectile_visual_ent.texture_offset = (self.dmg_dev_laser_offset*0.2, self.dmg_dev_laser_offset)
            self.projectile_path_raycast_ent.texture_offset = (self.dmg_dev_laser_offset*0.1, self.dmg_dev_laser_offset)

        def reset_visuals(self, original_texture, original_color, original_texture_offset):
            self.projectile_visual_ent.texture = original_texture
            self.projectile_visual_ent.color = original_color
            self.projectile_visual_ent.texture_offset = original_texture_offset
            self.projectile_path_raycast_ent.texture = original_texture
            self.projectile_path_raycast_ent.color = original_color
        
        
    class experimental_points:
        def prepare_experimental_animation_points(self, 
            range=20, 
            speed=105, 
            scale=(1,.4,1), 
            circle_degrees=180, 
            rotation=(0,0,0),
            ):
            '''
            - This is a blank slate for acquiring points, and then sending them 
            to be animated by the target type of the slot_owner (for now). 
            - Originally designed for the dash with the slot_owner. In this
            simplified state, it will be much easier to build other classes from
            this one. 
            '''
            
            self.add_curve_to_path(
                scale=scale, 
                circle_degrees=circle_degrees, 
                )
            
            self.compile_path(
                range, 
                rotation,
                )
            
            dist_of_visual_vertices, num_vertices_path = self.get_length_of_path(
                self.animation_path_raycast_ent.model.vertices, scale=range)

            duration = dist_of_visual_vertices / speed 

            curve_points = [Vec3(self.world_position)] + [
                Vec3(scene.getRelativePoint(self.animation_visual_ent, vertex)) 
                for vertex in self.animation_visual_vertices]

            direction_vec = Vec3(0,0,1)

            return duration, curve_points, direction_vec

        def use_experimental_animation_points(self, duration, curve_points, direction_vec):
            self.eaat._experimental_recieve_animation_points(direction_vec, duration, curve_points)
        
        
    class camera:
            
        def _set_camera_parent_properties(self, world_rotation=None):
            self.cam_ent = self.slot_owner.cam_mount_main_ent
            self.cam_ent_orig_pos = self.cam_ent.position 
            self.cam_ent_original_rot = self.cam_ent.rotation
            # cam_ent.parent = scene
            # cam_ent.world_position = self.hit_info.world_point
            # cam_ent.look_at(self)
                
            #########
            ## Slot Owner
            #########
            if self.slot_owner in self.path_target_types:
                self.cam_ent.parent = self.slot_owner
                self.cam_ent.position = self.slot_owner.cam_mount_main_default_pos
                
            #########
            ## Everything Else
            #########
            else:
        
                ## POSSIBLE BUG: By checking if self.hit_info and never resetting it to None (as of right now, hit_info never resets to None, then we might have a hit_info
                ## even though we are about to apply this weapon to a self.this_combility or something.
                ## Maybe... We can actually set the hit_info information to the slot_owner or this_combility? I could manually do it, but it wouldn't have a normal, right? 
                ## I'm not really sure at this point. But some ideas to keep in mind. )
                if self.hit_info:
                    ## NOTE: We look at the self (this combility), so we always look the direction that the camera was shot in,
                    ## Whether the camera was attached/separated from the slot_owner at the time. 
                    self.cam_ent.parent = scene
                    self.cam_ent.world_position = self.hit_info.world_point
                    self.cam_ent.look_at(self)
                
                #########
                ## Self (This Combility):
                else:
                    self.cam_ent.parent = self.eaat
                    self.cam_ent.world_position = self.eaat.world_position
                    self.cam_ent.rotation = self.eaat.rotation
                    eaat_scale = self.eaat.scale
                    counter_scale = [1/s for s in eaat_scale]
                    
                    self.cam_ent.scale = counter_scale
                    self.cam_ent.world_scale = 1
                    
            if world_rotation is not None:
                self.cam_ent.world_rotation = world_rotation
        
        def _unset_camera_parent_properties(self):
            self.cam_ent = self.slot_owner.cam_mount_main_ent

            self.cam_ent.parent = self.slot_owner
            
            self.cam_ent.position = self.slot_owner.cam_mount_main_default_pos

            self.cam_ent.rotation = (0,0,0)
            
            # pt(self.cam_ent.scale, self.cam_ent.world_scale)
            
            self.cam_ent.world_scale = 1
            
            window.render_mode = 'default'
            
        def _set_camera_render_properties(self, render_mode='default'):
            window.render_mode = render_mode        
            
        def _set_camera_properties(self, render_mode, world_rotation=None):
            self._set_camera_parent_properties(world_rotation)
            self._set_camera_render_properties(render_mode)
        
        def _unset_camera_properties(self):
            self._unset_camera_parent_properties()
            
            window.render_mode = 'default'
            camera.fov = self.default_camera_fov
            
        def _set_entity_colors(self, entity_color_category):
            ent_color_attr = f"entity_{entity_color_category}_colors"
            entity_colors = getattr(self, ent_color_attr)
            for entity, color in entity_colors.items():
                entity.color = color
            
        def _generate_entity_colors(self, entity_color_category='original', default_color=None, **kwargs):
            entity_colors_attr = f"entity_{entity_color_category}_colors"
            setattr(self, entity_colors_attr, {})

            # First, set the colors of the entities specified in kwargs
            for entity_set_name, color in kwargs.items():
                entity_set = EG_Globals.entity_sets.get(entity_set_name)
                if entity_set is not None:
                    for entity in entity_set:
                        if hasattr(entity, 'color'):
                            getattr(self, entity_colors_attr)[entity] = color

            # Then, set the colors of the remaining entities to the default color
            for entity_set_name, entity_set in EG_Globals.entity_sets.items():
                for entity in entity_set:
                    if entity not in getattr(self, entity_colors_attr) and hasattr(entity, 'color'):
                        if entity_color_category == 'original':
                            getattr(self, entity_colors_attr)[entity] = entity.color
                        elif default_color is not None:
                            getattr(self, entity_colors_attr)[entity] = default_color
                        else:
                            getattr(self, entity_colors_attr)[entity] = entity.color
        
        def prepare_camera_night_vision(self, 
            color=Color(0, .25, 0, 1), ## Low Light Green
            energy_amount=121,
            **kwargs
        ):
            
            self._prepare_camera_colors(
                entity_color_category='camera',
                default_color=color,
                shields=Color(0,0,0,0),
                shield_parts=Color(0,0,0,0),
                shield_part2s=Color(0,0,0,0),
                sky=Color(0, 0, 0, 0)
            )
        
        def use_camera_night_vision(self):
            self._set_camera_properties('default')
            self._set_entity_colors(entity_color_category='camera')

        def disable_camera_night_vision(self):
            self._unset_camera_properties()    
            self._set_entity_colors(entity_color_category='original')
        
        def prepare_camera_bw_beings(self,
            color=Color(0.25, 0.25, 0.25, 1), ## Low light Red
            energy_amount=121,
            **kwargs
        ):

            self._prepare_camera_colors(
                entity_color_category='camera',
                characters=color,
            )
        
        def use_camera_bw_beings(self):
            self._set_camera_properties('default')
            self._set_entity_colors(entity_color_category='camera')

        def disable_camera_bw_beings(self):
            self._unset_camera_properties()    
            self._set_entity_colors(entity_color_category='original')
            
        def prepare_camera_bw_non_beings(self, 
            color=Color(0.25, 0.25, 0.25, 1), ## Low light Red
            energy_amount=121,
            **kwargs
        ):

            self._prepare_camera_colors(
                entity_color_category='camera',
                default_color=color,
                enemy_characters=(1,0,0,1),
                teammate_characters=(0,0,1,1),
                npc_characters=(1,1,0,1),
            )
        
        def use_camera_bw_non_beings(self):
            self._set_camera_properties('default')
            self._set_entity_colors(entity_color_category='camera')

        def disable_camera_bw_non_beings(self):
            self._unset_camera_properties()    
            self._set_entity_colors(entity_color_category='original')
            
        def prepare_camera_thermal_vision(self, 
            color=Color(0.25, 0, 0, 1), ## Low light Red
            energy_amount=121,
            **kwargs
        ):
            # c = color*2.5
            # s = color*.8
            # pt(c,s)
            r,g,b,a = color
            shields_color = (r*4.5, g*4.5, b*4.5, a*1.75)
            self._prepare_camera_colors(
                entity_color_category='camera',
                default_color=color,
                characters=color*1.25,
                cores=color*5.5,
                shields=shields_color,
                shield_parts=Color(0,0,0,0),
                shield_part2s=Color(0,0,0,0),
                sky=Color(0, 0, 0, 0)
            )
        
        def use_camera_thermal_vision(self):
            self._set_camera_properties('default')
            self._set_entity_colors(entity_color_category='camera')

        def disable_camera_thermal_vision(self):
            self._unset_camera_properties()    
            self._set_entity_colors(entity_color_category='original')
            
        def prepare_camera_x_ray(self, 
            mode='grey',
            energy_amount=121,
            **kwargs
        ):
            core_color = Color(0.5, 0.5, 0.5, 0.95)
            slots_color = Color(0.5,0.5,0.5,0.95)
            sky_color = Color(0, 0, 0, 0)

            if mode == 'colors':
                enemy_characters = Color(1, 0, 0, 0.1)
                teammate_characters = Color(0, 0, 1, 0.1)
                npc_characters = Color(1, 1, 0, 0.1)
                
                self._prepare_camera_colors(
                    entity_color_category='camera',
                    default_color=Color(0.5, 0.5, 0.5, 0.1),
                    enemy_characters=enemy_characters,
                    teammate_characters=teammate_characters,
                    npc_characters=npc_characters,
                    cores=core_color,
                    slots=slots_color,
                    sky=sky_color
                )
            else:
                self._prepare_camera_colors(
                    entity_color_category='camera',
                    default_color=Color(0.5, 0.5, 0.5, 0.1),
                    cores=core_color,
                    slots=slots_color,
                    sky=sky_color
                )

        def _prepare_camera_colors(self, entity_color_category, **kwargs):
            self._generate_entity_colors(entity_color_category='original')
            self._generate_entity_colors(entity_color_category, **kwargs)
        
        def use_camera_x_ray(self):
            self._set_camera_properties('default')
            self._set_entity_colors(entity_color_category='camera')
            
        def disable_camera_x_ray(self):
            self._unset_camera_properties()    
            self._set_entity_colors(entity_color_category='original')
            
        def use_camera_visual(self):
            self._set_camera_properties('default')
            
        def disable_camera_visual(self):
            # pt.c(' disable cam visual')
            self._unset_camera_properties()
            
        def use_camera_electro_magnetic(self):
            self._set_camera_properties('normals')
        
        def disable_camera_electro_magnetic(self):
            # pt.c(' disable cam electro magnetic')
            self._unset_camera_properties()
            
        def use_camera_prop_zoom(self, fov=90):
            camera.fov = max(3, min(179, fov))
            
        def disable_camera_prop_zoom(self):
            self._unset_camera_properties()

        def prepare_camera_prop_zooming_incremental(self, fov_step=5, step_timing=0.05, energy_amount=100):
            self.start_step_time = time.time() ## NOTE: I'm not sure if time.time() is appropriate here, or if I should
                                                ## be using some ursina equivalent
            
        def use_camera_prop_zooming_incremental(self, fov_step=5, step_timing=0.05):
            if time.time() - self.start_step_time <= step_timing:
                return

            camera.fov = max(2, min(179, camera.fov + fov_step))
            
        def disable_camera_prop_zooming_incremental(self):
            self._unset_camera_properties()
        
        
    class camera_pip_rtt:
            
        from panda3d.core import Camera
        
        def use_camera_prop_resolution(self, resolution=(128, 128)):
            '''    TODO - Not currently working
                Change Game Resolution, independent of the window size
            '''
            if hasattr(self, 'rtt_display'):
                ...
            
            self.rtt_buffer = app.win.makeTextureBuffer("rtt buffer", 
                resolution[0], resolution[1]
                )

            ## Camera
            self.rtt_camera = app.makeCamera(self.rtt_buffer)
            self.rtt_camera.node().getLens().setFov(90)
            self.rtt_camera.reparentTo(self.slot_owner)
            # camera.clip_far = 11

            ## Display
            self.rtt_display = Entity(model='quad', scale=2, position=(0, 0, 0.5))
            self.rtt_display.parent = camera.ui
            self.rtt_display.texture = Texture(self.rtt_buffer.getTexture())
            
        def disable_camera_prop_resolution(self):
            self._unset_camera_properties
            
        def use_camera_pip(self, cam_parent=None, position=Vec3(0,0,0), rotation=Vec3(0,0,0), energy_amount=100):
            
            if hasattr(self, 'pip_display_region'):
                self.ursina_window.removeDisplayRegion(self.pip_display_region)
                self.camera_2.removeNode()
                
            ## Ursina's main display region
            self.main_display_region = app.camNode.getDisplayRegion(0)
            # self.main_display_region.setDimensions(0, 1, 0, 1)
            # self.main_display_region.setSort(0)
            self.ursina_window = self.main_display_region.getWindow()
            
            ## secondary display region & camera
            self.camera_node_2 = Camera('CameraNode2')
            self.camera_2 = scene.attachNewNode(self.camera_node_2)
            self.camera_2.node().getLens(0).setFar(11333)
            # self.camera_2.node().getLens(0).setFar(13444)
            
            # self.camera_2.setPos(camera.getPos() + Vec3(0, 0, 0))
            if cam_parent is not None:
                self.camera_2.reparent_to(cam_parent)
            else:
                self.camera_2.reparent_to(camera)
                
            self.camera_2.setPos(position)
            self.camera_2.setHpr(rotation)
            
            self.pip_display_region = self.ursina_window.makeDisplayRegion(0.4, 0.6, 0.78, 0.98)
            self.pip_display_region.setCamera(self.camera_2)
            self.pip_display_region.setSort(22)
            
            
            
            # main_camera_fov = app.camLens.getFov()
            # camera_2_fov = camera_node_2.getLens().getFov()
            # pt(main_camera_fov, camera_2_fov)
            # # camera_node_2.getLens().setFov(main_camera_fov)

            # aspect_ratio = window.size[0] / window.size[1]  # Get the aspect ratio of the window
            # pt(aspect_ratio)
            # fov = app.camLens.getFov()  # Get the current field of view
            # new_fov = (fov[0], fov[0] / aspect_ratio)  # Calculate the new field of view
            # pt(fov, new_fov)
            # app.camLens.setFov(new_fov)  # Set the new field of view

        def disable_camera_pip(self):
            # self.pip_display_region.setActive(False)
            # self.ursina_window.removeDisplayRegion(self.pip_display_region)
            # self.camera_2.removeNode()
            # pt('disable camera pip')
            if hasattr(self, 'pip_display_region'):
                self.ursina_window.removeDisplayRegion(self.pip_display_region)
                self.camera_2.removeNode()

        def use_camera_rtt(self, cam_parent=camera, position=Vec3(0,0,0), rotation=Vec3(0,0,0), energy_amount=100):
            ''' Render to Texture, main scene objects'''
            if hasattr(self, 'rtt_display'):
                ...
            

            self.rtt_buffer = app.win.makeTextureBuffer("rtt buffer", 512, 512)

            ## Camera
            self.rtt_camera = app.makeCamera(self.rtt_buffer)
            self.rtt_camera.node().getLens().setFov(90)
            self.rtt_camera.reparentTo(scene)
                
            self.rtt_camera.setPos(position)
            self.rtt_camera.setHpr(rotation)


            ## Display
            self.rtt_display = Entity(model='quad', scale=2, position=(2, 0, 3))
            self.rtt_display.parent = camera
            self.rtt_display.texture = Texture(self.rtt_buffer.getTexture())

            # if cam_parent is not None:
            #     self.rtt_display.reparent_to(camera)

        def disable_camera_rtt(self):
            if hasattr(self, 'rtt_display'):
                self.rtt_display.enabled = False
                # self.rtt_display = None

            if hasattr(self, 'rtt_camera'):
                self.rtt_buffer.removeNode()
                # self.rtt_buffer = None

            if hasattr(self, 'rtt_render'):
                self.rtt_render.removeNode()
                # self.rtt_render = None

            if hasattr(self, 'rtt_buffer'):
                app.graphicsEngine.removeWindow(self.rtt_buffer)
                # self.rtt_buffer = None

        def use_camera_rtt_specific_objects(self, cam_parent=camera, position=Vec3(0,0,0), rotation=Vec3(0,0,0), energy_amount=100):
            ''' Render to Texture, render specific objects only (like your avatar or map stuff etc.)
            TODO - make a test for this, choose combility slot owner as target or something
            
            '''
            
            if hasattr(self, 'rtt_display'):
                ...
            

            self.rtt_buffer = app.win.makeTextureBuffer("rtt buffer", 512, 512)
            self.rtt_render = NodePath("rtt render")

            ## Camera
            self.rtt_camera = app.makeCamera(self.rtt_buffer)
            self.rtt_camera.node().getLens().setFov(90)
            self.rtt_camera.reparentTo(self.rtt_render)
                
            self.rtt_camera.setPos(position)
            self.rtt_camera.setHpr(rotation)


            ## Display
            self.rtt_display = Entity(model='quad', scale=2, position=(2, 0, 3))
            self.rtt_display.parent = camera
            self.rtt_display.texture = Texture(self.rtt_buffer.getTexture())

            # if cam_parent is not None:
            #     self.rtt_display.reparent_to(camera)

        def disable_camera_rtt_specific_objects(self):
            if hasattr(self, 'rtt_display'):
                self.rtt_display.enabled = False
                # self.rtt_display = None

            if hasattr(self, 'rtt_camera'):
                self.rtt_buffer.removeNode()
                # self.rtt_buffer = None

            if hasattr(self, 'rtt_render'):
                self.rtt_render.removeNode()
                # self.rtt_render = None

            if hasattr(self, 'rtt_buffer'):
                app.graphicsEngine.removeWindow(self.rtt_buffer)
                # self.rtt_buffer = None


        def use_create_pip(self, 
            pip_name=None, 
            camera_name=None,
            position=Vec3(0,0,0), 
            rotation=Vec3(0,0,0), 
            corner_positions=(0.4, 0.6, 0.78, 0.98), 
            energy_amount=111
        ):
            main_display_region = app.camNode.getDisplayRegion(0)
            main_camera = main_display_region.getCamera()
            self.ursina_window = main_display_region.getWindow()

            num_regions = self.ursina_window.getNumDisplayRegions()
            generated_name = f'pip_display_region_{num_regions}'

            pip_display_region = self.ursina_window.makeDisplayRegion(
                corner_positions[0], corner_positions[1], corner_positions[2], corner_positions[3]
            )
            pip_display_region.setSort(22)

            # If no camera_name is given or if the camera_name is not found, 
            # use the last created camera or the default Ursina camera
            if camera_name is None or not hasattr(self, camera_name):
                if self.cameras:
                    camera_to_use = self.cameras[-1]
                else:
                    camera_to_use = main_camera
            else:
                potential_camera = getattr(self, camera_name)
                if isinstance(potential_camera, Camera):
                    camera_to_use = potential_camera
                else:
                    raise ValueError(f"{camera_name} is not a valid Camera object")

            pip_display_region.setCamera(camera_to_use)


            # Store the pip_name with the associated display region in the dictionary
            pip_name = generated_name if pip_name is None else pip_name
            Combility.pip_regions[pip_name] = pip_display_region
            
            # setattr(self, pip_name, pip_display_region)

        def disable_create_pip(self, pip_name):
            pip_region = Combility.pip_regions.get(pip_name)

            if pip_region is not None:
                self.ursina_window.removeDisplayRegion(pip_region)
                del Combility.pip_regions[pip_name]

        def use_new_camera(self,
            cam_parent=None,
            rtt_name=None,
            pip_name=None,
            camera_name=None,
            position=Vec3(0,0,0), rotation=Vec3(0,0,0), 
            resolution=(512, 512),
            energy_amount=100):

            # Try to find the rtt display region first
            display_region = None
            if rtt_name is not None:
                display_region = Combility.rtt_regions.get(rtt_name)

            # If no rtt display region found, try to find the pip display region
            if display_region is None and pip_name is not None:
                display_region = Combility.pip_regions.get(pip_name)

            # If no display region found, default to the last rtt or pip
            if display_region is None:
                if Combility.rtt_regions:
                    display_region = list(Combility.rtt_regions.values())[-1]
                    rtt_name = list(Combility.rtt_regions.keys())[-1]
                elif Combility.pip_regions:
                    display_region = list(Combility.pip_regions.values())[-1]
                    pip_name = list(Combility.pip_regions.keys())[-1]
                else:
                    raise ValueError('No display region found')

            ## secondary display region & camera
            self.camera_node_2 = Camera('CameraNode2')
            self.camera_2 = scene.attachNewNode(self.camera_node_2)
            self.camera_2.node().getLens(0).setFar(11333)

            if cam_parent is not None:
                self.camera_2.reparent_to(cam_parent)
            else:
                self.camera_2.reparent_to(camera)

            self.camera_2.setPos(position)
            self.camera_2.setHpr(rotation)

            # If using rtt, setup a texture buffer and make a camera with it
            if rtt_name is not None:
                texture_buffer = app.win.makeTextureBuffer(rtt_name, *resolution)
                mirror_camera = app.makeCamera(texture_buffer)
                display_region.setCamera(mirror_camera)
            else:
                display_region.setCamera(self.camera_2)

            # Generate a system name for the camera
            num_cameras = len(Combility.cameras)
            generated_name = f'camera_{num_cameras}'

            # Store the camera_name in the dictionary
            camera_name = generated_name if camera_name is None else camera_name
            Combility.pip_regions[camera_name] = self.camera_2

        def disable_new_camera(self, camera_name):
            this_camera = Combility.cameras.get(camera_name)

            if this_camera is not None:
                # self.ursina_window.removeDisplayRegion(pip_region)
                del Combility.cameras[camera_name]
                self.this_camera.removeNode()
        
        def prepare_camera_vr_simulation(self):
            ...
        
        
    class dash:
        def prepare_dash(self, 
            range=22,
            speed=205,
            direction=None,
            rotation=None,
            scale=(1,.4,1),
            circle_degrees=222,
            visual_resolution=22,
            path_resolution=6,
            surface_types=None,
            dash_style='arc_dash',
            c_dash_last_line=None,
            ):
            # pt( 
            # range,
            # speed,
            # direction,
            # rotation,
            # scale,
            # circle_degrees,
            # visual_resolution,
            # path_resolution,
            # surface_types,
            # dash_style,
            # c_dash_last_line,
            # )
            '''
            - Speed is in units/second (meters/sec)
            - rotation and direction are actually identical properties, so we can only recieve one. But we 
            convert the direction to a rotation if its an argument
            
            '''
            if dash_style not in ['arc_dash', 'g_dash', 'c_dash']:
                raise ValueError(f'The {dash_style=} must be an arc_dash, g_dash, or c_dash')
            
            if rotation and direction:
                raise ValueError(f"Cannot pass both a rotation and a direction. Choose one - In Class {self.name}")
            # If direction is passed, convert it to a rotation
            if direction:
                direction_vec = self.calculate_user_passed_direction_vec(direction)
                rotation = self.calculate_rotation_from_direction(direction_vec)
            # pt(direction)
            
            self.add_curve_to_path(
                scale=scale,
                circle_degrees=circle_degrees,
                visual_resolution=visual_resolution,
                path_resolution=path_resolution,
                
                )

            if dash_style != 'c_dash' and c_dash_last_line is not None:
                raise ValueError('c_dash_last_line is only for "dash_style=c_dash"!')
            if dash_style == 'c_dash':
                if not c_dash_last_line:
                    # Get the last two points of the path
                    last_two_points = self.assistant_visual_vertices[-2:]
                    # Calculate the vector from the second last point to the last point
                    vector = last_two_points[1] - last_two_points[0]
                    # Add the vector to the last point to get the new point
                    new_point = last_two_points[0] + vector * 10
                    # Add the new point to the path
                    self.add_points_to_path(new_point)
                else:
                    self.add_points_to_path(c_dash_last_line)
            
            self.compile_path(
                range=range, 
                rotation=rotation,
                
                # direction_vec=direction_vec,
                )
            
            self.add_target_types(general=surface_types)
            
            visual_vertices = self.assistant_visual_ent.model.vertices 
            dist_of_visual_vertices, num_points_visual_vertices = self.get_length_of_path(
                visual_vertices, scale=range)
            
            raycast_vertices = self.assistant_path_raycast_ent.model.vertices
            dist_of_raycast_vertices, num_points_raycast_vertices = self.get_length_of_path(
                raycast_vertices, scale=range)
            
            duration = dist_of_visual_vertices / speed 
            
            ratio_visual_verts_to_path_verts = num_points_visual_vertices / num_points_raycast_vertices
            
            avg_dist_between_visual_points = dist_of_visual_vertices / (num_points_visual_vertices - 1)
            
            self.is_performing_action_dash = False
            

            return surface_types, duration, num_points_visual_vertices, ratio_visual_verts_to_path_verts, raycast_vertices, avg_dist_between_visual_points
            
        def use_dash(self,
            surface_types,
            duration,
            num_points_visual_vertices,
            ratio_visual_verts_to_path_verts,
            raycast_vertices,
            avg_dist_between_visual_points):

            if self.is_performing_action_dash:
                return
            
            
            self.assistant_path_raycast_ent.world_position = self.eaat.world_position
            curve_points = [Vec3(self.world_position)] + [Vec3(scene.getRelativePoint(self.assistant_path_raycast_ent, vertex)) for vertex in self.assistant_visual_ent.model.vertices]
            
            self.add_target_types(general=surface_types)
            self.is_performing_action_dash = True
            self._choose_ray_type()
            self.assistant_path_raycast_ent.world_position = self.ccaus_barrel_end.world_position
            
            if not self.hate:
                pt.c("Dash failed. Target surface type is not in the targeted_entities list.")
                self.is_performing_action_dash = False
                return
            
            equivalent_visual_index = int(self.index_of_last_point_before_hit * ratio_visual_verts_to_path_verts)
            hit_point_distance = (self.hit_info.world_point - raycast_vertices[self.index_of_last_point_before_hit]).length()
            vertices_to_remove = int(hit_point_distance / avg_dist_between_visual_points)
            equivalent_visual_index -= vertices_to_remove
            
            new_curve_points = curve_points[:equivalent_visual_index+1]
            new_point = self.hit_info.world_point + self.hit_info.normal * (self.eaat.world_scale*0.5)
            new_curve_points.append(new_point)
            
            adjusted_duration = duration * (len(new_curve_points) / num_points_visual_vertices)
            
            if len(new_curve_points) > 1:
                self.eaat.recieve_dash(adjusted_duration, new_curve_points)
                
            self.is_performing_action_dash = False
            
            
    class visual_deception:
        def use_visibility(self, alpha=0.0, duration=1.0):
            self.eaat.recieve_visibility(self.specific_target, alpha=alpha, duration=duration)
                

        def use_mimic(self, duration=1.0):
            if self.get_real_eaat().parent.name == 'environment':
                return

            ignore_list = self.get_relevant_descendants(self.eaat)
            texture, texture_scale, color, entity = self.get_new_hit_ent_attributes(ignore_list)
            self.eaat.recieve_mimic(self.specific_target, entity=entity, duration=duration)

        def use_camo(self, duration=1.0):
            if self.get_real_eaat().parent.name == 'environment':
                return

            ignore_list = self.get_relevant_descendants(self.eaat)
            texture, texture_scale, color, entity = self.get_new_hit_ent_attributes(ignore_list)
            self.eaat.recieve_camo(specific_target=self.specific_target, texture=texture, texture_scale=texture_scale, color=color, duration=duration)
            self.add_update_function_if_exists("camo", (texture, texture_scale, color, duration))
        
        def use_copy_target(self):
            real_eaat = self.get_real_eaat()
            Combility.stored_copied_entity = real_eaat ## STORES THIS AS A WEAK REFERENCE
                                                                    ## so it can be garbage collected when destroyed
            Combility.stored_copied_entity_attributes = {
                'model': real_eaat.model,
                'world_scale': real_eaat.world_scale,
                'world_rotation': real_eaat.world_rotation,
                'texture': real_eaat.texture,
                'texture_scale': real_eaat.texture_scale,
                'color': real_eaat.color,
                'alpha': real_eaat.color.a,
                'always_on_top': real_eaat.always_on_top,
            }
            # pt('stored ent, stored attributes', Combility.stored_copied_entity_attributes, 
                # real_eaat.name, real_eaat)
                
        def get_new_hit_ent_attributes(self, ignore_list):
            if Combility.stored_copied_entity_attributes is not None:
                return Combility.stored_copied_entity_attributes['texture'], Combility.stored_copied_entity_attributes['texture_scale'], Combility.stored_copied_entity_attributes['color'], Combility.stored_copied_entity

            # First raycast in the forward direction
            hit_info = raycast(self.eaat.world_position, self.eaat.forward, 
                            distance=12, ignore=ignore_list,
                            debug=True,
                            )
            if not hit_info.hit:
                # Second raycast in the downward direction
                hit_info = raycast(self.eaat.world_position, -self.eaat.up, distance=12, ignore=ignore_list)
            if hit_info.hit:
                return hit_info.entity.texture, hit_info.entity.texture_scale, hit_info.entity.color, hit_info.entity
            else:
                # Default values if no entity is hit
                return None, None, None, None
        
        
    class tk:
        def prepare_tk_grab(self, energy_amount=100):
            deque_size = max(1, int(1 / (energy_amount / 100)))
            self.tk_grabbed_ent_positions_deque = deque(maxlen=deque_size)
            pt(deque_size)

            
            
            # self.tk_grab_hand = Light_Position_Model_Entity(
            #     parent=self, 
            #     color=tk_grab_hand_color,
            # )
            color_index = min(energy_amount // 100, 10)
            tk_grab_hand_color = EG_Globals.SHIELD_COLORS()[int(color_index)]
            
            self.tk_grab_hand = Entity(name='tk_grab_hand',
                parent=self,
                add_to_scene_entities=False, 
                model='cube',
                world_scale=.6,
                color=tk_grab_hand_color,
                enabled=False,
                )
            self.track_spawned_sub_entity(self.tk_grab_hand)
            
                
        def use_tk_grab(self, energy_amount):
            self.tk_grabbed_ent = self.get_real_eaat()
            self.tk_grab_hand.enabled = True
            
            self.tk_grab_hand.world_position = self.hit_info.world_point
            self.tk_grabbed_ent_offset = self.tk_grabbed_ent.world_position - self.tk_grab_hand.world_position

            # Calculate the initial distance between self and tk_grab_hand world positions
            initial_distance = distance(self.world_position, self.tk_grab_hand.world_position)
            
            # Calculate the number of elements to add to the deque based on the initial distance
            
            num_elements_to_add = int((initial_distance / self.path_range) * self.tk_grabbed_ent_positions_deque.maxlen)
            pt(energy_amount, initial_distance, self.path_range, initial_distance/self.path_range, num_elements_to_add,
                self.tk_grabbed_ent_positions_deque.maxlen)
            
            
            new_position = self.tk_grab_hand.world_position + self.tk_grabbed_ent_offset
            self.tk_grabbed_ent_positions_deque.extend([new_position] * num_elements_to_add)

            self.add_update_function_if_exists('tk_grab', energy_amount)
            
        def update_tk_grab(self, energy_amount):
            # pt.t(2)
            # Save the new position in the deque
            new_position = self.tk_grab_hand.world_position + self.tk_grabbed_ent_offset

            self.tk_grabbed_ent_positions_deque.append(new_position)
            self.tk_grabbed_ent.world_position = self.tk_grabbed_ent_positions_deque.popleft()


    class attacher:
        def prepare_attacher(self, energy_amount):
            self.auto_swivel = False ## TODO, might not be doing anything, anywhere..
            
            
            self.attacher_ent = Entity(name='attacher_ent', model='sphere', color=color.orange, enabled=False)
            self.track_spawned_sub_entity(self.attacher_ent)
            self.attacher_health = energy_amount
            
        def use_attacher(self, energy_amount):
            self.attached_entity = self.get_real_eaat()
            
            self.attacher_ent.enabled = True 
            self.attacher_ent.world_position = self.hit_info.world_point
            self.attached_entity_offset = self.attached_entity.world_position - self.attacher_ent.world_position
            self.add_update_function_if_exists("attacher", (energy_amount,))
        
        def update_attacher(self, energy_amount):
            if self.attacher_ent.enabled:
                self.orient_to_attacher()
                self.attached_entity.world_position = self.attacher_ent.world_position + self.attached_entity_offset
                
                
        def angle_to_start_stop_attacher(self, stop_angle=89):
            # Get the direction vectors
            direction_self = -self.forward ## TODO - Investigate why we have to use a negative forward?
                                                ## Maybe arm or one of its parents is turned around? 
            direction_attacher = self.attacher_ent.world_position - self.world_position

            # Calculate the angle between the direction vectors
            angle = self.angle_between(direction_self, direction_attacher)
            # pt(angle);pt.ex()
            # If the angle is greater than 90 degrees, disable the attacher_ent
            if angle > stop_angle:
                # rotation = self.calculate_rotation_from_direction(self.forward)
                self.projectile_visual_ent.world_rotation = self.ccaus_barrel_end.world_rotation
                self.projectile_path_raycast_ent.world_rotation = self.ccaus_barrel_end.world_rotation
                
                self.attacher_ent.enabled = False
                
                return
                

            # Only enable the attacher_ent if it's currently disabled
            if not self.attacher_ent.enabled:
                self.attacher_ent.enabled = True
        
        
        def add_auto_swivel(self):
            '''NOTE: This doesn't appear to have been working anywhere, so not sure why its in the orient_to_attacher function etc.. '''
            self.auto_swivel = True
            
        def orient_to_attacher(self):
            '''
            - rope/solids might care if attacher actually connects or not, 
                but this function does not. It only looks to orient. 
            - DO NOT shorten paths for attacher distance. We may have
                penetration, etc. This only is for orientation. 

            '''
            
            if self.auto_swivel:
                self.look_at_in_local_space(self, self.attacher_ent)
            else:
                self.look_at_in_local_space(self.projectile_visual_ent, self.attacher_ent)
                self.look_at_in_local_space(self.projectile_path_raycast_ent, self.attacher_ent)
                
                self.angle_to_start_stop_attacher(89)
                ## TODO BUGFIX: I should be able to pass only the self.ccaus_barrel_end instead of both
                ##  the self.path_raycast_ent and self.raycast_path_raycast_ent, to achieve the same/cleaner version
                ##  of the same thing. But when I use the bullet_end, the path shrinks in size. 
                # self.look_at_in_local_space(self.ccaus_barrel_end, self.attacher_ent)
