
#include "viz_sound.h"
#include "viz_defines.h"
#include "viz_main.h"

unsigned int vizSoundLen;

int *vizAudioSM = NULL;
short test_buffer[buffer_len][2];

void VIZ_SoundInit() {
    try {
        VIZSMRegion *bufferRegion = &vizSMRegion[VIZ_SM_AUDIO_NUM];
        VIZ_SMCreateRegion(bufferRegion, false, VIZ_SMGetRegionOffset(bufferRegion), buffer_len);
//        printf("Created audio buffer");
        memset(bufferRegion->address, 0, bufferRegion->size);

        VIZ_DebugMsg(1, VIZ_FUNC, "region: %d, offset %zu, size: %zu", VIZ_SM_AUDIO_NUM,
                     bufferRegion->offset, bufferRegion->size);

    }
    catch(...){ // bip::interprocess_exception
        VIZ_Error(VIZ_FUNC, "Failed to map buffers.");
    }

    vizAudioSM = static_cast<int *>(VIZ_SM_AUDIO.address);
}

void VIZ_CopySoundBuffer() {
    S_Get_render(test_buffer, buffer_len);
    memcpy((void *) vizAudioSM, (void *) test_buffer, 4 * buffer_len);
}
