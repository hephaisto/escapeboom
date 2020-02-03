#include "main_state.hpp"

#include "communication/communication.hpp"

FullInput input;
FullOutput output;
FullState state;

communication::Communication comm{state.commState, input.comm, output.comm};

void setup()
{
	comm.setup();
}

void loop()
{
	comm.loop();
}
