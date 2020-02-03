#include "main_state.hpp"

#include "communication/communication.hpp"

FullState state;

communication::Communication comm{state.commState};

void setup()
{
	comm.setup();
}

void loop()
{
	comm.loop();
}
