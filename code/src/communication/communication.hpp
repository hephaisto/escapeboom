#include "../config.hpp"

#include "state.hpp"

namespace communication
{

class Communication
{
public:
	Communication(State &state, HardwareInput &input, HardwareOutput &output)
	:m_state{state}
	,m_input{input}
	,m_output{output}
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
	HardwareInput &m_input;
	HardwareOutput &m_output;

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

		setSource(newSource, Source::off, m_input.off, numActive);
		setSource(newSource, Source::morse, m_input.crypt, numActive);
		setSource(newSource, Source::aux, m_input.aux, numActive);
		setSource(newSource, Source::plain, m_input.plain, numActive);
		setSource(newSource, Source::microphone, m_input.microphone, numActive);
		setSource(newSource, Source::boardCom1, m_input.boardCom1, numActive);
		setSource(newSource, Source::boardCom2, m_input.boardCom2, numActive);

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
		if(m_state.turning)
		{
			if(m_millisecondsWhenRotationEnds < millis()) // rotation ended
			{
				if(m_currentRotationDirection == RotationDirection::cw)
					turnCw();
				else
					turnCcw();
				m_state.turning = false;
			}
		}
		else
		{
			checkRotationInputs();
		}
		m_output.motorActive = m_state.turning;
	}

	void checkRotationInputs()
	{
		if( (m_input.antennaCw) && (m_input.antennaCcw) )
		{
			m_state.turning = false;
			m_output.motorMalfunction = true;
		}
		else if( (m_input.antennaCw) && (!m_input.antennaCcw))
		{
			m_state.turning = true;
			m_currentRotationDirection = RotationDirection::cw;
			m_millisecondsWhenRotationEnds = millis() + config::millisecondsForOneAntennaRotation;
		}
		else if( (!m_input.antennaCw) && (m_input.antennaCcw))
		{
			m_state.turning = true;
			m_currentRotationDirection = RotationDirection::ccw;
			m_millisecondsWhenRotationEnds = millis() + config::millisecondsForOneAntennaRotation;
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
