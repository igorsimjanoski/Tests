### This is repository for automatic UI tests using selenium

    Scripts: bin/test_goeuro.py - this script is checking that sorting by price is correct
    Usage: ./test_goeuro.py

    Test is using firefox driver. FLow is like this:
    -open browser
    -insert text into to/from fields
    -click on search
    -wait until results are ready(this can be tricky, in this case test check for class attribute on one of elements to change to specific value)
    -extract price from results
    -check if results are sorted
    -close browser
