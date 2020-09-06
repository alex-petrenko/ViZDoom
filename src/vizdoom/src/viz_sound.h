

#ifndef VIZDOOM_VIZ_SOUND_H
#define VIZDOOM_VIZ_SOUND_H

#include "viz_shared_memory.h"
#include "basictypes.h"
#include "s_sound.h"
#include <stddef.h>

extern unsigned int vizSoundLen;

void VIZ_SoundInit();
void VIZ_CopySoundBuffer();

#endif //VIZDOOM_VIZ_SOUND_H
