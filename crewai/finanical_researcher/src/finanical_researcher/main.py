 #!/usr/bin/env python

import sys
import warnings

from datetime import datetime

from finanical_researcher.crew import FinanicalResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



def run():
    """
    Run the crew.
    """
    inputs = {
        'company': 'tesla',
        
    }

    try:
       results =  FinanicalResearcher().crew().kickoff(inputs=inputs)
       print(results.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if  __name__ == "__main__":
    
    run()
