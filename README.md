🚴 Relay

Relay is a program real-time bikeshare data from GBFS feeds and intelligently optimizes bike routes to maximize usage of the Indy Rides Free Pass from the Pacers Bikeshare program.

🚀 Overview

Relay is designed to make urban biking in Indianapolis more efficient and cost-effective by leveraging:

GBFS (General Bikeshare Feed Specification) data for real-time station and bike availability
Route optimization logic to maximize free ride eligibility
Smart decision-making to help users avoid overage charges

The API acts as the brain behind a potential frontend app, handling all computation, data aggregation, and optimization.

🧠 Core Idea

The Indy Rides Free pass allows riders to take trips under a certain time limit for free. Relay optimizes routes by:

Breaking longer trips into multiple valid segments
Routing through strategically placed docking stations
Ensuring each segment stays within the free ride window
