"""main_vr 02 """
from print_tricks import pt
import os

from ursina import *
from p3dopenvr.p3dopenvr import P3DOpenVR
from p3dopenvr.skeleton import DefaultLeftHandSkeleton, DefaultRightHandSkeleton
from p3dopenvr.hand import LeftHand, RightHand

import pydirectinput
from panda3d.core import LVector3

pydirectinput.PAUSE = 0.0


def setup_vr(app, player):
    # Panda3d FPS meter (it displays different numbers than Ursina...)
    app.setFrameRateMeter(True)
    app.disableMouse()

    # Create and configure the VR
    ovr = P3DOpenVR()
    """Optional Items to set in our VR environment:
    Set Far clip plane, anti aliasing, and setup a "root" object to attach your playspace to objects in game (for moving around, etc)"""
    # ovr.init(far=25000, root=player.head)
    # ovr.init(far=25000, root=player)
    ovr.init(far=25000)

    app.win.setClearColor((0, 0, 0, 1))  # Set the background color to black

    # NOTE TODO vvv - This is actually intelligent code to place an object onto the ground correctly. I can utilize this (I think) in Ursina. Or use it as inspiration because not sure how easy it would be to use tight_bounds
    # model = loader.loadModel("panda")
    # model.reparentTo(render)
    # min_bounds, max_bounds = model.get_tight_bounds()
    # height = max_bounds.get_z() - min_bounds.get_z()
    # model.set_scale(1.5 / height)
    # model.set_pos(10, 11, -min_bounds.get_z() / height * 1.5)

    ### keyboard Controls (We should probably adapt these to ursina Inputs)
    app.accept("escape", app.userExit)
    app.accept("d", ovr.list_devices)
    app.accept("b", app.bufferViewer.toggleEnable)

    vr = Main_VR(ovr, app, player)


class Main_VR(Entity):
    def __init__(self, ovr, app, player):
        super().__init__()
        self.ovr = ovr
        self.player = player

        # Setup the application manifest, it will identify and configure the app
        # We force it in case it has changed.
        # cwd = os.getcwd()
        cwd = pt.l()
        pt(cwd)
        vrmanifest = f"{cwd}\\manifest\\main_vr.vrmanifest"
        actions_json = f"{cwd}\\manifest\\actions.json"

        pt(f" actions.json exists! - {actions_json}") if os.path.exists(
            actions_json
        ) else pt(f" actions.json does not exist! {actions_json}")

        pt(f"manifest exists {vrmanifest}") if os.path.exists(vrmanifest) else pt(
            f" manifest not exist {vrmanifest}"
        )
        ovr.identify_application(os.path.join(vrmanifest), "egvr.p3dopenvr", force=True)
        # Load the actions manifest, it must be the same as the manifest referenced
        #   in the application manifest
        ovr.load_action_manifest(actions_json)
        # Use the '/actions/default' action set. This action set will be updated each frame
        ovr.add_action_set("/actions/default")

        # Use the '/actions/platformer' action set. This action set will be updated each frame
        self.ovr.add_action_set("/actions/platformer")

        ###
        # SKELETON stuff
        ###
        # Get the handle of the action '/actions/default/in/Pose'. This hande will be
        #   used to update the position of the hands.
        hands_pose = ovr.vr_input.getActionHandle("/actions/default/in/Pose")
        # self.action_move = self.ovr.vr_input.getActionHandle(
        #  '/actions/platformer/in/Move')

        # Get the handle of the skeleton actions. These handle will be used to update
        #   the animation of the hands
        left_hand_skeleton_input = ovr.vr_input.getActionHandle(
            "/actions/default/in/SkeletonLeftHand"
        )
        right_hand_skeleton_input = ovr.vr_input.getActionHandle(
            "/actions/default/in/SkeletonRightHand"
        )

        # Create the representation of the left hand and attach a skinned hand model
        # to it
        self.left_hand = LeftHand(
            ovr, "assets/vr_models/vr_glove_left_model.glb", hands_pose
        )
        self.left_hand.set_skeleton(
            DefaultLeftHandSkeleton(ovr, left_hand_skeleton_input)
        )

        # Create the representation of the left hand and attach a skinned hand model
        # to it
        self.right_hand = RightHand(
            ovr, "assets/vr_models/vr_glove_right_model.glb", hands_pose
        )
        self.right_hand.set_skeleton(
            DefaultRightHandSkeleton(ovr, right_hand_skeleton_input)
        )

        self.title = Text(
            "VR Mode",
            scale=6,
            color=color.white,
            line_height=2,
            x=-0.2,
            y=0.44,
            parent=camera.ui,
        )

        self.inst1 = Text("[ESC] - Quit", x=-0.84, y=0.45, color=color.black)
        # self.inst1_shadow  = Text("[ESC] - Quit",
        #                             x = -.84, y=.1,
        #                             scale = 1.2,
        #                             color = color.black)

        self.inst2 = Text(
            "[F10] - Cycle through collision, ..., ..., ...",
            x=-0.84,
            y=0.4,
            color=color.black,
        )
        self.inst3 = Text(
            "[L stick up] - Walk Forward", x=-0.84, y=0.35, color=color.black
        )

        # Set up the environment
        # self.ovr.tracking_space.setPos(self.ralphStartPos)
        # self.ralph.setPos(self.ovr.hmd_anchor.getPos(render))

        ################
        # New untested VR device data
        ################
        # Get the handle of the action '/actions/platformer/in/Move'. This handle will
        #   be used to retrieve the data of the action.
        self.action_move = self.ovr.vr_input.getActionHandle(
            "/actions/platformer/in/Move"
        )

        # Get the handle of the action '/actions/default/out/Haptic'. This handle will
        #   be used to trigger the haptic vibration.
        self.action_haptic = ovr.vr_input.getActionHandle("/actions/default/out/Haptic")

        # Get the handle of the action '/actions/default/in/GrabGrip'. This handle will
        #   be used to retrieve the data of the action.
        self.action_grip = ovr.vr_input.getActionHandle("/actions/default/in/GrabGrip")
        self.grip_active = False

        self.action_pinch = ovr.vr_input.getActionHandle(
            "/actions/default/in/GrabPinch"
        )
        self.pinch_active = False

    def update(self):
        # try:
        # print('update')
        self.get_vr_data()
        self.pinch_temp_jump()
        self.grip_temp_teleport()
        # self.pinch()
        # self.grip()
        # self.move()
        # self.move_original()
        self.move_original2()
        self.ovr.tracking_space.setPos(self.player.position)
        self.ovr.get_update_task_sort()
        self.left_hand.update()
        self.right_hand.update()

    # except:
    #     ...
    def get_vr_data(self):
        try:
            self.move_data, self.device_path = self.ovr.get_analog_action_value(
                self.action_move
            )
        except:
            ...
        # pydirectinput.keyDown('w')
        ...

    def pinch(self):
        # Retrieve the state of the pinch action and the device that has triggered it
        pinch_state, device = self.ovr.get_digital_action_rising_edge(
            self.action_pinch, device_path=True
        )
        if pinch_state:
            # If the pinch is active, activate the haptic vibration on the same device
            self.ovr.vr_input.triggerHapticVibrationAction(
                self.action_haptic, 0, 1, 4, 1, device
            )

            pydirectinput.keyDown("w")
            # invoke(self.pinch_stop, delay=.1)
        # else:
        #     pydirectinput.keyUp('w')

    def pinch_stop(self):
        pydirectinput.keyUp("w")

    def pinch_temp_jump(self):
        pinch_state, device = self.ovr.get_digital_action_rising_edge(
            self.action_pinch, device_path=True
        )
        if pinch_state:
            # If the pinch is active, activate the haptic vibration on the same device
            # self.ovr.vr_input.triggerHapticVibrationAction(self.action_haptic, 0, 1, 4, 1, device)

            pydirectinput.keyDown("space")
            # pt('space')
            pydirectinput.keyUp("space")

    def grip_temp_teleport(self):
        grip_state, device = self.ovr.get_digital_action_rising_edge(
            self.action_grip, device_path=True
        )
        if grip_state:
            # If the grip is active, activate the haptic vibration on the same device
            # self.ovr.vr_input.triggerHapticVibrationAction(self.action_haptic, 0, 1, 4, 1, device)

            pydirectinput.keyDown("tab")
            # pt('tab')
            pydirectinput.keyUp("tab")

    def grip(self):
        # Retrieve the state of the Grip action and the device that has triggered it
        grip_state, device = self.ovr.get_digital_action_rising_edge(
            self.action_grip, device_path=True
        )
        # if pt.r(reactivateInSeconds=1):
        #     pt(grip_state, device)

        # if grip_state:
        #     pt('grip')
        #     pydirectinput.keyDown('s')
        #     self.grip_active = True
        # #     # If the grip is active, activate the haptic vibration on the same device
        # #     self.ovr.vr_input.triggerHapticVibrationAction(self.action_haptic, 0, 1, 4, 1, device)

        # #     pydirectinput.keyDown('s')
        # #     pt('s down')

        # #     # invoke(self.grip_stop, delay=.1)
        # # elif self.grip_active == True and grip_state == False:
        # #     self.grip_active = False
        # #     pt('s up')
        # #     # pydirectinput.keyUp('s')
        # #     # invoke(self.grip_stop, delay=.1)
        # elif self.grip_active == True:
        #     if grip_state == False:
        #         pt('no grip')

    def grip_stop(self):
        pydirectinput.keyUp("s")

    def move(self):
        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()

        # If a move-button is touched, move in the specified direction.
        if self.move_data is not None:
            # print('move', move_data)
            x, z = self.move_data.x, self.move_data.z
            # The x coordinate is used to turn the camera
            self.ovr.tracking_space.setH(self.ovr.tracking_space.getH() - x * 60 * dt)
            # The y coordinate is used to move the camera along the view vector
            # We retrieve the orientation of the headset and we generate a 2D direction
            orientation = self.ovr.hmd_anchor.get_quat(render)

            # vector = orientation.xform(LVector3(0, 1, 0))
            # vector[2] = 0

            # vector = Vec3(0, 1, 0)
            vector = Vec3(0, 0, 1)
            # vector[2] = 0
            # vector[2] = 0
            vector.normalize()
            # Use the vector and the x value to move the camera relative to itself
            # self.ovr.tracking_space.setPos(self.ovr.tracking_space.getPos() + vector * (y * 5 * dt))
            self.player.position = self.player.position + vector * (z * 5 * dt)

    def move_original(self):
        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()

        # If a move-button is touched, move in the specified direction.
        if self.move_data is not None:
            # print('move', move_data)
            x, y = self.move_data.x, self.move_data.y
            # The x coordinate is used to turn the camera
            self.ovr.tracking_space.setH(self.ovr.tracking_space.getH() - x * 60 * dt)
            # The y coordinate is used to move the camera along the view vector
            # We retrieve the orientation of the headset and we generate a 2D direction
            orientation = self.ovr.hmd_anchor.get_quat(render)

            # vector = orientation.xform(LVector3(0, 1, 0))
            # pt('--start--')
            vector = Vec3(0, 0, 1)
            # pt(vector)
            # vector[2] = 0
            # pt(vector)
            vector.normalize()
            # pt(vector)
            # Use the vector and the x value to move the camera relative to itself
            # self.ovr.tracking_space.setPos(self.ovr.tracking_space.getPos() + vector * (y * 5 * dt))
            self.player.position = self.player.position + vector * (y * 5 * dt)

    def move_original2(self):
        # Get the time that elapsed since last frame.  We multiply this with
        # the desired speed in order to find out with which distance to move
        # in order to achieve that desired speed.
        dt = globalClock.getDt()

        # If a move-button is touched, move in the specified direction.
        if self.move_data is not None:
            # print('move', move_data)
            x, y, z = self.move_data.x, self.move_data.y, self.move_data.z
            # The x coordinate is used to turn the camera
            self.ovr.tracking_space.setH(self.ovr.tracking_space.getH() - x * 60 * dt)
            # The y coordinate is used to move the camera along the view vector
            # We retrieve the orientation of the headset and we generate a 2D direction
            orientation = self.ovr.hmd_anchor.get_quat(render)

            vector = orientation.xform(LVector3(0, 0, 1))
            # pt('--start--')
            # vector = Vec3(0, 0, 1)
            # pt(vector)

            # flight on or off lol
            vector[
                1
            ] = 0  # turns off flight, lol Commend this out to fly instead of walk
            # pt(vector)
            vector.normalize()
            # pt(vector)
            # Use the vector and the x value to move the camera relative to itself
            # self.ovr.tracking_space.setPos(self.ovr.tracking_space.getPos() + vector * (y * 5 * dt))
            # self.player.rotation = orientation
            self.player.position = self.player.position + vector * (y * 25 * dt)
            # self.player.rotation = orientation

            # self.ovr.tracking_space.setPos(self.ovr.tracking_space.getPos() + vector * (y * 5 * dt))
            # self.player.position = self.ovr.tracking_space.getPos()
            self.player.rotation = self.ovr.hmd_anchor.getPos(render)
            # self.player.rotation = orientation

            # self.ovr.tracking_space.setPos(self.ovr.tracking_space.getPos() + vector * (y * 5 * dt))


if __name__ == "__main__":
    app = Ursina()
    from levels.levels import CityLevel, Hyperdash_OrangeA

    player = Entity(model="cube", scale=(0.25, 1, 0.25))
    citylevel = CityLevel(player, enabled=True)
    setup_vr(app, player)

    app.run()
