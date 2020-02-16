#include "../config.hpp"

#include "state.hpp"

namespace communication
{

class Communication
{
public:
	Communication(State &state, HardwareInput &hardware)
	:m_state{state}
	,m_hardware{hardware}
	{}

	void setup()
	{
	}

	void loop()
	{
		readSourceSwitch();
	}
private:
	State &m_state;
	HardwareInput &m_hardware;

	enum class RotationDirection
	{
		cw, ccw
	} m_currentRotationDirection;
	bool m_isRotating{false};
	unsigned long m_millisecondsWhenRotationEnds{0};

	void readSourceSwitch()
	{
		uint8_t numActive = 0;
		Source newSource{Source::off};

		setSource(newSource, Source::off, m_hardware.off, numActive);
		setSource(newSource, Source::morse, m_hardware.crypt, numActive);
		setSource(newSource, Source::aux, m_hardware.aux, numActive);
		setSource(newSource, Source::plain, m_hardware.plain, numActive);
		setSource(newSource, Source::microphone, m_hardware.microphone, numActive);
		setSource(newSource, Source::boardCom1, m_hardware.boardCom1, numActive);
		setSource(newSource, Source::boardCom2, m_hardware.boardCom2, numActive);

		if(numActive == 1)
		{
			m_state.selectedSource = newSource;
		}
	}

	void setSource(Source &newSource, const Source pinSource, const bool input, uint8_t &numActive)
	{
		if(input)
		{
			newSource = pinSource;
			numActive++;
		}
	}


	void turnAntenna()
	{
		if(m_isRotating)
		{
			if(m_millisecondsWhenRotationEnds < millis())
			{
				if(m_currentRotationDirection == RotationDirection::cw)
					turnCw();
				else
					turnCcw();
			}
		}
	}

	void turnCw()
	{
		if(m_state.antennaAngle == 0)
		{
			m_state.antennaAngle = config::antennaRotationPositions;
		}
		else
		{
			m_state.antennaAngle--;
		}
	}

	void turnCcw()
	{
		if(m_state.antennaAngle >= config::antennaRotationPositions-1)
		{
			m_state.antennaAngle = 0;
		}
		else
		{
			m_state.antennaAngle++;
		}
	}
};

}
