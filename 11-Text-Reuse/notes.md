# notes on test run with 01_reuse_jaccard_by_hand 
Terminal output:
python 01_reuse_jaccard_by_hand.py
A: 'honorary members shall not exceed the proportion of one to twentyfive active members and shall consist of persons well known as patrons of physical education they shall be nominated by the council and require a twothirds vote of the members present to elect'
B: 'honorary members shall not exceed the proportion of one to twentyfive active members and shall consist of persons well known as patrons of physical education they shall be nominated by the executive committee and require a twothirds vote of the members present to elect'

# ngram set at 5 : Word 5-grams
  A (39): ['a twothirds vote of the', 'active members and shall consist', 'and require a twothirds vote', 'and shall consist of persons', 'as patrons of physical education', 'be nominated by the council', 'by the council and require', 'consist of persons well known', 'council and require a twothirds', 'education they shall be nominated', 'exceed the proportion of one', 'honorary members shall not exceed', 'known as patrons of physical', 'members and shall consist of', 'members shall not exceed the', 'nominated by the council and', 'not exceed the proportion of', 'of one to twentyfive active', 'of persons well known as', 'of physical education they shall', 'of the members present to', 'one to twentyfive active members', 'patrons of physical education they', 'persons well known as patrons', 'physicaleducation they shall be', 'proportion of one to twentyfive', 'require a twothirds vote of', 'shall be nominated by the', 'shall consist of persons well', 'shall not exceed the proportion', 'the council and require a', 'the members present to elect', 'the proportion of one to', 'they shall be nominated by', 'to twentyfive active members and', 'twentyfive active members and shall', 'twothirds vote of the members', 'vote of the members present', 'well known as patrons of']
  B (40): ['a twothirds vote of the', 'active members and shall consist', 'and require a twothirds vote', 'and shall consist of persons', 'as patrons of physical education', 'be nominated by the executive', 'by the executive committee and', 'committee and require a twothirds', 'consist of persons well known', 'education they shall be nominated', 'exceed the proportion of one', 'executive committee andrequire a', 'honorary members shall not exceed', 'known as patrons of physical', 'members and shall consist of', 'members shall not exceed the', 'nominated by the executive committee', 'not exceed the proportion of', 'of one to twentyfive active', 'of persons well known as', 'of physical education they shall', 'of the members present to', 'one to twentyfive active members', 'patrons of physical education they', 'persons well known as patrons', 'physical education they shall be', 'proportion of one to twentyfive', 'require a twothirdsvote of', 'shall be nominated by the', 'shall consist of persons well', 'shall not exceed the proportion', 'the executive committee and require', 'the members present to elect', 'the proportion of one to', 'they shall be nominated by', 'to twentyfive active members and', 'twentyfive active members and shall', 'twothirds vote of the members', 'vote of the members present', 'well known as patrons of']
  shared (34): ['a twothirds vote of the', 'active members and shall consist', 'and require a twothirds vote', 'and shall consist of persons', 'as patrons of physical education', 'consist of persons well known', 'education they shall be nominated', 'exceed the proportion of one', 'honorary members shall not exceed', 'known as patrons of physical', 'members and shall consist of', 'members shall not exceed the', 'not exceed the proportion of', 'of one to twentyfive active', 'of persons well known as', 'of physical education they shall', 'of the members present to', 'one to twentyfive active members', 'patrons of physical education they', 'persons well known as patrons', 'physical education they shall be', 'proportion of one to twentyfive', 'require a twothirds vote of', 'shall be nominated by the', 'shall consist of persons well', 'shall not exceed the proportion', 'the members present to elect', 'the proportion of one to', 'they shall be nominated by', 'to twentyfive active members and', 'twentyfive active members and shall', 'twothirds vote of the members', 'voteof the members present', 'well known as patrons of']
  Jaccard = 34 shared / 45 total = 0.76 
  # computed by dividing total shared n-grams from both passages with total ngrams in all.

  # Shingles: character 5-shingles
  A had 231 shingles 
  B had 242 shingles
  Shared between A and B: 220 shingles
  Jaccard = 220 shared / 253 total (every different shingle that appears in either text, counted once. You get it by adding both texts’ shingles and subtracting the overlap so the shared ones aren’t counted twice: 231 + 242 − 220 = 253) = 0.87
  Jaccard = 220 / 253 = 0.87

Other notes: CLEAN prevented any capitalizaton differences or dashes from being counted as extra differences between texts. 

# Raised Ngram to 7 and reran. The N-gram results were:
A = 37
B = 38
Jaccard = 30 shared/ 45 total = 0.67 
# higher ngrams makes it harder to located shared words. A 7 word phrase that matches within text is tough to find without breaking the ngram.

# Set Ngram at 3 and ran again
A = 41
B = 42
Shared = 38
Jaccard = 38 shared / 45 total= 0.84

# set Ngram to 4 and reran
A = 40
B = 41
Shared = 36
Jaccard= 0.80

# ngram = 6 yielded a jaccard score of 0.87 same as N=5.