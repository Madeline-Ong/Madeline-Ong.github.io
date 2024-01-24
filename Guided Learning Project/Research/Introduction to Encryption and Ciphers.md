# Intro
As I started this project my Learning Facilitator asked me, what is a cipher and I realised I did not even know how to describe it. So I started my research on what a cipher is.


## History & Their Importance
The first cipher was created by Julius Caesar in times of war where information needed to be kept secret so that even if the enemy got their hands on the message, they would not be able to understand it. Even now, encryption is used to secure sensitive information before it is sent over modern communication. 
An example of how important ciphers are, is when Alan Turing cracked the German's Enigma cipher, which was a significant factor leading to the German's defeat. As the decryption of German communications provided the Allies with crucial information about German military plans, strategies, and activities.

- [Types of Encryption Methods] (#encrypt_mtd)
  - [Substitution Ciphers](#substitution)
  - [Transposition Ciphers]
  - [Digraph cipher]
  - [Symmetric Key Encryption]
  - [Asymmetric Key Encryption]
  - [Hashing]
- [Cipher Cracking] (#cipher_cracking)
  - [Frequency Analysis]
  - [Pattern Recognition]
  - [Difficult to Reverse Mathematical Operations]
- [Making Ciphers Hard to Crack]
  - [Trapdoor functions]
  - [More Characters or Mapping Multiple Characters to 1 Plaintext Character]

<a name="encrypt_mtd"></a>
# Types of Encryption Methods
<a name="substitution"></a>
## Substitution Ciphers 
### Monoalphabetical Ciphers
Generally, a simple one-to-one mapping of letters is used. For example, each 'A' in the plaintext is replaced by the same letter in the ciphertext.

Examples include: 
* Caesar Cipher: (Also known as Shift or Rotation Cipher) Each letter in the plaintext is shifted by a fixed number of positions (also called the key) down the alphabet. For example, if the key is 3, 'A' in the plaintext would be 'D' in the ciphertext. 
* Atbash Cipher: The alphabet is reversed such that A becomes Z, etc.
* Affine Cipher: Each letter is mapped to its numeric equivalent, multiplied by a constant, and then shifted by another constant.
* Pigpen Cipher: Letters are replaced with symbols.
* Templar Cipher:
* Mixed Alphabet Cipher: Each letter is replaced by a corresponding letter from a mixed-up or randomly generated alphabet.
  * Vatsyayana Cipher: 26 letters paired into 13 pairs, substitution using those pairs. 

## Transposition Ciphers
Examples include:
* Rail Fence Cipher: (Also known as Zigzag cipher)
The plaintext is written in a zigzag pattern across a set number of rails of the fence (which are the lines) and then each line of text (each rail) is appended to the ciphertext. 

The characters would start going downwards and diagonally across the rails and at the bottom, move upwards and diagonally across. 

The cipher would read: 

Spacing is optional in the ciphertext as it would not be related to the spacing in the plaintext and would not give away any information. However, the ciphertext is split into groups of 5 using spacing so that the ciphertext is more readable. 

* Columnar Transposition


* Scytale
is a simple version of matrix transposition cipher
set number of columns
and in 


### Homophonic Ciphers
Multiple ciphertext characters can be used to represent a single plaintext character. This introduces ambiguity and makes frequency analysis more challenging.

#### Polygraphic Ciphers
* Hill Cipher 
* Playfair Cipher (digraph cipher)

### Polyalphabetical Ciphers

* Vigenère Cipher
* Autokey Cipher



## Symmetric Key Encryption
A single key is used to encrypt and decrypt. Symmetric keys are usually 128 or 256 bits long. The longer the key, the harder it is to crack. For example, a 128-bit key has around 340,000,000,000,000,000,000,000,000,000,000,000,000 encryption code possibilities. This makes brute force attacks more time-consuming and it becomes a less realistic approach to crack such a key.

### Data Encryption Standard (DES)

### Advanced Encryption Standard (AES)


## Asymmetric Key Encryption
Use of public-private key pairing such that data that has been encrypted with the public key can only be decrypted using the private key. The sender and recipient would have their own unique public-private key pair. As the name of the keys implies, the public key is shared openly, while the private key is kept confidential.

### Rivest–Shamir–Adleman (RSA)

### Elliptic Curve Cryptography (ECC) 

## Hashing
Meant to be a one-way encryption to secure data. 
### Salting
Adding a unique value (salt) to the data before hashing, enhances security by preventing precomputed attacks.

<a name="cipher_cracking"></a>
# Cipher Cracking
## Frequency Analysis
It is typically used to break substitution ciphers. It studies the frequency of letters or groups of letters in the ciphertext, based on the fact that in any written language, certain letters and combinations of letters occur with varying frequencies. For example in the English language, the letters E, T, A, and O are the most common. 
One would identify the most often occurring letters in the ciphertext and theorise which letters those in the ciphertext are mapped to. They may then be able to recognise patterns or words in the partially decoded text to identify more letters. 

## Pattern Recognition 
Identifying patterns in ciphertext can provide insights into the underlying structure of a substitution or transposition cipher.

## Mathematical Operations that are difficult to reverse 
Matrix 


# How to make cipher harder to crack
## Trapdoor functions
They refer to operations that are easy to calculate in one direction but difficult to reverse without special knowledge. 

## Introducing more characters or mapping multiple characters to a plaintext character
