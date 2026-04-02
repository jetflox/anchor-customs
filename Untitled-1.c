#include <stdio.h>

int main() {
    int daysInMonth[12] = {
        31, 28, 31, 30, 31, 30,
        31, 31, 30, 31, 30, 31
    };

    char *months[12] = {
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    };

    int secondSaturday = 13;   // January's second Saturday

    for (int i = 0; i < 12; i++) {
        printf("Second Saturday of %s is on: %d\n",
               months[i], secondSaturday);

        // Calculate for next month
        secondSaturday += daysInMonth[i] % 7;

        // Adjust if date exceeds days in next month
        if (i < 11 && secondSaturday > daysInMonth[i + 1]) {
            secondSaturday -= daysInMonth[i + 1];
        }
    }

    return 0;
}

 Adjust if date exceeds next month days
   if (i < 11 && secondSaturday > daysInMonth[i + 1]) {
            secondSaturday -= daysInMonth[i + 1];