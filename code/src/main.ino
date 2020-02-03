#include "main_state.hpp"

#include "communication/communication.hpp"

FullInput input;
FullState state;

communication::Communication comm{state.commState, input.comm};

void setup()
{
	comm.setup();
}

void loop()
{
	comm.loop();
}
