# Welcome

This is a collection of scripts and bots for Twitter.

## Instructions

1) Get a <i>consumer key, consumer secret, access token, and access token secret</i> from:

https://developer.twitter.com/en/apply-for-access

2) Create a secrets.txt file. In one line, paste all four <i>in order</i> followed by the account you want to work on (also separated by a comma).

Example: asdfdsfafd,2340dfsfd,90u293fjsdf,9fe00w0asdf,someAccount

3) Run the script or executable!

If you have any problems, contact Roly Poly on twitter or via telegram.

## Notes

### the 24 hour rate limit window

You really do have to wait <b>at least 24 hours</b> before running either follower script again. If you follow 400 people between 7:00 am and 7:10 am on Monday, you'll be rate limited ("suspended") until 7:10 am on Tuesday.

### "Friendships/create" aka <i>follows</i>, daily limitation:

https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits

"POST friendships/create; window: 24 hours;	limit per user: 400"

### Daily limit of script usage

My understanding is that the rate limit on follows is separate from all other actions taken by an account.

If that is correct, you can run the follower scripts regardless of your account's other activity for the day.

However, since either one of them will use up all of your follows for the day, you can only use one.


<i>Made for Moneywave.</i>