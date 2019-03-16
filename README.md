# PEKS with Bloom Filter
Public Key Encryption with Keyword Search (PEKS) is one of the most used method to search keywords over
encrypted data. Suppose, Bob is sending email with specic keywords to Alice. Encrypted emails are stored
in the server. Alice wants to search emails with keywords from email server but does not want to allow the
server decrypt any email. The paper on PEKS [http://crypto.stanford.edu/~dabo/papers/encsearch.pdf]
described two algorithms to achieve that goal. The rst algorithm takes less time and space compared to the
second. However, the rst one can not guarantee semantic security. The second one is semantically secure. But
dictionary attack can help attackers to guess keywords and pose serious damage. I have resolved that issue using
a Bloom Filter. The false positives of a bloom lter does not allow to make it susceptible to dictionary attack.
In this project, I have implemented the second algorithm of PEKS that originates form trapdoor permutations.
Then I have implemented Bloom Filter that is used to search keywords over the hashmap.
