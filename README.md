**🚴 Relay**
Smart bikeshare routing for Indianapolis — powered by Pacers Bikeshare GBFS data

**What is Relay?**
Relay is a real-time urban bikeshare navigation app built for Indianapolis. It streams live station data from the GBFS feed and uses a custom graph-based routing algorithm to break long trips into free-ride segments — keeping every leg under the Indy Rides Free Pass 30-minute window.
Think of it as Google Maps meets Pacers Bikeshare, optimized for people who want to ride for free.

**How It Works**
The Pacers Bikeshare free pass lets riders take trips under a time limit at no cost. Relay exploits this by:

 - Fetching real-time station availability from the GBFS feed
 - Building a weighted graph of the bikeshare network using NetworkX
 - Running a shortest-path algorithm that respects the MAX_RIDE_KM = 7.5 constraint (~25-minute ride buffer)
 - Returning a multi-hop route — walk to station → bike → dock → walk to station → bike → dock → ... walk to destination
 - Enriching each segment with turn-by-turn directions via the Mapbox Directions API
