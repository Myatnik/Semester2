#include <iostream>
using namespace std;
#pragma once

class Date_time
{
private:
	int To_Julian(const Date_time r);
	Date_time From_Julian(int jdn);
public:
	int day;
	int month;
	int year;

	Date_time();
	Date_time(int day_input, int month_input, int year_input);
	
	Date_time& operator += (const Date_time r);

	friend istream& operator >>(istream& in, Date_time& r);
	friend ostream& operator <<(ostream& out, const Date_time& r);
};
