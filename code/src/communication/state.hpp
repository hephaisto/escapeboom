#pragma once

namespace communication
{

enum Source
{
	off,
	morse,
	crypt,
	aux,
	plain,
	microphone,
	boardCom1,
	boardCom2
};

struct State
{
	bool canBePoweredOn{false};
	Source selectedSource;
	uint16_t selectedFrequency{800};
};

struct HardwareInput
{
	bool off;
	bool morse;
	bool crypt;
	bool aux;
	bool plain;
	bool microphone;
	bool boardCom1;
	bool boardCom2;

	bool auxIn;
	bool morseButton;

	bool frequencyA;
	bool frequencyB;

	bool antennaLeft;
	bool antennaRight;
};

struct HardwareOutput
{
	// display TODO
};

}