// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

unsigned int DICTIONARY_SIZE = 0;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
        node *toinsert = malloc(sizeof(node));
        if (!toinsert)
        {
            printf("Out of memory\n");
            return 1;
        }
        strcpy(toinsert->word, word);
        toinsert->next = NULL;
        unsigned int index = hash(word);
        node *insert = hashtable[index];
        if (insert)
        {
            toinsert->next = insert;
        }
        hashtable[index] = toinsert;
        DICTIONARY_SIZE++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO

    return DICTIONARY_SIZE;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    unsigned int index = hash(word);
    node *to_check = hashtable[index];
    bool isequal = false;
    while (to_check)
    {
        if (strlen(to_check->word) != strlen(word))
        {
            isequal = false;
            to_check = to_check->next;
        }
        else
        {
            for (int i = 0; to_check->word[i] != '\0' && word[i] != '\0'; i++)
            {
                if (tolower(to_check->word[i]) != tolower(word[i]))
                {
                    isequal = false;
                    to_check = to_check->next;
                    break;
                }
                else
                {
                    isequal = true;
                }
            }
            return true;
        }
    }
    return isequal;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    if (!size())
    {
        return false;
    }
    else
    {
        for (int i = 0; i < N; i++)
        {
            node *cross = hashtable[i];
            while (cross)
            {
                node *tmp = cross;
                cross = cross->next;
                free(tmp);
                DICTIONARY_SIZE--;
            }
        }
        return true;
    }
}
