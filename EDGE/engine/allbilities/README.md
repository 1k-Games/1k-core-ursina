<style>
    h1 { color: lightgreen; }
    h2 { color: skyblue; }
    h3 { color: darkorchid; }
</style>

<h1>
Allbilities
</h1>

<h2>
Combility:
</h2>

A combination of:
  - A trigger-control system
  - Any combination of other mods, Mod Mixes, or other Combilities
  - Models, Animations, & Sounds to support it


This is attached to a slot. Allows you to use weapons/tools/abilities.  

Other names: a Combination of Abilities, Combility Device/Tool/Tech/Weapon, or Co-Mod, CombiMods, Combactions. 

<h3>Mods/Actions/Abilities: </h3>

Individual abilities or properties that can modify the energy output of your device. Build together to form a Mod Mix or a Combility (Combination of Abilities). 

<h3>Mod Mix: </h3>

A combination of several mods, that are grouped together by the user, but does nothing until you combine them into a combility, with or without other mods & mod mixes (not trigger control system, etc).

<h3>Combilities: </h3>

More than one Combility.

<h3>Slot:</h3>

Energy-port on your armor that can generate combilities. 

<h3>Loadout: </h3>

- Contains a pre-determined Combility in each of the 8+ slots.
- Switching a loadout means that all 8 slots change their combilities at once. 

<h2>
Skillbility: 
</h2>

Actions that take skills to perform for benefits:
- Parrying a shot, 
- Shooting center of a bubble shield
- All of the Realbilities

<h2>
Movbility: 
</h2>

In-game movement abilities.
These are actually all mod mixes that have a different control trigger system than their combility counterparts. Triggered via combinations of stick movements primarily. 

- Walking
- Sprinting
- Dodging (Flick & quickly let go of stick)
- Mid-air dodging (flick and quickly let go of stick)
- Landing a Fall
- Jumping
- Wall Jumping (jumping off a wall for greater height)
- Wall Running
- Wall Climbing

<h2>
Realbility: 
</h2>

Moving IRL to accomplish in-game actions at 0 energy cost (because you are using energy/coordination/exercise IRL). Almost all Movbilities can be Realbilities. Maybe some other abilities that aren't Movbitlities could be candidates as well. 

<h3>examples: </h3>

- Dodging IRL to dodge huge in game.
    - Left/right/forward/backward dodges
    - jump for upward dodge if in air, or jump if on ground
    - crouch for downward dodge if in air, and low crouch if on ground. 

- Crouching IRL to do a super-low crouch in game.
    - Crouching at the right time when falling to land with 0 damage/energy loss. 
- Jumping IRL to do super jump-dodge in game. 
- Walking/Running in place to do the same in game. 


How to categorize these?:
- Parrying bullets... Do you need energy to do this or not? It is a IRL skill, but then again, so is aiming a weapon.... 


<h2>
Corebility:
</h2>

- Possibly spawn in with less max capacity by spawning in early. 
- Self Destruction

<h2>
Swap Combilities:
</h2>

(See my notes in EG controls spreadsheet)

<h2>
Swap Loadouts:
</h2>

(see my notes in eg controls spreadsheet)

- Swapping loadouts via the rods in your R arm.
- Accessing even more loadouts/options via a cog wheel on your r arm.



<h1>
File Structure
</h1>

<h2>
Keys:
</h2>

</h4>

- E = Entity,
- NP = Nodepath,
- GI = GPU Instance
- BB = Billboard (np)
- I = instantiated simple class,
- D = data (data to be used in other classes),

- N = Number of objects/instances/




<h3>
Character / CCAUS / Combility / Mods:
</h3>
-> Game -> Game Manager

-> Character (E) -> CCAUS device (E)

-> live_combility (NP) -> combility_code (D)

-> Mods (D)
 - Mods_Effects 
    - brings in various mod files
    - has a filter, for certain mods per game.
    - has low-level and high-level mod files
 - Mods_Trajectories
    - (Same stuff as mods_effects)



<h3>
Aura's (E, NP, I, D)
</h3>
-> AuraManager (I) -> AuraSector (I) -> AuraZone (I)

-> AGG_Color_Atlas, -> AGG_Box_Atlas, -> AGG_3d_Atlas, 

-> AuraGroup_Color_Atlas -> AuraGroup_Box_Atlas, -> AuraGroup_3d_Atlas (NP, I*N), 

-> AuraBB, -> AuraGI -> AuraNodepath -> AuraEntity



AuraGrandGroup
(with: AGG_color_Atlas, AGG_box_Atlas, AGG_3d_Atlas)
- A texture atlas Mesh points, where each point is a picture of AuraGroup that was absorbed by this Grand Group. 

AuraGroup_color_atlas:
- Each aura is represented by a couple of colored pixels at best. 

AuraGroup_box_Atlas:
- A simple 6-sided box that has the Aura picture taken from 6 sides. 

AuraGroup_3d_Atlas:
- Aura has images placed on multiple angles. A rough 3d view of the model is formed depending on the angle viewed. Each image is on a texture atlas. Each Aura is part of a Mesh(), and is just
one re-created quad or a couple of quads with a texture atlas to recreate his likness. 

AuraBB:
- The active Billboard part of an Aura

AuraGI:
- The active GPU instance part of an Aura

AuraNodepath:
- The active Nodepath part of an Aura

AuraEntity: 
- The active entity part of an aura



