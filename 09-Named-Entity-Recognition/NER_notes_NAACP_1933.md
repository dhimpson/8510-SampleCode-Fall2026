# NER Notes — NAACP Greenville, S.C. File (1933–1934)

Source transcription: `data/NAACP_1933_Greenville_SC_transcription.txt`
Original: NAACP Papers, Manuscript Division, Library of Congress (34-page PDF)

---

## 1. What the source is

Typed correspondence, January–June 1934, about two Greenville County prosecutions in which the NAACP paid a special prosecutor:

1. **The chain gang case.** Four white guards (H.P. Dill, W.H. Forrester, C.B. Baker,
   Julius Hightower) were indicted for beating Roy Hudson, a Black convict, to death on
   the Greenville County chain gang. The first trial, in March 1934, ended in a mistrial.
   The second, in May 1934, ended in acquittal after Judge Oxner's charge to the jury.
2. **The George Green lynching (November 1933).** Several men were indicted. The trial
   is repeatedly postponed, and the file does not record an outcome.

Most letters are between **Joseph A. Tolbert** (Greenville attorney, former Republican
national committeeman, hired as special prosecutor) and **Roy Wilkins** (NAACP Assistant Secretary, New York).




## NAACP file notes:

# SpaCy run: seemed to have found a lot of items that correlated to the set list from spaCy. However, this does not really help me with identifying what I want to quickly uncover from this file. I do not need to know random ordinal numbers and I already know that the pronoun "I" refers to a person. The output of items that are unnecessary to me is very "noisy" and I do not think Spacy is a good fit for me if there are other tools available that can be tailored to what I am researching. 

# Gliner run: This tool seems to be a better fit for historical research than spacy in that the list of searchable terms can be modified to fit a historian's question. I kept the original list and added "occupation" and "crime". I also kept the threshold at 0.7 for the first run. The first run presented results that were more tailored to the document itself. I can clearly see what people from the NAACP are involved in sending correspondence about the two court cases. I also can clearly locate the two victims of the cases. Geographic locations and organizations seem to be mostly accurate. It does lable "The Committee" as an organization and still picks up on personal pronouns.I thnk raised the threshold to 0.9 and reran. The output list associated "chain gang" as related to "crime" and did not include "mob" as an organization (see the 0.3 run below).

# Gliner run at 0.3 Threshold: Gliner seems to have still captured the most important names. There are a few oddities, like "chain gang" and "mob" being organizations, "both cases" listed as "crime"

# Gemini Run: 
Model: gemini-3.5-flash-lite

Found 314 entities:

  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  George Green                                          PERSON
  George Green                                          PERSON
  Roy Hudson                                            PERSON
  Library of Congress                                   ORGANIZATION
  JOSEPH A. TOLBERT                                     PERSON
  GREENVILLE                                            CITY_OR_TOWN
  S.C.                                                  STATE
  Roy Wilkins                                           PERSON
  N.A.A.C. P.                                           ORGANIZATION
  New York City                                         CITY_OR_TOWN
  Mr. Wilkins                                           PERSON
  George Green                                          PERSON
  Greenville County                                     COUNTY
  Greenville County                                     COUNTY
  Joseph A. Tolbert                                     PERSON
  E. B. Burroughs                                       PERSON
  Charleston                                            CITY_OR_TOWN
  South Carolina                                        STATE
  Dr. Burroughs                                         PERSON
  National Office                                       ORGANIZATION
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  Greenville                                            CITY_OR_TOWN
  George Green                                          PERSON
  South Carolina                                        STATE
  R. Unreadable. Mance                                  PERSON
  Columbia Branch                                       ORGANIZATION
  Columbia                                              CITY_OR_TOWN
  South Carolina                                        STATE
  Dr. Mance                                             PERSON
  National Office                                       ORGANIZATION
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  National Of- fice                                     ORGANIZATION
  South Carolina                                        STATE
  Greenville                                            CITY_OR_TOWN
  Greenville                                            CITY_OR_TOWN
  George Green                                          PERSON
  National Office                                       ORGANIZATION
  South Carolina                                        STATE
  National Office                                       ORGANIZATION
  T. Lester                                             PERSON
  Florence Branch                                       ORGANIZATION
  Florence                                              CITY_OR_TOWN
  South Carolina                                        STATE
  Mr. Lester                                            PERSON
  National Office                                       ORGANIZATION
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  National Of- fice                                     ORGANIZATION
  South Carolina                                        STATE
  Greenville                                            CITY_OR_TOWN
  Greenville                                            CITY_OR_TOWN
  George Green                                          PERSON
  National Office                                       ORGANIZATION
  South Carolina                                        STATE
  National Office                                       ORGANIZATION
  E. C. L. Adams                                        PERSON
  Columbia                                              CITY_OR_TOWN
  South Carolina                                        STATE
  Mr. Adams                                             PERSON
  Mr. White                                             PERSON
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  Greenville                                            CITY_OR_TOWN
  George Green                                          PERSON
  Joseph A. Tolbert                                     PERSON
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  County Solicitor                                      PERSON
  Association                                           ORGANIZATION
  Mr. Tolbert                                           PERSON
  South Carolina                                        STATE
  Mr. White                                             PERSON
  South Carolina                                        STATE
  Greenville                                            CITY_OR_TOWN
  S. C.                                                 STATE
  Roy Wilkins                                           PERSON
  N. A. A. C. P.                                        ORGANIZATION
  New York City                                         CITY_OR_TOWN
  Mr. Wilkins                                           PERSON
  Greenville County                                     COUNTY
  George Green                                          PERSON
  Greenville County                                     COUNTY
  Joseph A. Tolbert                                     PERSON
  Joseph A. Tolbert                                     PERSON
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  Mr. Tolbert                                           PERSON
  Legal Committee                                       ORGANIZATION
  George Green                                          PERSON
  R. B. ELEAZER                                         PERSON
  MRS. JESSIE DANIEL AMES                               PERSON
  E. McNEILL POTEAT, JR.                                PERSON
  M. ASHBY JONES                                        PERSON
  R. H. KING                                            PERSON
  MRS. W. A. NEWELL                                     PERSON
  EMILY H. CLAY                                         PERSON
  J. SHERRARD KENNEDY                                   PERSON
  WILL W. ALEXANDER                                     PERSON
  ARTHUR F. RAPER                                       PERSON
  Commission on Interracial Cooperation                 ORGANIZATION
  703 STANDARD BUILDING                                 FACILITY
  Atlanta                                               CITY_OR_TOWN
  Ga.                                                   STATE
  Roy Wilkins                                           PERSON
  N. A. A. C. P.                                        ORGANIZATION
  New York City                                         CITY_OR_TOWN
  Mr. Wilkins                                           PERSON
  South Carolina                                        STATE
  South Carolina                                        STATE
  Will W. Alexander                                     PERSON
  Dr. Will W. Alexander                                 PERSON
  Committee on Interracial Cooperation                  ORGANIZATION
  703 Standard Building                                 FACILITY
  Atlanta                                               CITY_OR_TOWN
  Georgia                                               STATE
  Dr. Alexander                                         PERSON
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  Joseph A. Tolbert                                     PERSON
  South Carolina                                        STATE
  Mr. Tolbert                                           PERSON
  Greenville                                            CITY_OR_TOWN
  George Green                                          PERSON
  Mr. Tolbert                                           PERSON
  South Caro- lina                                      STATE
  Commission on Interracial Cooperation                 ORGANIZATION
  Mr. Tolbert                                           PERSON
  E. C. L. Adams                                        PERSON
  Columbia                                              CITY_OR_TOWN
  South Carolina                                        STATE
  Mr. Adams                                             PERSON
  Greenville                                            CITY_OR_TOWN
  South                                                 STATE
  E.C.L. Adams                                          PERSON
  Columbia                                              CITY_OR_TOWN
  Unreadable.C.                                         STATE
  Mr. Adams                                             PERSON
  N. J. Frederick                                       PERSON
  Greenville                                            CITY_OR_TOWN
  Joseph A. Tolbert                                     PERSON
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  Mr. Tolbert                                           PERSON
  George Green                                          PERSON
  Luther Hudson                                         PERSON
  Luther Hudson                                         PERSON
  Greenville                                            CITY_OR_TOWN
  Greenville                                            CITY_OR_TOWN
  S. C                                                  STATE
  Joseph A. Tolbert                                     PERSON
  Joseph A. Tolbert                                     PERSON
  Mr. Turner                                            PERSON
  Mr. Wilkins                                           PERSON
  Joseph A. Tolbert                                     PERSON
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  JOSEPH A. TOLBERT                                     PERSON
  GREENVILLE                                            CITY_OR_TOWN
  GREENVILLE                                            CITY_OR_TOWN
  S. C.                                                 STATE
  S. C.                                                 STATE
  Mr. Roy Wilkins                                       PERSON
  Roy Wilkins                                           PERSON
  N. A. C. P.                                           ORGANIZATION
  New York                                              CITY_OR_TOWN
  N. Y.                                                 STATE
  The State of South Carolina                           ORGANIZATION
  H.P. Dill                                             PERSON
  W.H. Forrester                                        PERSON
  C.B. Baker                                            PERSON
  Julius Hightower                                      PERSON
  Mr. Wilkins                                           PERSON
  General Sessions Court for Greenville County          ORGANIZATION
  S. C.                                                 STATE
  Joseph A. Tolbert                                     PERSON
  James A. King                                         PERSON
  Greenville                                            CITY_OR_TOWN
  N. C.                                                 STATE
  Mr. King                                              PERSON
  Greenville                                            CITY_OR_TOWN
  Mr. Joseph A. Tolbert                                 PERSON
  Legal Com- mittee                                     ORGANIZATION
  Joseph A. Tolbert                                     PERSON
  Greenville                                            CITY_OR_TOWN
  S. C.                                                 STATE
  Mr. Tolbert                                           PERSON
  Legal Committee                                       ORGANIZATION
  South Carolina                                        STATE
  H. P. Dill                                            PERSON
  New York Daily News                                   ORGANIZATION
  Asst. Secretary                                       PERSON
  N. A.A. C.P.                                          ORGANIZATION
  New York City                                         CITY_OR_TOWN
  State of South Carolina                               ORGANIZATION
  H.P. Dill                                             PERSON
  Roy Hudson                                            PERSON
  Roy Hudson                                            PERSON
  Mr. Wilkins                                           PERSON
  Greenville                                            CITY_OR_TOWN
  General Sessions Court                                ORGANIZATION
  Joseph A. Tolbert                                     PERSON
  Arthur B. Spingarn                                    PERSON
  New York City                                         CITY_OR_TOWN
  Mr. Spingarn                                          PERSON
  Mr. Joseph A. Tolbert                                 PERSON
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  New York Sunday News                                  ORGANIZATION
  Mr. Tolbert                                           PERSON
  Mr. Tolbert                                           PERSON
  George Green                                          PERSON
  Roy Hudson                                            PERSON
  JOSEPH A. TOLBERT                                     PERSON
  GREENVILLE                                            CITY_OR_TOWN
  S. C.                                                 STATE
  Mr. Roy Wilkins                                       PERSON
  N. A. A. C. P.                                        ORGANIZATION
  N. A. A. C. P.                                        ORGANIZATION
  New York                                              CITY_OR_TOWN
  New York                                              CITY_OR_TOWN
  N.Y.                                                  STATE
  Mr. Wilkins                                           PERSON
  South Carolina                                        STATE
  H.P.Dill                                              PERSON
  Joseph A. Tolbert                                     PERSON
  Joseph A. Tolbert                                     PERSON
  Mr. Joseph A. Tolbert                                 PERSON
  Greenville                                            CITY_OR_TOWN
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  Mr. Tolbert                                           PERSON
  Legal Committee                                       ORGANIZATION
  Legal Committee                                       ORGANIZATION
  South Carolina                                        STATE
  South                                                 STATE
  H. P. Dill                                            PERSON
  Committee                                             ORGANIZATION
  Committee                                             ORGANIZATION
  Solicitor's Office                                    ORGANIZATION
  Committee                                             ORGANIZATION
  Mr. Joseph A. Tolbert                                 PERSON
  Greenville                                            CITY_OR_TOWN
  South Carolina                                        STATE
  Mr. Tolbert                                           PERSON
  South Carolina                                        STATE
  H. P. Dill                                            PERSON
  JOSEPH A. TOLBERT                                     PERSON
  GREENVILLE                                            CITY_OR_TOWN
  S. C.                                                 STATE
  S. C.                                                 STATE
  Mr. Roy Wilkins                                       PERSON
  Mr. Roy Wilkins                                       PERSON
  N.A.A. C. P.                                          ORGANIZATION
  New York                                              CITY_OR_TOWN
  N.Y.                                                  STATE
  State of South Carolina                               ORGANIZATION
  H. P. Dill                                            PERSON
  Mr. Wilkins                                           PERSON
  legal committee                                       ORGANIZATION
  Joseph A. Tolbert                                     PERSON
  Greenville                                            CITY_OR_TOWN
  National Asso. for the Advancement of Colored People  ORGANIZATION
  New York                                              CITY_OR_TOWN
  N.Y.                                                  STATE
  The State of South Carolina                           ORGANIZATION
  H.P. Dill                                             PERSON
  H.P. Dill                                             PERSON
  W.H.Forrester                                         PERSON
  C.B.Baker                                             PERSON
  Julius Hightower                                      PERSON
  Roy Hudson                                            PERSON
  Greenville County                                     COUNTY
  Mr. Turner                                            PERSON
  Joseph A. Tolbert                                     PERSON
  State                                                 ORGANIZATION
  H. P. Dill                                            PERSON
  JOSEPH A. TOLBERT                                     PERSON
  GREENVILLE                                            CITY_OR_TOWN
  S. C.                                                 STATE
  Mr. Roy Wilkins                                       PERSON
  N.A.A. C. P.                                          ORGANIZATION
  New York                                              CITY_OR_TOWN
  N.Y.                                                  STATE
  South Carolina                                        STATE
  H.P. Dill                                             PERSON
  Mr. Wilkins                                           PERSON
  Court of General Sessions                             ORGANIZATION
  Greenville                                            CITY_OR_TOWN
  S. C.                                                 STATE
  State                                                 ORGANIZATION
  Statutes of South Carolina                            ORGANIZATION
  Judge Oxner                                           PERSON
  Legal Committee                                       ORGANIZATION
  Mr. Joseph A. Tolbert                                 PERSON
  Greenville                                            CITY_OR_TOWN
  S.C.                                                  STATE
  S.C.                                                  STATE
  JOSEPH A. TOLBERT                                     PERSON
  GREENVILLE                                            CITY_OR_TOWN
  S. C.                                                 STATE
  Mr. Roy Wilkins                                       PERSON
  N. A. A. C. P.                                        ORGANIZATION
  New York                                              CITY_OR_TOWN
  N. Y.                                                 STATE
  N. Y.                                                 STATE
  South Carolina                                        STATE
  H. P. Dill                                            PERSON
  Mr. Wilkins                                           PERSON
  Mr. Wilkins                                           PERSON
  Joseph A. Tolbert                                     PERSON

Saved output/03_gemini.csv and output/03_gemini.html

Every entity was found word for word in the source.

Tokens: 9,354 in, 8,045 out   Cost: $0.022919