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
	bool enabled{false};

};

}
