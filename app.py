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
import os, traceback

from types import FrameType
from flask import Flask, redirect, request
from utils.logging import logger

app = Flask(__name__)

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
            var credential = authResult.credential;
            var isNewUser = authResult.additionalUserInfo.isNewUser;
            var providerId = authResult.additionalUserInfo.providerId;
            var operationType = authResult.operationType;
            // Do something with the returned AuthResult.
            // Return type determines whether we continue the redirect
            // automatically or whether we leave that to developer to handle.
            return true;
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
          firebaseui.auth.AnonymousAuthProvider.PROVIDER_ID
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
    image_html = """
            # <!DOCTYPE html>
            # <html>
            # <head>
            #     <title>Upload Image</title>
                
            #     <style>
            #     fieldset { margin: 0; }  
            #     legend { font-size: 1.5em; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: bold; }
            #     input { margin: 10px; }
            #     button { margin: 10px; }
            #     li { font-size: 1em; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 10px; }
            #     </style>
                
            # </head>
            # <body>
            #     <fieldset>
            #         <form method="POST" enctype="multipart/form-data" action="/upload">
            #         <legend>Upload Image</legend>
            #         <input type="file" id="file" name="form_file" accept="image/jpeg"/>
            #         <button>Upload</button>
            #         </form>
            #     </fieldset>
            #     <br />
            #     <div align="right"><button onClick='document.location.href="https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://34.172.81.167:8080/"'>Log Out</button></div>
            test
            """
            
    for file in list_of_files():
        image_html += "<li><a href=\"/files/" + file + "\">" + file + "</a></li>"
    
    return image_html

@app.route('/upload', methods=['POST'])
def upload():
    try:
        
        print("POST /upload")
        file = request.files['form_file'] 
        file.save(os.path.join("./files", file.filename))
        
    except:
        traceback.print_exc()
    return redirect('/')

@app.route('/files')
def list_of_files():
    print("GET /files")
    files = os.listdir("./files")
    for file in files:
        if not file.endswith('.jpg'):
            files.remove(file)
    return files

@app.route('/files/<filename>')
def get_file(filename):
    print("GET /files/+filename")
    return 'Get File ' + filename


 



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
