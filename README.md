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


Pitch:
Most bikeshare users don’t realize they’re leaving free rides on the table — not because the system is bad, but because navigation isn’t optimized for how pricing actually works.

Relay fixes that.

Relay is a real-time bikeshare navigation app built for Indianapolis that turns one long ride into a series of perfectly timed, free segments. We tap directly into Pacers Bikeshare’s live GBFS data, model the entire network as a graph, and compute routes that guarantee every ride stays under the 30-minute free pass window.

Instead of “fastest route,” we optimize for zero cost.

So what would normally be a $10+ trip becomes completely free — just by intelligently choosing when and where to dock and continue.

Under the hood, we’re combining:

Real-time station availability
Constraint-based shortest path routing (NetworkX)
And Mapbox-powered directions for seamless navigation

The result is a multi-hop route that feels natural to the user but is algorithmically optimized behind the scenes.

This isn’t just a convenience feature — it’s a new way to think about urban mobility:
price-aware routing, not just distance-aware routing.

And while we’re starting with Indianapolis, this model scales to any city with GBFS-compatible bikeshare systems worldwide.

Relay turns bikeshare from “cheap transportation” into truly free transportation — intelligently.
