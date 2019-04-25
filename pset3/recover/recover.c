#include <stdio.h>
#include <stdint.h>
#include <cs50.h>
#include <stdlib.h>

bool IsJpeg(uint8_t *ptr);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    char *outfile = argv[1];

    // open input file
    FILE *outptr = fopen(outfile, "r");
    if (outptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", outfile);
        return 2;
    }
    int count = 0;
    uint8_t *buffer = malloc(sizeof(uint8_t) * 512);

    char *infile = malloc(sizeof(char) * 8);
    sprintf(infile, "%.03i.jpg", count++);
    FILE *inptr = fopen(infile, "a");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    bool isStarted = false;
    while (fread(buffer, 512, 1, outptr) == 1)
    {
        if (IsJpeg(buffer))
        {
            if (!isStarted)
            {
                fwrite(buffer, 512, 1, inptr);
                isStarted = true;
            }
            else
            {
                fclose(inptr);
                sprintf(infile, "%.03i.jpg", count++);
                inptr = fopen(infile, "a");
                if (inptr == NULL)
                {
                    fprintf(stderr, "Could not open %s.\n", infile);
                    return 2;
                }
                fwrite(buffer, 512, 1, inptr);
            }
        }
        else if (isStarted)
        {
            fwrite(buffer, 512, 1, inptr);
        }
    }
    fclose(inptr);
    fclose(outptr);
    free(infile);
    free(buffer);
    return 0;
}

bool IsJpeg(uint8_t *ptr)
{
    if (ptr[0] == 0xff && ptr[1] == 0xd8 && ptr[2] == 0xff &&
        (ptr[3] & 0xf0) == 0xe0)
    {
        return true;
    }
    else
    {
        return false;
    }
}