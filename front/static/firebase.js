/**
 * Copyright 2021 Google LLC
 * Licensed under the Apache License, Version 2.0 (the `License`);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an `AS IS` BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

firebase.initializeApp(config);

// Watch for state change from sign in
function initApp() {
  const users = ["thibault.lefevre@loreal.com", "thibault.lefevre@converteo.com", "meirkhan.rakhmetzhanov@converteo.com"];
  firebase.auth().onAuthStateChanged(user => {
    if (user) {
      // User is signed in.
      if (users.includes(user.email)) {
      // if (user.email.indexOf('@converteo.com') > -1) {
        
        document.getElementById('signInButton').innerText = 'Sign Out';
        document.getElementById('chatbox').style.display = '';
        document.getElementById('input-area').style.display = '';
        document.getElementById('user-input').style.display = '';
        document.getElementById('send-button').style.display = '';
        
      }
      else{
        document.getElementById('signInButton').innerText = 'Unauthorized';
        document.getElementById('chatbox').style.display = 'none';
        document.getElementById('input-area').style.display = 'none';
        document.getElementById('user-input').style.display = 'none';
        document.getElementById('send-button').style.display = 'none';

      }
    } else {
      // No user is signed in.
      document.getElementById('signInButton').innerText = 'Sign In with Google';
      document.getElementById('chatbox').style.display = 'none';
      document.getElementById('input-area').style.display = 'none';
      document.getElementById('user-input').style.display = 'none';
      document.getElementById('send-button').style.display = 'none';
    }
  });
}
window.onload = function () {
  initApp();
};

function signIn() {
  const provider = new firebase.auth.GoogleAuthProvider();
  provider.addScope('https://www.googleapis.com/auth/userinfo.email');
  firebase
    .auth()
    .signInWithPopup(provider)
    .then(result => {
      // Returns the signed in user along with the provider's credential
      console.log(`${result.user.displayName} logged in.`);
      window.alert(`Welcome ${result.user.displayName}!`);
    })
    .catch(err => {
      console.log(`Error during sign in: ${err.message}`);
      window.alert(`Sign in failed. Retry or check your browser logs.`);
    });
}

function signOut() {
  firebase
    .auth()
    .signOut()
    .then(result => {})
    .catch(err => {
      console.log(`Error during sign out: ${err.message}`);
      window.alert(`Sign out failed. Retry or check your browser logs.`);
    });
}

// Toggle Sign in/out button
function toggle() {
  if (!firebase.auth().currentUser) {
    signIn();
  } else {
    signOut();
  }
}

