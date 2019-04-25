// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;

//Size counter initialization
int DICTIONARY_SIZE = 0;

void clear_node(node *node)
{
    if (node->is_word)
    {
        DICTIONARY_SIZE--;
    }
    for (unsigned int i = 0; i < N; i++)
    {
        if (node->children[i])
        {
            clear_node(node->children[i]);
        }
    }
    free(node);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        return false;
    }
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
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

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
//        printf("%s\n", word);
        node *new_word = root;
        int n = strlen(word);
        for (unsigned int i = 0; word[i] != '\0'; i++)
        {
            node *to_check = (word[i] == '\'') ? new_word->children[26] : new_word->children[tolower(word[i]) - 'a'];
            if (to_check == NULL)
            {
                to_check = malloc(sizeof(node));
                if (to_check == NULL)
                {
                    return false;
                }
                to_check->is_word = false;
                for (int j = 0; j < N; j++)
                {
                    to_check->children[j] = NULL;
                }
                if (word[i] == '\'')
                {
                    new_word->children[26] = to_check;
                }
                else
                {
                    new_word->children[tolower(word[i]) - 'a'] = to_check;
                }
            }
            if (i + 1 == n)
            {
                to_check->is_word = true;
                DICTIONARY_SIZE++;
            }
            new_word = to_check;
        }
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
    node *to_check = root;
    for (unsigned int i = 0, n = strlen(word); i < n; i++)
    {
        to_check = (word[i] == '\'') ? to_check->children[26] : to_check->children[tolower(word[i]) - 'a'];
        if (to_check == NULL)
        {
            return false;
        }
        else
        {
            if (i + 1 == n)
            {
                return to_check->is_word;
            }
        }
    }
    return to_check->is_word;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    if (root)
    {
        clear_node(root);
        return true;
    }
    return false;
}
