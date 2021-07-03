#!/usr/bin/env python3

#####################################################################
# This script presents how to use the most basic features of the environment.
# It configures the engine, and makes the agent perform random actions.
# It also gets current state and reward earned with the action.
# <episodes> number of episodes are played. 
# Random combination of buttons is chosen for every action.
# Game variables from state and last reward are printed.
#
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from __future__ import print_function
import vizdoom as vzd
print(vzd.__file__)
import moviepy.editor as mpe
import cv2

from random import choice
from time import sleep
import time
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plot
import os
# import msvcrt

# import wavio
is_audio = True

if __name__ == "__main__":
    # Create DoomGame instance. It will run the game and communicate with you.
    game = vzd.DoomGame()

    # Now it's time for configuration!
    # load_config could be used to load configuration instead of doing it here with code.
    # If load_config is used in-code configuration will also work - most recent changes will add to previous ones.
    # game.load_config("../../scenarios/basic.cfg")

    # Sets path to additional resources wad file which is basically your scenario wad.
    # If not specified default maps will be used and it's pretty much useless... unless you want to play good old Doom.
    
    wad_path = "/home/khegde/Desktop/Github/sample-factory/envs/doom/scenarios/simple_sound_finder.wad"
    # wad_path = "/home/shashank/Downloads/play_a_sound.wad"

    game.set_doom_scenario_path(wad_path)
    # game.set_doom_scenario_path("./scenarios/deathmatch.wad")
    # game.set_doom_scenario_path("./scenarios/rocket_basic.wad")
    # game.set_doom_scenario_path("./scenarios/defend_the_center.wad")

    # Sets map to start (scenario .wad files can contain many maps).
    game.set_doom_map("map01")

    # Sets resolution. Default is 320X240
    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)
    # game.set_screen_resolution(vzd.ScreenResolution.RES_160X120)


    # Sets the screen buffer format. Not used here but now you can change it. Default is CRCGCB.
    game.set_screen_format(vzd.ScreenFormat.RGB24)

    # Enables depth buffer.
    game.set_depth_buffer_enabled(True)

    # Enables labeling of in game objects labeling.
    game.set_labels_buffer_enabled(True)

    # Enables buffer with top down map of the current episode/level.
    game.set_automap_buffer_enabled(True)

    # Enables information about all objects present in the current episode/level.
    game.set_objects_info_enabled(True)

    # Enables information about all sectors (map layout).
    game.set_sectors_info_enabled(True)

    # Sets other rendering options (all of these options except crosshair are enabled (set to True) by default)
    game.set_render_hud(False)
    game.set_render_minimal_hud(False)  # If hud is enabled
    game.set_render_crosshair(False)
    game.set_render_weapon(True)
    game.set_render_decals(False)  # Bullet holes and blood on the walls
    game.set_render_particles(False)
    game.set_render_effects_sprites(False)  # Smoke and blood
    game.set_render_messages(False)  # In-game messages
    game.set_render_corpses(False)
    game.set_render_screen_flashes(True)  # Effect upon taking damage or picking up items

    # Adds buttons that will be allowed.
    # game.add_available_button(vzd.Button.MOVE_LEFT)
    # game.add_available_button(vzd.Button.MOVE_RIGHT)
    game.add_available_button(vzd.Button.MOVE_FORWARD)
    game.add_available_button(vzd.Button.MOVE_BACKWARD)
    game.add_available_button(vzd.Button.TURN_LEFT)
    game.add_available_button(vzd.Button.TURN_RIGHT)
    		
		
		
		
    # game.add_available_button(vzd.Button.ATTACK)

    # Adds game variables that will be included in state.
    game.add_available_game_variable(vzd.GameVariable.AMMO2)

    # Causes episodes to finish after 200 tics (actions)
    game.set_episode_timeout(500)

    # Makes episodes start after 10 tics (~after raising the weapon)
    game.set_episode_start_time(10)

    # Makes the window appear (turned on by default)
    game.set_window_visible(True)

    # -----------------------------------------------------------------------------------------------------------------------
    # Turns on the sound. (turned off by default)
    game.set_sound_enabled(is_audio)
    # -----------------------------------------------------------------------------------------------------------------------

    # Sets the living reward (for each move) to -1
    game.set_living_reward(-1)

    # Sets ViZDoom mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR, PLAYER mode is default)
    game.set_mode(vzd.Mode.PLAYER)

    # Enables engine output to console.
    #game.set_console_enabled(True)

    # Initialize the game. Further configuration won't take any effect from now on.
    game.init()

    # Define some actions. Each list entry corresponds to declared buttons:
    # MOVE_LEFT, MOVE_RIGHT, ATTACK
    # game.get_available_buttons_size() can be used to check the number of available buttons.
    # 5 more combinations are naturally possible but only 3 are included for transparency when watching.
    actions = [[True, False, False, False, False, False], 
                [False, True, False, False, False, False], 
                [False, False, True, False, False, False], 
                [False, False, False, True, False, False], 
                [False, False, False, False, True, False], 
                [False, False, False, False, False, True]]

    # Run this many episodes
    episodes = 1
    f_skip = 12
    # Sets time that will pause the engine after each action (in seconds)
    # Without this everything would go too fast for you to keep track of what's happening.
    sleep_time = 1.0 / vzd.DEFAULT_TICRATE  # = 0.028
    sleep_time *= f_skip

    audios = []
    screens = []
    d = 0
    frames = 0
    st_tim = time.time()
    for i in range(episodes):
        print("Episode #" + str(i + 1))

        # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
        game.new_episode()
        step = 0
        while not game.is_episode_finished():

            a = 1

            # Gets the state
            state = game.get_state()

            # Which consists of:
            n = state.number
            vars = state.game_variables
            screen_buf = state.screen_buffer
            depth_buf = state.depth_buffer
            labels_buf = state.labels_buffer
            automap_buf = state.automap_buffer
            labels = state.labels
            objects = state.objects
            sectors = state.sectors
            if is_audio:
                if state.audio_buffer is not None:
                    audio = state.audio_buffer

                    audios.extend(list(audio))
                    # audios.extend([np.array([0,0]) for l in range(1260*3)])
                    # plot.specgram(audio[:,0])
                    # plot.show()

            screens.append(screen_buf[:,:,::-1])
                # print(max(audio))

            # Games variables can be also accessed via:
            #game.get_game_variable(GameVariable.AMMO2)

            # Makes a random action and get remember reward.
            if step % 10 == 0:
                ac = choice(actions)
            # print(ac)
            r = game.make_action(ac,f_skip)
            # r = game.make_action(ac)
            frames += 1
            # d += 1
            # Makes a "prolonged" action and skip frames:
            # skiprate = 4
            # r = game.make_action(choice(actions), skiprate)

            # The same could be achieved with:
            # game.set_action(choice(actions))
            # game.advance_action(skiprate)
            # r = game.get_last_reward()

            # Prints state's game variables and reward.
            # print("State #" + str(n))
            # print("Game variables:", vars)
            # print("Reward:", r)
            # print("=====================")

            if sleep_time > 0:
                # sleep(sleep_time)
                d += sleep_time
            step += 1
        # Check how the episode went.
        # print("Episode finished.")
        # print("Total reward:", game.get_total_reward())
        # print("************************")
    en_tim = time.time()
    l = []
    r = []
    m = []
    for i,a in enumerate(audios):
        m.append(a)
        if i % 2 == 0:
            l.append(a)
        else:
            r.append(a)

    wa = np.array([l,r])
    m = np.array(m)
    ran = np.random.randint(200)

    vid = np.array(screens)
    os.makedirs("trials/"+str(ran), exist_ok=True)

    print("actual time:")
    print(en_tim - st_tim)
    print("Game time:")
    print(d)
    print("Frame rate:")
    print(frames/(en_tim - st_tim))
    if is_audio:
        print("Total audio length is: {}".format(len(m[:,0])))
        plot.specgram(m[:,0])
        plot.savefig('trials/'+ str(ran) +'/specl.png')
        plot.specgram(m[:,1])
        plot.savefig('trials/'+ str(ran) +'/specr.png')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('trials/'+ str(ran) +'/video.mp4', fourcc, vzd.DEFAULT_TICRATE/f_skip, (640,480))
    for i in range(len(screens)):
        out.write(screens[i])
    out.release()
    if is_audio:
        # write('trials/'+ str(ran) +'/audio.wav', 44100/2, m)
        write('trials/'+ str(ran) +'/audio.wav', 22050, m)
        # write('stereo_test'+ str(en_tim - st_tim) +'.wav', 44100, wa.T)
        # wavio.write('stereo_test'+ str(en_tim - st_tim) +'.wav',)
        print("total audio time should be :" + str(d))
    # It will be done automatically anyway but sometimes you need to do it in the middle of the program...
    my_clip = mpe.VideoFileClip('trials/'+ str(ran) +'/video.mp4')
    if is_audio:
        audio_background = mpe.AudioFileClip('trials/'+ str(ran) +'/audio.wav')
        # final_audio = mpe.CompositeAudioClip([my_clip.audio, audio_background])
        final_clip = my_clip.set_audio(audio_background)
    else:
        final_clip = my_clip
    final_clip.write_videofile("trials/"+ str(ran) +"/movie.mp4")
    game.close()