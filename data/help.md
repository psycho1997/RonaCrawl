**TrashBot by PsYcHo**
```
- !help             display this message
- !country [name]   responds with ISO 3166-1 alpha-2 code for the Country
- !git              displays repo information
- !tex [LaTex]*       Renders a short LaTeX equation (one line only)
- !rona [atribute] [date]* [country]**
    responds with the requested data:
    -> attribute: 
        + STATS     Usage:  !rona STATS [single Country]
                    Displays the current data of country

        + NEWCASES  Usage:  !rona NEWCASES [Date]* [Country]**
                    Displays the number of cases for every datapoint
        
        + DEATHS    Usage:  !rona DEATHS [Date]* [Country]**
                    Displays the number of Deaths (Total)

        + CASES     Usage:  !rona CASES [Date]* [Country]**
                    Displays the number of CASES (Total)

    -> date:        Optional. In format MM.YY doesnt work with STATS
    
    -> country:     For STATS only one country, else at least one Country 
                    in ISO 3166-1 alpha-2 code (see !country)

- !add              Adds one country to the last graph

                

```
