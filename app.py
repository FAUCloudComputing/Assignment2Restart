# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import signal
import sys
import traceback
from types import FrameType

from flask import Flask, redirect, request, jsonify, session, send_file, Response

import storage
from utils.logging import logger

app = Flask(__name__)
app.secret_key = '47238947238439279382479'


@app.route('/')
def index():
    print("GET /")
    index_html = """
            <!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Image Upload App</title>
    <script src="https://www.gstatic.com/firebasejs/ui/6.0.2/firebase-ui-auth__en.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <link type="text/css" rel="stylesheet" href="https://www.gstatic.com/firebasejs/ui/6.0.2/firebase-ui-auth.css" />

    <script src="https://www.gstatic.com/firebasejs/9.13.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.13.0/firebase-auth-compat.js"></script>
    
    
    <script>
    var config = {
        apiKey: "AIzaSyAlTjagupmUrQ9veESjRJHhlgm9J4L4CxQ",
        authDomain: "vernal-landing-376714.firebaseapp.com",
    };
    firebase.initializeApp(config);
    </script>
    
    
    <script type="text/javascript">
      // FirebaseUI config.
      var uiConfig = {
        callbacks: {
          signInSuccessWithAuthResult: function(authResult, redirectUrl) {
            var user = authResult.user;
            var userId = user.uid;  // Get the user ID from the user object
            var credential = authResult.credential;
            var isNewUser = authResult.additionalUserInfo.isNewUser;
            var providerId = authResult.additionalUserInfo.providerId;
            var operationType = authResult.operationType;
        
            // Store the user ID in the Flask session object
            fetch('/store_user_id', {
              method: 'POST',
              body: JSON.stringify({'user_id': userId}),
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(function(response) {
              // Redirect to the image upload page
              window.location.assign('/image');
            });
        
            // Return false to prevent automatic redirect
            return false;
          },
          signInFailure: function(error) {
            // Some unrecoverable error occurred during sign-in.
            // Return a promise when error handling is completed and FirebaseUI
            // will reset, clearing any UI. This commonly occurs for error code
            // 'firebaseui/anonymous-upgrade-merge-conflict' when merge conflict
            // occurs. Check below for more details on this.
            return handleUIError(error);
          },
          uiShown: function() {
            // The widget is rendered.
            // Hide the loader.
            document.getElementById('loader').style.display = 'none';
          }
        },
        credentialHelper: firebaseui.auth.CredentialHelper.NONE,
        // Query parameter name for mode.
        queryParameterForWidgetMode: 'mode',
        // Query parameter name for sign in success url.
        queryParameterForSignInSuccessUrl: 'signInSuccessUrl',
        // Will use popup for IDP Providers sign-in flow instead of the default, redirect.
        signInFlow: 'popup',
        signInSuccessUrl: '/image',
        signInOptions: [
          // Leave the lines as is for the providers you want to offer your users.
          firebase.auth.GoogleAuthProvider.PROVIDER_ID,
          {
            provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
            // Whether the display name should be displayed in the Sign Up page.
            requireDisplayName: true
          },
          // firebaseui.auth.AnonymousAuthProvider.PROVIDER_ID // THIS IS THE ANONYMOUS LOGIN
        ],
        // Set to true if you only have a single federated provider like
        // firebase.auth.GoogleAuthProvider.PROVIDER_ID and you would like to
        // immediately redirect to the provider's site instead of showing a
        // 'Sign in with Provider' button first. In order for this to take
        // effect, the signInFlow option must also be set to 'redirect'.
        immediateFederatedRedirect: false,
        // tosUrl and privacyPolicyUrl accept either url string or a callback
        // function.
        // Terms of service url/callback.
        tosUrl: '<your-tos-url>',
        // Privacy policy url/callback.
        privacyPolicyUrl: function() {
          window.location.assign('<your-privacy-policy-url>');
        }
      };

      var ui = new firebaseui.auth.AuthUI(firebase.auth());
      // The start method will wait until the DOM is loaded.
      ui.start('#firebaseui-auth-container', uiConfig);
    </script>
  </head>
  <body>
    <!-- The surrounding HTML is left untouched by FirebaseUI.
         Your app may use that space for branding, controls and other customizations.-->
    <h1><div align="center"><br />Cloud Computing<br />Image Upload App<br /><br /> </div></h1>
    <div id="firebaseui-auth-container"></div>
    <div id="loader">Loading...</div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
  </body>
</html>
            """

    return index_html


@app.route('/image')
def image():
    print("GET /image")

    # Get the user_id from the session
    user_id = session.get('user_id')

    # Call the list_db_entries API to get a list of all image files for this user
    images = storage.list_db_entries(user_id)

    # Generate HTML for displaying the list of image files
    image_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
            <title>Image List</title>

            <style>
            fieldset { margin: 0; }  
            legend { font-size: 1.5em; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: bold; }
            input { margin: 10px; }
            button { margin: 10px; }
            li { font-size: 1em; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 10px; }
            </style>

        </head>
        <body>
            <fieldset>
                <form method="POST" enctype="multipart/form-data" action="/upload">
                <legend>Upload Image</legend>
                <input type="file" id="file" name="form_file" accept="image/jpeg"/>
                <button>Upload</button>
                </form>
            </fieldset>
            <br />
            <div>
                <h4>List of Image Files:</h4>
                <ul>
    """

    # Add a link to each image file in the list
    for main_image in images:
        image_html += "<li><a href=\"/files/" + main_image['Name'] + "\" target=\"_blank\">" + main_image[
            'Name'] + "</a></li>"

    # Close the HTML tags
    image_html += """
                </ul>
            </div>
            <div align="right"><button onClick='document.location.href="https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=https://assignment2restart-pexpqiuvaa-uc.a.run.app"'>Log Out</button></div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
        </body>
        </html>
    """

    return image_html


@app.route('/store_user_id', methods=['POST'])
def store_user_id():
    print("POST /store_user_id")

    # Get the user_id from the request JSON data
    user_id = request.json['user_id']

    # Store the user_id in the session
    session['user_id'] = user_id

    # Return a JSON response with a status message
    return jsonify({'status': 'success'})


@app.route('/upload', methods=['POST'])
def upload():
    try:
        print("POST /upload")

        # Get the file from the request
        file = request.files['form_file']

        # Get the user_id from the session
        user_id = session.get('user_id')

        # Extract file name and size
        file_name = file.filename.split('.')[0]
        file_size = len(file.read())

        # Store file metadata in the database
        storage.add_db_entry(user_id, file_name, file_size)

        # Upload file to storage
        blob_name = f"{file_name}.jpg"
        storage.upload_file(user_id, blob_name, file)

    except:
        # If an exception occurs, print the traceback
        traceback.print_exc()

    # Redirect to the previous page
    return redirect(request.referrer)


@app.route('/files/<filename>')
def get_file(filename):
    # Get the user_id from the session
    user_id = session.get('user_id')

    # Download the file from storage
    image_data = storage.download_file(user_id, f"{filename}.jpg")

    # Return a response with the file data and MIME type
    return Response(image_data, mimetype='image/jpeg')


# @app.route("/")
# def hello() -> str:
#     # Use basic logging with custom fields
#     logger.info(logField="custom-entry", arbitraryField="custom-entry")

#     # https://cloud.google.com/run/docs/logging#correlate-logs
#     logger.info("Child logger with trace Id.")

#     return "Hello, World!"


def shutdown_handler(signal_int: int, frame: FrameType) -> None:
    logger.info(f"Caught Signal {signal.strsignal(signal_int)}")

    from utils.logging import flush

    flush()

    # Safely exit program
    sys.exit(0)


if __name__ == "__main__":
    # Running application locally, outside of a Google Cloud Environment

    # handles Ctrl-C termination
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(host="localhost", port=8080, debug=True)
else:
    # handles Cloud Run container termination
    signal.signal(signal.SIGTERM, shutdown_handler)
