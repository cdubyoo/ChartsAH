# ChartsAH

Live on : https://chartsah.herokuapp.com/

Site built using django framework

- Landing Page
  - short description of site purpose
  - team information at bottom

- User System
  - register
  - login
  - log out
  - upload profile picture 
  - users are able to set and edit their bio
  - ability to update profile pic and password
  - able to request password reset via email
  
- Posts
  - users are able to create posts
  - includes image, text, tags, date
  - ability for users to edit and delete their own post 
  
- Comments
  - users are able to comment on posts
  - users are able to delete their own comments
  - post owner are able to delete any comments off of their post
  
- Upvotes
  - users are able to upvote posts
  - upvotes are used to sort posts
  
- Feeds
  - main feeds shows all recent trades, ability to sort by most upvoted by day/week/month/year/all
  - custom feed with posts only by users followed

- Sidebar
  - side bar includes the top 5 most posted tickers on the day
  
- Follow System
  - users are able to follow and unfollow each other
  - follows are used to filter custom feed

- Search
  - users are able to search via the quick search bar which searches for user/ticker/tags
  - or via the advanced search where they can filter for their query through specific user/ticker/tag/date(or date range)

- Message
  - users are able to message each other
  - message page will display recent conversations with the last message sent or received
  
- Notifications
  - users are notified when they receive a comment on their post, if someone started following them, or if someone messaged them
  - ability to delete specific notification or clear all at once
  
- Contact
  - users are able to contact owner through contact form which goes to owner's email
