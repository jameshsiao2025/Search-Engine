This project is for CS121/IN4MATX 141 Information Retrieval Class at UC, Irvine. 

The author are Yiwen "Sarina" Chen, James Hsiao, Tristin Proctor

The following dependencies/libraries are used for the project
{
    'spacy' : @version 3
    (installation guide: https://spacy.io/usage )

    import os
    import json
    import codecs
    import math
    import re
    from bs4 import BeautifulSoup
    from collections import defaultdict
    from defaultlist import defaultlist
    import math
    import webbrowser
    from tkinter import *


}


The project code files are listed below 
    1. Main.py
        -this file is used for running the query and the GUI. The file path on line 42 needs to be changed to match the chrome installation location,
         and 173 and 174 should be set to the index files path.
         - SpaCy libraries are needed to use
    2.Index.py
        -this file was used for indexing. SpaCy libraries are needed to use. See dependencies above. Line 42 should be set to bookkeeping.json file path.dependencies
            line 43 is file path for corpus 

We used findall to find specific tags. This was to prevent searching in-tag attributes or text in html, for instance href. We included tags
like <p> <title> <h1> <h2> <h3> and <li>. These are the tags that exist in the text but not in other form such as in the attribute of the tags.