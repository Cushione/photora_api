[Go to README](README.md)

Screenshots of some unauthorised unsafe request were taken in the local deployment because they cause an application error in the production deployment [Go to bugs](README.md#bugs)

| Testcase                                                                     | Expected Result                                                                                             | Test Result | Screenshots                                                              |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------ |
| **Profiles**                                                                 |                                                                                                             |             |                                                                          |
| _[Profile List](https://photora-api.herokuapp.com/profiles)_                 |                                                                                                             |             |
| GET Unauthenticated                                                          | returns 200 response: a list of all the profiles                                                            | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-profiles.png)                |
| GET Authenticated                                                            | returns 200 response: a list of all the profiles                                                            | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-profiles.png)                  |
| POST, PUT, DELETE                                                            | Not provided                                                                                                | ✅ PASS     |
| _[Profile Detail](https://photora-api.herokuapp.com/profiles/8)_             |                                                                                                             |             |
| GET Unauthenticated                                                          | returns 200 response: the profile specified by id                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-profiles-detail.png)         |
| GET Authenticated                                                            | returns 200 response: the profile specified by id                                                           | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-profiles-detail.png)           |
| POST, PUT, DELETE                                                            | Not provided                                                                                                | ✅ PASS     |
| _[Profile Follow](https://photora-api.herokuapp.com/profiles/8/followers)_   |                                                                                                             |             |
| GET Unauthenticated                                                          | returns 403 Forbidden error                                                                                 | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-profiles-followers.png)      |
| GET Authenticated                                                            | returns 200 response: a list of profiles following the specified profile                                    | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-profiles-followers.png)        |
| POST Authenticated                                                           | returns 201 or 204 response: allows authenticated users to follow the specified profile                     | ✅ PASS     | [Screenshot](docs/tests/authenticated-post-profiles-followers.png)       |
| POST Unauthenticated                                                         | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-post-profiles-followers.png)     |
| PUT, DELETE                                                                  | Not provided                                                                                                | ✅ PASS     |
| _[User Profile](https://photora-api.herokuapp.com/profiles/user)_            |                                                                                                             |             |
| GET Authenticated                                                            | returns 200 response: returns the profile of the requesting user                                            | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-profiles-user.png)             |
| GET Unauthenticated                                                          | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-profiles-user.png)           |
| PUT Authenticated                                                            | returns 200 response: allows authenticated users to update their profile                                    | ✅ PASS     | [Screenshot](docs/tests/authenticated-put-profiles-user.png)             |
| PUT Unauthenticated                                                          | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-put-profiles-user.png)           |
| POST, DELETE                                                                 | Not provided                                                                                                | ✅ PASS     |
| **Posts**                                                                    |                                                                                                             |             |                                                                          |
| _[Post List](https://photora-api.herokuapp.com/posts)_                       |                                                                                                             |             |
| GET Unauthenticated                                                          | returns 200 response: returns a list of all the posts                                                       | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-posts.png)                   |
| GET Authenticated No Follow                                                  | returns 200 response: Filters out the posts from the requesting user                                        | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-posts.png)                     |
| GET Authenticated With Follow                                                | returns 200 response: Filters out the posts from the requesting user and from the profiles the user follows | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-posts-follow.png)              |
| POST Authenticated                                                           | returns 201 response: allows authenticated users to create posts                                            | ✅ PASS     | [Screenshot](docs/tests/authenticated-post-posts.png)                    |
| POST Unauthenticated                                                         | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-post-posts.png)                  |
| PUT, DELETE                                                                  | Not provided                                                                                                | ✅ PASS     |
| _[Post Detail](https://photora-api.herokuapp.com/posts/12)_                  |                                                                                                             |             |
| GET Unauthenticated                                                          | returns the post specified by id                                                                            | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-posts-detail.png)            |
| GET Authenticated                                                            | returns the post specified by id                                                                            | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-posts-detail.png)              |
| PUT Authenticated Owner                                                      | allows the owner to update the post                                                                         | ✅ PASS     | [Screenshot](docs/tests/authenticated-owner-put-posts-detail.png)        |
| PUT Authenticated Not Owner                                                  | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/authenticated-not-owner-put-posts-detail.png)    |
| PUT Unauthenticated                                                          | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-put-posts-detail.png)            |
| DELETE Authenticated Owner                                                   | returns 204 response: post is deleted                                                                       | ✅ PASS     | [Screenshot](docs/tests/authenticated-owner-delete-posts-detail.png)     |
| DELETE Authenticated Not Owner                                               | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/authenticated-not-owner-delete-posts-detail.png) |
| DELETE Unauthenticated                                                       | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-delete-posts-detail.png)         |
| POST                                                                         | Not provided                                                                                                | ✅ PASS     |
| _[Post Like](https://photora-api.herokuapp.com/posts/12/likes)_              |                                                                                                             |             |
| GET Unauthenticated                                                          | returns a list of profiles that liked the specified post                                                    | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-posts-likes.png)             |
| GET Authenticated                                                            | returns a list of profiles that liked the specified post                                                    | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-posts-likes.png)               |
| POST Authenticated                                                           | returns 201 or 204 response: allows authenticated users to like the specified post                          | ✅ PASS     | [Screenshot](docs/tests/authenticated-post-posts-likes.png)              |
| POST Unauthenticated                                                         | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-post-posts-likes.png)            |
| PUT, DELETE                                                                  | Not provided                                                                                                | ✅ PASS     |
| _[Post Search](https://photora-api.herokuapp.com/posts/search?keywords=dog)_ |                                                                                                             |             |
| GET Unauthenticated                                                          | returns a list of posts containing keywords                                                                 | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-posts-search.png)            |
| GET Authenticated                                                            | returns a list of posts containing keywords                                                                 | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-posts-search.png)              |
| GET Empty Keywords                                                           | returns 400 Bad Request error                                                                               | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-posts-search-empty.png)        |
| POST, PUT, DELETE                                                            | Not provided                                                                                                | ✅ PASS     |
| _[Profile Post List](https://photora-api.herokuapp.com/profiles/8/posts)_    |                                                                                                             |             |
| GET Unauthenticated                                                          | returns all the post from the specified profile                                                             | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-profiles-posts.png)          |
| GET Authenticated                                                            | returns all the post from the specified profile                                                             | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-profiles-posts.png)            |
| POST, PUT, DELETE                                                            | Not provided                                                                                                | ✅ PASS     |
| _[Follow Post List](https://photora-api.herokuapp.com/posts/feed)_           |                                                                                                             |             |
| GET Authenticated                                                            | allows authenticated users to retrieve a list of all the post from the profiles they follow                 | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-follow-posts.png)              |
| GET Unauthenticated                                                          | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-follow-posts.png)            |
| POST, PUT, DELETE                                                            | Not provided                                                                                                | ✅ PASS     |
| _[Liked Post List](https://photora-api.herokuapp.com/posts/liked)_           |                                                                                                             |             |
| GET Authenticated                                                            | allows authenticated users to retrieve a list of all the post they liked                                    | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-liked-posts.png)               |
| GET Unauthenticated                                                          | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-liked-posts.png)             |
| POST, PUT, DELETE                                                            | Not provided                                                                                                | ✅ PASS     |
| **Comments**                                                                 |                                                                                                             |             |                                                                          |
| _[Comment List](https://photora-api.herokuapp.com/posts/18/comments)_        |                                                                                                             |             |
| GET Unauthenticated                                                          | returns a list of all the comments from a specified post                                                    | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-comments.png)                |
| GET Authenticated                                                            | returns a list of all the comments from a specified post                                                    | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-comments.png)                  |
| POST Authenticated                                                           | returns 201 response: allows authenticated users to create comments                                         | ✅ PASS     | [Screenshot](docs/tests/authenticated-post-comments.png)                 |
| POST Unauthenticated                                                         | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-post-comments.png)               |
| PUT, DELETE                                                                  | Not provided                                                                                                | ✅ PASS     |
| _[Comment Detail](https://photora-api.herokuapp.com/posts/18/comments/20)_   |                                                                                                             |             |
| GET Unauthenticated                                                          | returns the comment specified by id                                                                         | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-get-comments-detail.png)         |
| GET Authenticated                                                            | returns the comment specified by id                                                                         | ✅ PASS     | [Screenshot](docs/tests/authenticated-get-comments-detail.png)           |
| PUT Authenticated Owner                                                      | allows the owner to update the comment                                                                      | ✅ PASS     | [Screenshot](docs/tests/authenticated-owner-put-comments-detail.png)     |
| PUT Authenticated Not Owner                                                  | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/authenticated-not-owner-put-comments-detail.png) |
| PUT Unauthenticated                                                          | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-put-comments-detail.png)         |
| DELETE Authenticated Owner                                                   | returns 204 response, comment is deleted                                                                    | ✅ PASS     | [Screenshot](docs/tests/authenticated-owner-delete-comments-detail.png)  |
| DELETE Authenticated Not Owner                                               | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/authenticated-not-owner-delete-posts-detail.png) |
| DELETE Unauthenticated                                                       | returns 403 error                                                                                           | ✅ PASS     | [Screenshot](docs/tests/unauthenticated-delete-posts-detail.png)         |
| POST                                                                         | Not provided                                                                                                | ✅ PASS     |