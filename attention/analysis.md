# Analysis

## Layer 3, Head 10

The tokens here appear to pay attention to the tokens that follows them.


Example Sentences:
**Input Text:** - The police dog was [MASK] very fast across the street to catch the thief.
- The police dog was running very fast across the street to catch the thief.
- The police dog was moving very fast across the street to catch the thief.
- The police dog was coming very fast across the street to catch the thief.

## Layer 4, Head 10

This attention head is capturing grammatical dependencies, necessary for sentence understanding. 

Ex: **(Token x) - high attention score - (Token y)**

- "The" - Dog and Police - Dog -> The model is grouping determiners and modifiers with their head noun to assemble the subject "The police dog".

- [Mask] - fast and [Mask] - very -> Related the [Mask] token to its surrounding adverbs, seeking context. 

- Across - street and the - street -> Connects prepositions and their objects, and determiners to nouns. Helps stabilize location and context for the action.

- catch - thief and the - thief -> The verb points to its object and the determiner points to the the noun. Attention in identifying the action - catching the thief.


Example Sentences:
**Input Text:** - The police dog was [MASK] very fast across the street to catch the thief.
- The police dog was running very fast across the street to catch the thief.
- The police dog was moving very fast across the street to catch the thief.
- The police dog was coming very fast across the street to catch the thief.



## Layer 6, Head 7

The token *street* is paying attention strongly to the token *across*. This demonstrates the hability of the attention head to identify Adpositions, the class of words that are used to express spatial or temporal relations, or mark various semantic roles.

Example Sentences:
**Input Text:** - The police dog was [MASK] very fast across the street to catch the thief.
- The police dog was running very fast across the street to catch the thief.
- The police dog was moving very fast across the street to catch the thief.
- The police dog was coming very fast across the street to catch the thief.