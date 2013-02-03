#bid increments
MIN_BID_VALUE = 1
MIN_BID_INCREMENT = 1

#auction states
NONE = 0 #not yet categorized or invalid
UPCOMING = 1 #auction is scheduled and has yet to start
LIVE = 2 #auction is live and may be bid on
PENDING = 3 #auction is finished, but waiting on owner actions (e.g. RFA match/decline)
COMPLETED = 4 #auction is completed - rosterplayer is created
