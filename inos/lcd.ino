/* From Fred Crowson */
#include <Wire.h>
#include <LiquidCrystal.h>

#ifdef __cplusplus
extern "C" {
#endif

LiquidCrystal lcd(7,8,9,10,11,12);

void setup(void) {
	Serial.begin(57600);
	Serial.println("Start");
	lcd.begin(16,2);
	lcd.print("LCD Test Prog");
	lcd.setCursor(0,1);
	lcd.print("Line: 2 ABCDEFG");
	return;
}

void loop(void) {
	/* more of your code here */
	return ;
}

#ifdef __cplusplus
}
#endif
