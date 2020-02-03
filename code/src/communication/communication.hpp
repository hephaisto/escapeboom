#include "state.hpp"

namespace communication
{

class Communication
{
public:
	Communication(State &state)
	:m_state{state}
	{}

	void setup(){}
	void loop(){}
private:
	State &m_state;
};

}
