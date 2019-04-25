#include <cs50.h>
#include <stdio.h>
#include <crypt.h>
#include <string.h>

void CharIncrement(string pass, int depth);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./crack hash");
        return 1;
    }
    string hash = argv[1];
    char salt[] = "AA";
    salt[0] = hash[0];
    salt[1] = hash[1];
//    printf("Salt: %s\n", salt);
    char pass[] = {'A', '\0', '\0', '\0', '\0'};
    while (crypt(pass, salt) != hash/* && pass[1] == '\0'*/)
    {
        CharIncrement(pass, 0);
//        printf("pass: %s, hash: %s\n", pass, crypt(pass, salt));
    }
    printf("%s\n", pass);
    return 0;
}

void CharIncrement(char pass[], int depth)
{
    if ((pass[depth] >= 'A' && pass[depth] < 'Z') || (pass[depth] >= 'a' && pass[depth] < 'z'))
    {
        // increment the character
        pass[depth]++;
        return;
    }
    else if (pass[depth] == 'Z')
    {
        pass[depth] = 'a';
        return;
    }
    else
    {
        pass[depth] = 'A';
        if (pass[depth + 1] == '\0')
        {
            pass[depth + 1] = 'A';
            return;
        }
        else
        {
            CharIncrement(pass, depth + 1);
            return;
        }
    }
}
