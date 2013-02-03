#bid increments
MIN_BID_VALUE = 1
MIN_BID_INCREMENT = 1

#UFA
UFA_3_YEAR_DISCOUNT_MAX = 5
UFA_5_YEAR_DISCOUNT_MAX = 8
UFA_DISCOUNT_MAX_DEFAULT = UFA_3_YEAR_DISCOUNT_MAX

#auction states
NONE = 0 #not yet categorized or invalid
UPCOMING = 1 #auction is scheduled and has yet to start
LIVE = 2 #auction is live and may be bid on
PENDING = 3 #auction is finished, but waiting on owner actions (e.g. RFA match/decline)
COMPLETED = 4 #auction is completed - rosterplayer is created
