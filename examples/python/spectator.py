#!/usr/bin/env python3

#####################################################################
# This script presents SPECTATOR mode. In SPECTATOR mode you play and
# your agent can learn from it.
# Configuration is loaded from "../../scenarios/<SCENARIO_NAME>.cfg" file.
# 
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from __future__ import print_function

from time import sleep
import vizdoom as vzd
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plot
import cv2
from scipy.io.wavfile import write
import moviepy.editor as mpe
import os

DEFAULT_CONFIG = "/home/khegde/Desktop/Github/sample-factory/envs/doom/scenarios/sound_multi.cfg"
if __name__ == "__main__":
    parser = ArgumentParser("ViZDoom example showing how to use SPECTATOR mode.")
    parser.add_argument(dest="config",
                        default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../../scenarios/*cfg for more scenarios.")
    args = parser.parse_args()
    game = vzd.DoomGame()
    number_of_frames = 4

    # Choose scenario config file you wish to watch.
    # Don't load two configs cause the second will overrite the first one.
    # Multiple config files are ok but combining these ones doesn't make much sense.

    game.load_config(args.config)

    # Enables freelook in engine
    game.add_game_args("+freelook 1")

    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)
    game.set_sound_enabled(True)
    game.set_sound_sampling_freq(vzd.SamplingRate.SR_44100)
    game.set_frame_number(number_of_frames)

    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    game.set_mode(vzd.Mode.SPECTATOR)

    game.init()

    episodes = 1
    audios = []
    screens = []

    for i in range(episodes):
        print("Episode #" + str(i + 1))

        game.new_episode()
        while not game.is_episode_finished():
            state = game.get_state()

            game.advance_action()
            last_action = game.get_last_action()
            reward = game.get_last_reward()
            state = game.get_state()
            if state is not None:
                if state.audio_buffer is not None:
                    audio = state.audio_buffer
                    list_audio = list(audio)
                    audios.extend(list_audio[:len(list_audio)//number_of_frames])
                    # audios.extend(list_audio)
                    screen = state.screen_buffer
                    screens.append(np.swapaxes(np.swapaxes(screen,0,1),1,2)[:,:,::-1])


                print("State #" + str(state.number))
                print("Game variables: ", state.game_variables)
                print("Action:", last_action)
                print("Reward:", reward)
                print("=====================")

        print("Episode finished!")
        print("Total reward:", game.get_total_reward())
        print("************************")
        sleep(2.0)

    game.close()

    audios = np.array(audios)
    videos = np.array(screens)

    ran = np.random.randint(200)
    os.makedirs("trials/"+str(ran), exist_ok=True)

    plot.specgram(audios[:,0])
    plot.savefig('trials/'+ str(ran) +'/specl.png')
    plot.specgram(audios[:,1])
    plot.savefig('trials/'+ str(ran) +'/specr.png')

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('trials/'+ str(ran) +'/video.mp4', fourcc, 35, (640,480))
    for i in range(len(screens)):
        out.write(screens[i])
    out.release()
    write('trials/'+ str(ran) +'/audio.wav', 44100, audios)
    # print("total audio time should be :" + str(d))
    my_clip = mpe.VideoFileClip('trials/'+ str(ran) +'/video.mp4')
    audio_background = mpe.AudioFileClip('trials/'+ str(ran) +'/audio.wav')
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile("trials/"+ str(ran) +"/movie.mp4")