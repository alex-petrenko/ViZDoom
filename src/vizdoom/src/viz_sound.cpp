
#include "viz_sound.h"
#include "viz_defines.h"
#include "viz_main.h"
#include "viz_labels.h"

EXTERN_CVAR (Int, samp_fre)



int *vizAudioSM = NULL;


void VIZ_SoundInit() {
    try {
        VIZSMRegion *bufferRegion = &vizSMRegion[VIZ_SM_AUDIO_NUM];
        VIZ_SMCreateRegion(bufferRegion, false, VIZ_SMGetRegionOffset(bufferRegion), 2 * sizeof(short) * 1260/(44100/(*samp_fre)));
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
    S_Get_render(vizAudioSM, 1260/(44100/(*samp_fre)));
}
