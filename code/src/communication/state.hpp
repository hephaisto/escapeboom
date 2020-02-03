#pragma once

namespace communication
{

enum class Source
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
	uint8_t antennaAngle{35};
	bool turning;
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

	bool antennaCw;
	bool antennaCcw;
};

struct HardwareOutput
{
	// display TODO
	bool motorMalfunction;
	bool motorActive;
};

}
