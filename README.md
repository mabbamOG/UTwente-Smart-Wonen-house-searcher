# UTwente-Smart-Wonen-house-searcher
this program finds the closest housing (rooms) to UTWENTE on smart-wonen

## BUGS
- the addresses are encoded in google maps api queries. i extract the queries with regex but it is unstable as hell. So i advice checking all houses that have been put as last (farthest) because if you see 100km distance it probably is wrong. error probability currently 1/75
