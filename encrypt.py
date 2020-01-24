import logging
logger = logging.getLogger(__name__)

def encrypt(key, data):
	if isinstance(data, str):
		data = [ord(d) for d in data]
	assert 0 <= key < 256

	out = []
	for d in data:
		result = key ^ d
		out.append(result)
		logger.info("{} ^ {} = {}".format(key, d, result))
	
	logger.info("result: {}".format(out))
	return out

def format_to_hex(encrypted):
	for e in encrypted:
		assert isinstance(e, int)
	return " ".join("{:02X}".format(e) for e in encrypted)

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	expected = [0b00000110, 0b00001110, 0b01000000, 0b01101011]
	logger.info("expected: {}".format(expected))
	assert encrypt(0x61, "go!\n") == expected
	
	result = format_to_hex(encrypt(0x61, "go!\n"))
	logger.info("result: {}".format(result))
	assert result == "06 0E 40 6B"
	logger.info("test PASS")

"""
Example:
input: go!<LF>
dec		103 111 33 10
key		01100001 01100001 01100001 01100001
binary	01100111 01101111 00100001 00001010
out		00000110 00001110 01000000 01101011
"""
