# The Philosopher's Corner

**For personal usage - but if you're into the wisdom I've accumulated throughout the years, just clone this and do this (I assume that you have Python set up and you know a bit of Python)**:

1. Set up an AWS account and set up a S3 bucket. Note down the name of your bucket. Crreate any necessary configuration (look up AWS docs if you're stuck).
2. Upload your finished `wisdom.json` to your S3 bucket.
3. Create `aws.json` and include the following (make sure you don't put any sensitive info in gitignore):
```json
{
    "bucket_name": "<your-bucket-name>",
    "s3_key": "/path/to/your/wisdom.json"
}
```
4. If you use Linux, put this in your `~/.bashrc`: `alias stoic='cd path/to/The_Philosophers_Corner/ && python src/main.py'` so the command `stoic` is enough to run the app. (If you don't use Linux ... get Linux)
5. That's it, now just run `main.py` and enjoy.

## User Stories - As a user I want to ...
- [x] See a black background of the Home page so there is less strain on my eyes.
- [x] See a random quote a.k.a "wisdom" when I click on the button "Show Wisdom".
- [x] Filter which category of "wisdom" (quote) I want to see through a dropdown of categories.
- [x] See a separate window being opened when I click on the button "Add Wisdom".
- [x] Add a piece of wisdom and place it in a cateogory (through a dropdown) in the new window.

## Technical Stories
- [x] Backend DB design: a single JSON file.
- [x] Store the JSON file in AWS S3 Bucket and retrieve it everytime the app is run.

## Architecture: MVVM (Model View View-Model)
- 2 day data binding between View and View Model. 
- View should not communicate with Model at all.
- ViewModel should not be aware of the View.
- Any logic that directly manipulates UI elements (like `self.lbl["state"] = "normal"`) should remain in the View.

## Design Patterns Used
- **Factory**: In the View, widgets are created and returned via methods, for reusability and easier layout management.

## AWS S3 Bucket
- Prod data is stored on my S3 bucket - when running `main.py` the file is downloaded and viewed locally. 
- The file is destroyed upon closing the app - if any updates occurred with the file, then it is uploaded to S3 again before the app is closed.
