#include <stdio.h>

int main() {
    int n, i;
    int actualSum = 0, expectedSum, missingNumber;

    printf("Enter number of elements: ");
    scanf("%d", &n);

    int arr[n];

    printf("Enter %d elements (from 0 to %d):\n", n, n);
    for (i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
        actualSum += arr[i];
    }

    expectedSum = n * (n + 1) / 2;
    missingNumber = expectedSum - actualSum;

    printf("Missing number is: %d\n", missingNumber);

    return 0;
}
