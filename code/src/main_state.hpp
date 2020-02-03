#include "communication/state.hpp"

struct FullInput
{
	communication::HardwareInput comm;
};

struct FullOutput
{
	communication::HardwareOutput comm;
};

struct FullState
{
	communication::State commState;
};

