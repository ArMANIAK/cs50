#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Input a non-negative number which is less than 24: ");
    }
    while (n < 0 || n > 24);
    for (int i = 0; i < n; i++)
    {
        int spaces = n -1 - i;
        int asterisks = i + 1;
        for (int j = 0; j < spaces; j++)
        {
            printf(" ");
        }
        for (int k = 0; k < asterisks; k++)
        {
            printf("#");
        }
        printf("  ");
        for (int k = 0; k < asterisks; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}