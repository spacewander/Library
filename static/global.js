var debugMode = true;

// log the message when in debug mode
function log(message) {
    if (!debugMode) {
        return;
    }
    if (console) {
        console.log(message);
    }
}

// store the value with key
function store(key, value) {
    if (!value) {
      console.warn('should be a value stored by ' + key);
    }
    else {
        try {
            console.log(key);
            localStorage.setItem(key, encodeURIComponent(value));
            log('store: ' + value);
        }
        catch (e) {
            log('store: ' + value + ' failed.');
        }
    }
}

// get the value with key
function get(key) {
    if (!key) {
        console.warn('should have a key to get something');
    }
    else {
        var value = localStorage.getItem(key);
        try {
            return value ? decodeURIComponent(value) : '';
        }
        catch (e) {
            return '';
        }
    }
}

// the web address of the app
var baseURL = window.location.href.replace(/(\?|#).*$/,"").replace(/((http:|https|)\/.*\/)(.*$)/, "$1");

// get the route part of URL
function getURLComponent() {
    return window.location.href.replace(/(\?|#).*$/, "").replace(/^.*\//, "");
}

// defines some URL patterns
var Global = {
    homepage : baseURL,
    showEntries : baseURL + 'entries',
    adminEntries : baseURL + 'admin',
    login : baseURL + 'login'
};

